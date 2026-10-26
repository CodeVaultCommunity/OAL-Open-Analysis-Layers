"""Run the local Tiny Catalog demonstration."""
import argparse
from pathlib import Path
import sys
from wsgiref.simple_server import make_server

from tiny_catalog.composition import build_application
from tiny_catalog.errors import StoreUnavailable
from tiny_catalog.transport.wsgi import CatalogWSGI


def create_handler(database: Path) -> CatalogWSGI:
    """Build the example's WSGI boundary for the repository launcher."""
    application = build_application(database)

    def report_error(kind: str, error: Exception) -> None:
        # Do not expose entity payloads or database details in the client response.
        print(f"{kind}: {type(error).__name__}", file=sys.stderr)

    return CatalogWSGI(application, report_error)


def main() -> None:
    parser = argparse.ArgumentParser(description="OAL Tiny Catalog — local demonstration")
    parser.add_argument("--database", type=Path, default=Path("data/catalog.sqlite3"))
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    try:
        handler = create_handler(args.database)
    except (OSError, StoreUnavailable) as error:
        parser.exit(1, f"Cannot initialize local storage: {error}\n")
    try:
        with make_server("127.0.0.1", args.port, handler) as server:
            print(f"Tiny Catalog: http://127.0.0.1:{args.port}/items", flush=True)
            print("Local demonstration; press Ctrl+C to stop.", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    except OSError as error:
        parser.exit(1, f"Cannot start the local server: {error}\n")


if __name__ == "__main__":
    main()
