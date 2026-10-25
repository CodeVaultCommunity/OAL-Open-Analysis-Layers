"""Launch any OAL example from any edition through an executor selected per example."""
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
VERSIONING = ROOT / "versioning"
CURRENT = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").is_file() else ""


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
            prog=f"python run_examples.py {example.key}",
            description=f"Run the {example.key} example in a local browser",
        )
        parser.add_argument("--port", type=int, default=example.default_port)
        parser.add_argument("--database", type=Path)
        parser.add_argument("--no-browser", action="store_true")
        args = parser.parse_args(argv)
        if args.port is None or not 1 <= args.port <= 65535:
            parser.error("port must be between 1 and 65535")
        if example.database_name is None:
            parser.error("this example has no database configuration")

        database = args.database or ROOT / "data" / example.version / example.database_name
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
    """Find every version/example that declares a runner.json."""
    examples: list[Example] = []
    if not VERSIONING.is_dir():
        return examples
    for version_dir in sorted(path for path in VERSIONING.iterdir() if path.is_dir()):
        examples_dir = version_dir / "examples"
        if not examples_dir.is_dir():
            continue
        for example_dir in sorted(path for path in examples_dir.iterdir() if path.is_dir()):
            runner = example_dir / "runner.json"
            if not runner.is_file():
                continue
            data = json.loads(runner.read_text(encoding="utf-8"))
            examples.append(
                Example(
                    version=version_dir.name,
                    name=data["name"],
                    directory=example_dir,
                    executor=data["executor"],
                    entrypoint=data["entrypoint"],
                    default_port=data.get("default_port"),
                    database_name=data.get("database_name"),
                )
            )
    return examples


def resolve(selection: str, examples: Sequence[Example]) -> Example:
    """Resolve EDITION/NAME or a bare NAME (preferring the current edition)."""
    if "/" in selection:
        version, _, name = selection.partition("/")
        matches = [item for item in examples if item.version == version and item.name == name]
    else:
        matches = [item for item in examples if item.name == selection]
    if not matches:
        available = ", ".join(item.key for item in examples) or "none"
        raise SystemExit(f"Unknown example: {selection}\nAvailable: {available}")
    if len(matches) == 1:
        return matches[0]
    current = [item for item in matches if item.version == CURRENT]
    if len(current) == 1:
        return current[0]
    available = ", ".join(item.key for item in matches)
    raise SystemExit(f"Ambiguous example name: {selection}\nUse one of: {available}")


def catalog(examples: Sequence[Example]) -> None:
    for item in examples:
        port = item.default_port if item.default_port is not None else "-"
        print(f"{item.key}  (port {port})")


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(
        description="Run an OAL example from any edition",
        epilog="Use --list to see every example of every edition. "
               "A bare NAME resolves to the current edition; use EDITION/NAME otherwise.",
    )
    parser.add_argument("example", nargs="?", help="NAME or EDITION/NAME")
    parser.add_argument("--list", action="store_true", help="list every example of every edition")

    if not arguments or arguments[0] in {"-h", "--help"}:
        examples = discover()
        parser.print_help()
        print()
        catalog(examples)
        return 0 if arguments else 2
    if arguments[0] == "--list":
        catalog(discover())
        return 0

    selection = parser.parse_args(arguments[:1])
    if selection.example is None:
        parser.error("an example is required")
    example = resolve(selection.example, discover())
    return EXECUTORS[example.executor].run(example, arguments[1:])


if __name__ == "__main__":
    raise SystemExit(main())
