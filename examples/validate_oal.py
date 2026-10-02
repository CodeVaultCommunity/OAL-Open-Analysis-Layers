"""Check cross-layer identities and local documentation links in the examples."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "examples" / "Alpha-v0.1.0-Alkimim"
TRANSITIONS = {
    ("needs", "ucs"),
    ("ucs", "adpm"),
    ("ucs", "advs"),
    (("adpm", "advs"), "adi"),
    ("adi", "adib"),
}


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_example(base: Path) -> None:
    tiny = base.name == "tiny-catalog"
    ucs = read(base / ("OAL-P1/index.json" if tiny else "OAL-P1/ucs.json"))
    cases = ucs["use_cases"]
    ids = [case["id"] for case in cases]
    require(len(ids) == len(set(ids)), f"duplicate UCS identity: {base}")
    needs = read(base / "needs-baseline.json")
    require(needs["version"] == "0.1.0", f"needs version: {base}")
    require({item["id"] for item in needs["needs"]} ==
            ({ref for case in cases for ref in case["needs"]} if tiny else
             {ref for case in cases for ref in case["needs"]}), f"needs coverage: {base}")

    bt = read(base / "OAL-P2/advs/behavioral-tests.json")["tests"]
    require(len(bt) == len(ids), f"BT count: {base}")
    require({item["ucs_case_id"] for item in bt} == set(ids), f"BT case IDs: {base}")
    require(len({item["id"] for item in bt}) == len(ids), f"duplicate BT: {base}")
    for item in bt:
        case = next(case for case in cases if case["id"] == item["ucs_case_id"])
        criteria = case["criteria"] if tiny else [criterion["id"] for criterion in case["criteria"]]
        require(set(item["ucs_criteria"]) == set(criteria), f"BT criteria: {item['id']}")
        require(bool(item["supporting_checks"]), f"BT without checks: {item['id']}")
        supporting_text = []
        for reference in item["supporting_checks"]:
            filename, _, symbol = reference.partition("::")
            source = base / filename
            require(source.is_file(), f"missing check: {source}")
            source_text = source.read_text(encoding="utf-8")
            supporting_text.append(source_text)
            if symbol:
                require(symbol.rsplit(".", 1)[-1] in source_text,
                        f"missing test symbol: {reference}")
        for criterion in criteria:
            require(any(criterion in source_text for source_text in supporting_text),
                    f"criterion not named in supporting checks: {item['id']}: {criterion}")

    mapping = read(base / "OAL-P2/adpm/traceability.json")["mapping"]
    require(len(mapping) == len(ids), f"ADI mapping count: {base}")
    require({item["id"] for item in mapping} == set(ids), f"ADI case IDs: {base}")
    require({item["behavioral_test"] for item in mapping} == {item["id"] for item in bt},
            f"ADI to BT links: {base}")
    for item in mapping:
        source = base / item["source"]
        require(source.is_file(), f"missing implementation: {item['source']}")
        class_name = item["implementation"].split(":", 1)[-1]
        classes = {node.name: node for node in ast.parse(source.read_text(encoding="utf-8")).body
                   if isinstance(node, ast.ClassDef)}
        require(class_name in classes, f"missing case class: {item['implementation']}")
        case_ids = [node.value.value for node in classes[class_name].body
                    if isinstance(node, ast.Assign) and
                    any(isinstance(target, ast.Name) and target.id == "ucs_id" for target in node.targets)
                    and isinstance(node.value, ast.Constant)]
        require(case_ids == [item["id"]], f"implementation case ID: {item['implementation']}")

    p4 = read(base / "OAL-P4/traceability.json")
    forward = p4["interface_to_cases"]
    reverse = p4["cases_to_interface"]
    require({item["case_id"] for item in reverse} == set(ids), f"P4 case IDs: {base}")
    require(len({item["id"] for item in forward}) == len(forward), f"duplicate interface ID: {base}")
    require({ref for item in forward for ref in item["case_ids"]} == set(ids),
            f"unexposed case: {base}")
    for item in forward:
        require(set(item["case_ids"]) <= set(ids), f"unknown P4 case: {item['id']}")
    for item in reverse:
        expected = {element["id"] for element in forward if item["case_id"] in element["case_ids"]}
        require(set(item["interface_element_ids"]) == expected, f"P4 reverse link: {item['case_id']}")
    for item in mapping:
        linked = next(case["interface_element_ids"] for case in reverse if case["case_id"] == item["id"])
        require(set(item["interface_element_ids"]) == set(linked),
                f"ADPM to P4 link: {item['id']}")
    require(set(p4["interface_only"]) == {item["id"] for item in forward if not item["case_ids"]},
            f"P4-only elements: {base}")

    derivations = read(base / "derivations.json")["transitions"]
    actual = {(tuple(item["from"]) if isinstance(item["from"], list) else item["from"],
               item["to"]) for item in derivations}
    require(actual == TRANSITIONS, f"derivation transitions: {base}")
    for item in derivations:
        require(item["source_version"] == item["destination_version"] == "0.1.0",
                f"derivation version: {base}")
        require(item["scope"] and item["responsible_people"] and set(item["case_ids"]) == set(ids),
                f"derivation scope/owner: {base}")
    print(f"{base.name}: {len(ids)} cases, {len(bt)} behavioral test identities, {len(forward)} interface elements")


def check_code_boundary(base: Path) -> None:
    package_name = base.name.replace("-", "_")
    package = base / "src" / package_name
    require((package / "usecases").is_dir(), f"missing case package: {base}")
    require((package / "transport" / "wsgi.py").is_file(), f"missing P4 adapter: {base}")
    require((package / "transport" / "static").is_dir(), f"missing P4 static files: {base}")
    for source in package.rglob("*.py"):
        relative = source.relative_to(package)
        if relative.parts[0] == "transport" or relative.name == "__main__.py":
            continue
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        imported = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
                if node.level and not node.module:
                    imported.extend(alias.name for alias in node.names)
        for name in imported:
            require(not (name == "transport" or name.startswith("transport.") or
                         name == f"{package_name}.transport" or
                         name.startswith(f"{package_name}.transport.") or
                         name == "wsgiref" or name.startswith("wsgiref.") or
                         name == "http" or name.startswith("http.")),
                    f"P3 imports a P4 dependency: {source}: {name}")
            if "usecases" in relative.parts:
                require(not (name == "sqlite3" or name == "json" or
                             name.endswith("sqlite_store")),
                        f"use case imports storage or representation: {source}: {name}")
    for asset in package.rglob("*"):
        if asset.suffix in {".html", ".css", ".js"}:
            require("transport" in asset.relative_to(package).parts,
                    f"interface asset outside P4: {asset}")


def check_links() -> None:
    markdown_link = re.compile(r"(?<!!)\]\(([^)]+)\)")
    html_file = re.compile(r'(?:src|href)="([^"#]+)(?:#[^"]*)?"')
    checked = 0
    for source in ROOT.rglob("*.md"):
        if any(part in {".pytest_cache", ".mypy_cache"} for part in source.parts):
            continue
        content = source.read_text(encoding="utf-8")
        targets = [match.group(1).split("#", 1)[0] for match in markdown_link.finditer(content)]
        targets += [match.group(1) for match in html_file.finditer(content)]
        for target in targets:
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            require((source.parent / target).exists(), f"broken link: {source}: {target}")
            checked += 1
    print(f"checked {checked} local Markdown and HTML references")


if __name__ == "__main__":
    for project in ("tiny-catalog", "board-crm", "work-board"):
        check_example(EDITION / project)
        check_code_boundary(EDITION / project)
    check_links()
