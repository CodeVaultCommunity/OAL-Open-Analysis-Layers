"""Launch examples belonging only to this self-contained OAL edition."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from importlib import import_module
import json
from pathlib import Path
import sys
from threading import Timer
from typing import Protocol, Sequence
import webbrowser
from wsgiref.simple_server import make_server


ROOT = Path(__file__).resolve().parent
EDITION = "Stable-v1.0.0"


@dataclass(frozen=True)
class Example:
    version: str
    name: str
    directory: Path
    executor: str
    entrypoint: str
    default_port: int | None = None
    database_name: str | None = None

    @property
    def key(self) -> str:
        return f"{self.version}/{self.name}"


class ExampleExecutor(Protocol):
    """Interpret the arguments and launch one kind of example."""

    def run(self, example: Example, argv: Sequence[str]) -> int: ...


class PythonWSGIExecutor:
    """Run a Python example that exposes a WSGI handler factory."""

    def run(self, example: Example, argv: Sequence[str]) -> int:
        parser = argparse.ArgumentParser(
            prog=f"python run_examples.py {example.name}",
            description=f"Run the {example.key} example in a local browser",
        )
        parser.add_argument("--port", type=int, default=example.default_port)
        parser.add_argument("--database", type=Path, help="SQLite file; relative paths use the current working directory")
        parser.add_argument("--no-browser", action="store_true")
        args = parser.parse_args(argv)
        if args.port is None or not 1 <= args.port <= 65535:
            parser.error("port must be between 1 and 65535")
        if example.database_name is None:
            parser.error("this example has no database configuration")

        database = args.database or ROOT / "data" / example.database_name
        database.parent.mkdir(parents=True, exist_ok=True)
        module_name, separator, factory_name = example.entrypoint.partition(":")
        if not separator or not module_name or not factory_name:
            parser.error("invalid Python handler entrypoint")
        sys.path.insert(0, str(example.directory / "src"))
        factory = getattr(import_module(module_name), factory_name)

        try:
            handler = factory(database)
            url = f"http://127.0.0.1:{args.port}/"
            with make_server("127.0.0.1", args.port, handler) as server:
                print(f"{example.key}: {url}\nPress Ctrl+C to stop.", flush=True)
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


EXECUTORS: dict[str, ExampleExecutor] = {"python-wsgi": PythonWSGIExecutor()}


def discover() -> list[Example]:
    """Read runner declarations only from this launcher's sibling examples."""
    examples: list[Example] = []
    examples_dir = ROOT / "examples"
    if not examples_dir.is_dir():
        return examples
    for runner in sorted(examples_dir.glob("*/runner.json")):
        data = json.loads(runner.read_text(encoding="utf-8"))
        examples.append(Example(
            version=EDITION,
            name=data["name"],
            directory=runner.parent,
            executor=data["executor"],
            entrypoint=data["entrypoint"],
            default_port=data.get("default_port"),
            database_name=data.get("database_name"),
        ))
    return examples


def resolve(selection: str, examples: Sequence[Example]) -> Example:
    """Resolve a bare NAME within this edition; never fall back to another."""
    matches = [item for item in examples if item.name == selection]
    if not matches:
        available = ", ".join(item.name for item in examples) or "none"
        raise SystemExit(f"Unknown example in {EDITION}: {selection}\n"
                         f"Use a bare NAME. Available: {available}")
    return matches[0]


def catalog(examples: Sequence[Example]) -> None:
    for item in examples:
        port = item.default_port if item.default_port is not None else "-"
        print(f"{item.name}  (port {port})")


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(
        description=f"Run an OAL example from {EDITION}",
        epilog="Use --list to see this edition\'s examples. Select another edition through its own launcher path.",
    )
    parser.add_argument("example", nargs="?", help="NAME in this edition")
    parser.add_argument("--list", action="store_true", help="list this edition's examples")

    if not arguments or arguments[0] in {"-h", "--help"}:
        examples = discover()
        parser.print_help()
        print()
        catalog(examples)
        return 0 if arguments else 2
    if arguments[0] == "--list":
        parser.parse_args(arguments)
        catalog(discover())
        return 0

    selection = parser.parse_args(arguments[:1])
    if selection.example is None:
        parser.error("an example is required")
    example = resolve(selection.example, discover())
    return EXECUTORS[example.executor].run(example, arguments[1:])


if __name__ == "__main__":
    raise SystemExit(main())
