"""Launch repository examples through an executor selected for each example."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
import sys
from threading import Timer
from typing import Protocol, Sequence
import webbrowser
from wsgiref.simple_server import make_server


EXAMPLES_ROOT = Path(__file__).resolve().parent
ROOT = EXAMPLES_ROOT.parent
EDITION = EXAMPLES_ROOT / "Alpha-v0.1.0-Alkimim"


@dataclass(frozen=True)
class Example:
    name: str
    directory: Path
    executor: str
    entrypoint: str
    default_port: int | None = None
    database_name: str | None = None


class ExampleExecutor(Protocol):
    """Interpret the arguments and launch one kind of example."""

    def run(self, example: Example, argv: Sequence[str]) -> int: ...


class PythonWSGIExecutor:
    """Run a Python example that exposes a WSGI handler factory."""

    def run(self, example: Example, argv: Sequence[str]) -> int:
        parser = argparse.ArgumentParser(
            prog=f"python examples/run_examples.py {example.name}",
            description=f"Run the {example.name} example in a local browser",
        )
        parser.add_argument("--port", type=int, default=example.default_port)
        parser.add_argument("--database", type=Path)
        parser.add_argument("--no-browser", action="store_true")
        args = parser.parse_args(argv)
        if args.port is None or not 1 <= args.port <= 65535:
            parser.error("port must be between 1 and 65535")
        if example.database_name is None:
            parser.error("this example has no database configuration")

        database = args.database or ROOT / "data" / example.database_name
        module_name, separator, factory_name = example.entrypoint.partition(":")
        if not separator or not module_name or not factory_name:
            parser.error("invalid Python handler entrypoint")
        sys.path.insert(0, str(example.directory / "src"))
        factory = getattr(import_module(module_name), factory_name)

        try:
            handler = factory(database)
            url = f"http://127.0.0.1:{args.port}/"
            with make_server("127.0.0.1", args.port, handler) as server:
                print(f"{example.name}: {url}\nPress Ctrl+C to stop.", flush=True)
                if not args.no_browser:
                    opener = Timer(0.5, webbrowser.open, args=(url,))
                    opener.daemon = True
                    opener.start()
                server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
        except OSError as error:
            parser.exit(1, f"Cannot start local example: {error}\n")
        return 0


EXAMPLES = {
    "tiny-catalog": Example(
        name="tiny-catalog",
        directory=EDITION / "tiny-catalog",
        executor="python-wsgi",
        entrypoint="tiny_catalog.__main__:create_handler",
        default_port=8000,
        database_name="catalog.sqlite3",
    ),
    "board-crm": Example(
        name="board-crm",
        directory=EDITION / "board-crm",
        executor="python-wsgi",
        entrypoint="board_crm.__main__:create_handler",
        default_port=8001,
        database_name="board-crm.sqlite3",
    ),
    "work-board": Example(
        name="work-board",
        directory=EDITION / "work-board",
        executor="python-wsgi",
        entrypoint="work_board.__main__:create_handler",
        default_port=8002,
        database_name="work-board.sqlite3",
    ),
}

EXECUTORS: dict[str, ExampleExecutor] = {"python-wsgi": PythonWSGIExecutor()}


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description="Run an OAL example")
    parser.add_argument("example", choices=sorted(EXAMPLES))
    if not arguments or arguments[0] in {"-h", "--help"}:
        parser.print_help()
        return 0 if arguments else 2

    selection = parser.parse_args(arguments[:1])
    example = EXAMPLES[selection.example]
    return EXECUTORS[example.executor].run(example, arguments[1:])


if __name__ == "__main__":
    raise SystemExit(main())
