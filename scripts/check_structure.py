"""Check explicit references in the selected OAL example edition, not semantics."""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ORIGINS = {"external", "domain", "assumption", "l4-decision"}
PROJECTS = ("tiny-catalog", "board-crm", "work-board")
MODELS = {
    "L1": "OAL-EX-M1-CASE-CONTRACTS",
    "L2": "OAL-EX-M2-PROGRAM-SCENARIOS",
    "L3": "OAL-EX-M3-PYTHON-CORE",
    "L4": "OAL-EX-M4-HTTP-BOUNDARY",
}


def unique_object(pairs):
    data = {}
    for key, value in pairs:
        if key in data:
            raise ValueError(f"duplicate JSON key: {key}")
        data[key] = value
    return data


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)
    elif isinstance(value, dict):
        for child in value.values():
            yield from strings(child)


def check_origins(obligations):
    return [f"invalid origin for {o.get('id')}: {o.get('origin')!r}"
            for o in obligations if o.get("origin") not in ORIGINS]


class Checker:
    def __init__(self, root, edition):
        self.root = root.resolve()
        self.edition = edition
        self.base = self.root / "versioning" / edition
        self.errors = []
        self.counts = Counter()
        self.trees = {}

    def need(self, condition, message):
        if not condition:
            self.errors.append(message)

    def unique(self, entries, key, where):
        ids = [entry[key] for entry in entries]
        self.need(len(ids) == len(set(ids)), f"{where}: duplicate {key}")
        return set(ids)

    def path(self, base, ref):
        name, _, symbol = ref.partition("::")
        target = (base / name).resolve()
        self.counts["file_references"] += 1
        self.need(target.is_relative_to(self.root), f"reference outside repository: {ref}")
        self.need(target.exists(), f"missing reference: {base.relative_to(self.root)}/{ref}")
        if symbol and target.is_file() and target.suffix == ".py":
            if target not in self.trees:
                self.trees[target] = ast.parse(target.read_text(encoding="utf-8"))
            node = self.trees[target]
            for part in symbol.split("."):
                node = next((n for n in getattr(node, "body", [])
                             if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
                             and n.name == part), None)
                if node is None:
                    break
            self.need(node is not None, f"missing declared Python symbol: {ref}")
            self.counts["symbol_references"] += 1
        return target

    def project(self, name):
        project = self.base / "examples" / name
        manifest = read_json(project / "model-instances.json")
        ucs = read_json(project / ("OAL-P1/index.json" if name == "tiny-catalog" else "OAL-P1/ucs.json"))
        adpm = read_json(project / "OAL-P2/adpm/traceability.json")
        advs = read_json(project / "OAL-P2/advs/behavioral-tests.json")
        adib = read_json(project / "OAL-P4/traceability.json")
        derivations = read_json(project / "derivations.json")
        baseline = manifest["artifact_version"]
        expected = "0.2.1" if name == "work-board" and self.edition == "Stable-v1.0.0" else "0.2.0"
        self.need(baseline == expected, f"{name}: artifact baseline mismatch")
        ucs_version = next(ucs[k] for k in ("specification_version", "project_specification_version", "version") if k in ucs)
        self.need(ucs_version == baseline, f"{name}: UCS version mismatch")
        for label, doc in (("manifest", manifest), ("ucs", ucs), ("adpm", adpm), ("advs", advs), ("adib", adib), ("derivations", derivations)):
            if "oal_edition" in doc:
                self.need(doc["oal_edition"] == self.edition, f"{name}/{label}: edition mismatch")
            for key in ("version", "ucs_version", "adpm_version", "advs_version", "adi_version", "adib_version"):
                if key in doc:
                    self.need(doc[key] == baseline, f"{name}/{label}: {key} mismatch")
        cases = self.unique(ucs["use_cases"], "id", f"{name}/UCS")
        self.counts["cases"] += len(cases)
        actors = self.unique(ucs["actors"], "id", name + "/actors")
        entities = self.unique(ucs["entities"], "id", name + "/entities")
        rules = self.unique(ucs["rules"], "id", name + "/rules")
        obligations = ucs.get("obligations", ucs.get("quality_obligations", []))
        obligation_ids = self.unique(obligations, "id", name + "/obligations")
        self.errors.extend(f"{name}: {error}" for error in check_origins(obligations))
        catalog = {c["id"]: c["case_id"] for c in ucs.get("criterion_catalog", [])}
        if catalog:
            self.unique(ucs["criterion_catalog"], "id", name + "/criterion_catalog")
        criteria = {}
        for case in ucs["use_cases"]:
            owned = case["criteria"]
            ids = [c["id"] if isinstance(c, dict) else c for c in owned]
            self.need(len(ids) > 0 and len(ids) == len(set(ids)), f"{name}/{case['id']}: empty/duplicate criteria")
            for cid in ids:
                self.need(cid not in criteria, f"{name}: criterion has multiple owners: {cid}")
                criteria[cid] = case["id"]
                if catalog:
                    self.need(catalog.get(cid) == case["id"], f"{name}: criterion catalog owner mismatch: {cid}")
            self.need(case["initiating_actor"] in case["permitted_actors"], f"{name}: initiating actor not permitted")
            for key, allowed in (("permitted_actors", actors), ("entities", entities), ("rules", rules), ("obligations", obligation_ids), ("dependencies", cases)):
                self.need(set(case.get(key, [])) <= allowed, f"{name}/{case['id']}: unknown {key}")
        if catalog:
            self.need(catalog == criteria, f"{name}: unreferenced criterion catalog entries")
        shared = ucs.get("shared_criteria", [])
        shared_ids = self.unique(shared, "id", name + "/shared criteria")
        self.need(not shared_ids & criteria.keys(), f"{name}: shared/case criterion collision")
        for criterion in shared:
            self.need(bool(criterion["case_ids"]) and set(criterion["case_ids"]) <= cases, f"{name}: shared criterion case reference")
            self.need(bool(criterion["obligation_ids"]) and set(criterion["obligation_ids"]) <= obligation_ids, f"{name}: shared criterion obligation reference")
        for rule in ucs["rules"]:
            self.need(set(rule["applied_by"]) <= cases, f"{name}: unknown rule case")
        self.need(self.unique(adpm["mapping"], "id", name + "/ADPM") == cases, f"{name}: ADPM case correspondence")
        tests = advs["tests"]
        self.need(self.unique(tests, "ucs_case_id", name + "/ADVS") == cases, f"{name}: ADVS case correspondence")
        test_ids = self.unique(tests, "id", name + "/behavioral tests")
        by_case = {t["ucs_case_id"]: t for t in tests}
        for test in tests:
            expected_criteria = {cid for cid, owner in criteria.items() if owner == test["ucs_case_id"]}
            self.need(set(test["ucs_criteria"]) == expected_criteria, f"{name}/{test['id']}: criterion references/coverage mismatch")
            self.need(set(test.get("shared_criteria", [])) <= shared_ids, f"{name}: unknown shared criterion")
            for ref in test["supporting_checks"]:
                self.path(project, ref)
        for check in advs.get("shared_supporting_checks", []):
            self.need(set(check["criteria_verified"]) <= shared_ids, f"{name}: shared check criterion reference")
            self.need(set(check["case_ids"]) <= cases, f"{name}: shared check case reference")
            self.need(set(check["obligation_ids"]) <= obligation_ids, f"{name}: shared check obligation reference")
            self.need(set(check["behavioral_test_ids"]) <= test_ids, f"{name}: shared check test reference")
            self.path(project, check["reference"])
        interfaces = self.unique(adib["interface_to_cases"], "id", name + "/interfaces")
        forward = {(entry["id"], case) for entry in adib["interface_to_cases"] for case in entry["case_ids"]}
        reverse = {(interface, entry["case_id"]) for entry in adib["cases_to_interface"] for interface in entry["interface_element_ids"]}
        self.need(forward == reverse, f"{name}: ADIB mappings disagree")
        self.need({case for _, case in forward} == cases, f"{name}: ADIB case correspondence")
        self.need(self.unique(adib["cases_to_interface"], "case_id", name + "/ADIB") == cases, f"{name}: reverse ADIB cases")
        for entry in adpm["mapping"]:
            self.need(entry["behavioral_test"] == by_case[entry["id"]]["id"], f"{name}: ADPM/ADVS identity mismatch")
            self.need(set(entry["interface_element_ids"]) == {i for i,c in forward if c == entry["id"]}, f"{name}: ADPM/ADIB mapping mismatch")
            symbol = entry["implementation"].partition(":")[2]
            self.path(project, entry["source"] + "::" + symbol)
        instances = manifest["instances"]
        self.need([inst["layer"] for inst in instances] == list(MODELS), f"{name}: expected exactly four ordered instances")
        for inst in instances:
            layer = inst["layer"]; model = inst["model"]
            definition = self.path(project, model["definition"])
            definition_meta = read_json(definition.parent / "model.json")
            self.need(model["identity"] == MODELS[layer] == definition_meta["identity"], f"{name}/{layer}: model identity mismatch")
            self.need(model["version"] == definition_meta["version"] == "0.1.0", f"{name}/{layer}: model version mismatch")
            self.need(definition_meta["oal_edition"] == self.edition, f"{name}/{layer}: model edition mismatch")
            for key in ("definition", "translation", "template", "example", "counterexample", "assessment_reference"):
                if key in definition_meta:
                    self.path(definition.parent, definition_meta[key])
            for key in ("files", "symbols", "canonical_content", "boundary_files"):
                for ref in strings(inst["artifact"].get(key, [])):
                    self.path(project, ref)
            mapping = inst["mapping"]["cases"]
            self.need(set(mapping) == cases, f"{name}/{layer}: instance case correspondence")
            for case, target in mapping.items():
                if layer == "L1":self.need(target == case, f"{name}: L1 mapping mismatch")
                elif layer == "L2":self.need(target == {"adpm":case,"behavioral_test":by_case[case]["id"]}, f"{name}: L2 mapping mismatch")
                elif layer == "L3":self.path(project, target)
                elif layer == "L4":self.need(set(target) == {i for i,c in forward if c == case}, f"{name}: L4 mapping mismatch")
            if "report" in inst["evidence"]:self.path(project, inst["evidence"]["report"])
            self.need(inst["evidence"]["execution"]["status"] in {"recorded","not_recorded","not_applicable"}, f"{name}: evidence status")
            self.counts["instances"] += 1
        needs_version = read_json(project / "needs-baseline.json")["version"]
        self.need(needs_version == "0.2.0", f"{name}: reconstructed needs version")
        for transition in derivations["transitions"]:
            self.need(set(transition["case_ids"]) == cases, f"{name}: derivation scope mismatch")
            self.need(transition["source_version"] == (needs_version if transition["from"] == "needs" else baseline), f"{name}: derivation source version")
            self.need(transition["destination_version"] == baseline, f"{name}: derivation destination version")
            for key in ("source_artifact", "source_artifacts", "destination_artifact", "destination_artifacts", "interface_mapping"):
                for ref in strings(transition.get(key, [])):self.path(project, ref)
            for source in transition.get("additional_sources", []):
                self.need(source["version"] == baseline, f"{name}: additional source version")
        self.need(derivations["engine_status"] == "not_demonstrated", f"{name}: unexpected transformer claim")
        self.counts["projects"] += 1

    def documents(self):
        paths = list(self.root.glob("*.md")) + list((self.root / ".github").rglob("*.md"))
        paths += list((self.root / "assets").rglob("*.md"))
        paths += list((self.root / "docs").rglob("*.md"))
        paths += [p for p in self.base.rglob("*.md") if not any(part.startswith("historical-") for part in p.parts)]
        # Check operational links in the two frozen editions without revalidating their models.
        for edition in sorted((self.root / "versioning").glob("Alpha-*")):
            examples = edition / "examples"
            paths += list(examples.glob("README*.md"))
            for project in PROJECTS:
                paths += list((examples / project).glob("README*.md"))
        for path in paths:
            # Only explicit Markdown links and HTML media references outside fenced examples.
            text = re.sub(r"(?ms)^ *(\x60{3,}|~{3,}).*?^ *\1 *$", "", path.read_text(encoding="utf-8"))
            targets = re.findall(r"\[[^\]\n]*\]\(([^)\s]+)(?:\s+[^)]*)?\)", text)
            targets += re.findall(r'(?:src|href)="([^"]+)"', text)
            for ref in targets:
                ref = ref.strip("<>")
                parsed = urlsplit(ref)
                if parsed.scheme or ref.startswith("//"):
                    continue
                target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
                self.counts["document_links"] += 1
                self.need(target.is_relative_to(self.root) and target.exists(), f"{path.relative_to(self.root)}: missing local link {ref}")
                # Anchors: explicit HTML IDs and ordinary Markdown heading slugs.
                if target.exists() and target.suffix == ".md" and parsed.fragment:
                    content = target.read_text(encoding="utf-8")
                    anchors = set(re.findall(r'<a\s+id="([^"]+)"', content))
                    for heading in re.findall(r"(?m)^#{1,6}\s+(.+)$", content):
                        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
                        anchors.add(slug)
                    self.need(unquote(parsed.fragment) in anchors, f"{path.relative_to(self.root)}: missing anchor {ref}")

    def metadata(self):
        if (self.root / "VERSION").read_text(encoding="utf-8").strip() == self.edition:
            citation = (self.root / "CITATION.cff").read_text(encoding="utf-8")
            self.need(f"version: {self.edition}\n" in citation, "CITATION/VERSION mismatch")
            self.need(self.edition in citation.split("title:", 1)[-1].splitlines()[0], "citation title mismatch")
        source_map = (self.base / "skill/references/source-map.md").read_text(encoding="utf-8")
        for label, path in (("English source", self.base / "README.md"),
                            ("Portuguese source", self.base / "README.pt-br.md"),
                            ("Original license", self.root / "LICENSE"),
                            ("Included license", self.base / "skill/LICENSE.txt")):
            expected = hashlib.sha256(path.read_bytes()).hexdigest()
            found = re.search(re.escape(label) + r" SHA-256:\*\*\s+\x60([0-9a-f]{64})\x60", source_map)
            self.need(found is not None and found.group(1) == expected, f"skill source hash mismatch: {label}")

    def run(self):
        self.need(self.base.is_dir(), f"missing edition: {self.edition}")
        for project in PROJECTS:
            try:
                self.project(project)
            except (OSError, ValueError, KeyError, TypeError, StopIteration) as error:
                self.errors.append(f"{project}: malformed declaration: {error}")
        self.documents()
        self.metadata()
        return {"edition": self.edition, "status": "failed" if self.errors else "passed",
                "counts": dict(self.counts), "errors": self.errors,
                "scope": "Selected edition's explicit file/symbol references, models, versions, case/criterion mappings, origins and local document links; Alpha operational README links included; historical linked targets checked for existence only.",
                "limits": "No prose/code semantics, scenario sufficiency, universal correctness, browser execution or transformer certification."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--edition", required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.-]*", args.edition):
        parser.error("edition must be a directory name")
    report = Checker(ROOT, args.edition).run()
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8", newline="\n")
    if report["errors"]:
        print("\n".join(report["errors"]), file=sys.stderr)
        return 1
    print(f"Structure OK: {report['counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
