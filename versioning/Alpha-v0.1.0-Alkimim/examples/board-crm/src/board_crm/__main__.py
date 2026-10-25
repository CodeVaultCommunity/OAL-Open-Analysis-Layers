"""Start the local Board CRM demonstration."""
from argparse import ArgumentParser
from pathlib import Path

from .composition import build_application
from .transport.wsgi import create_wsgi, serve


def create_handler(database: Path):
    """Build the example's WSGI boundary for the repository launcher."""
    return create_wsgi(build_application(database))


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=Path("data/board-crm.sqlite3"))
    parser.add_argument("--port", type=int, default=8001)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    serve(args.database, args.port)


if __name__ == "__main__":
    main()
