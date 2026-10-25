#!/usr/bin/env python3
"""Render both LaTeX editions from the complete bilingual UCS JSON."""
from __future__ import annotations

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "ucs.json"

LABELS = {
    "en": {
        "purpose": "Purpose and scope", "scope": "Scope", "actors": "Participants",
        "needs": "Needs", "assumptions": "Assumptions", "out_of_scope": "Outside this baseline",
        "entities": "Entities and validity", "rules": "Shared business rules",
        "capabilities": "Required capabilities",
        "use_cases": "Use-case contracts", "quality": "Complementary obligations",
        "glossary": "Glossary", "evolution": "Evolution",
        "objective": "Objective", "trigger": "Trigger", "inputs": "Inputs",
        "preconditions": "Assumed conditions", "main_flow": "Main flow",
        "alternatives": "Alternatives and failures", "results": "Results",
        "effects": "Effects", "guarantees": "Guarantees",
        "dependencies": "Required capabilities", "needs_refs": "Needs",
        "rule_refs": "Rules", "entity_refs": "Entities", "criteria": "Acceptance criteria",
        "validity": "Validity", "status": "Status", "edition": "OAL edition",
        "permitted_actors": "Permitted actors",
        "spec_version": "Project specification version", "source": "Reference language",
    },
    "pt-BR": {
        "purpose": "Objetivo e escopo", "scope": "Escopo", "actors": "Participantes",
        "needs": "Necessidades", "assumptions": "Premissas", "out_of_scope": "Fora desta baseline",
        "entities": "Entidades e validade", "rules": "Regras de negócio compartilhadas",
        "capabilities": "Capacidades exigidas",
        "use_cases": "Contratos dos casos de uso", "quality": "Obrigações complementares",
        "glossary": "Glossário", "evolution": "Evolução",
        "objective": "Objetivo", "trigger": "Acionamento", "inputs": "Entradas",
        "preconditions": "Condições assumidas", "main_flow": "Fluxo principal",
        "alternatives": "Alternativas e falhas", "results": "Resultados",
        "effects": "Efeitos", "guarantees": "Garantias",
        "dependencies": "Capacidades exigidas", "needs_refs": "Necessidades",
        "rule_refs": "Regras", "entity_refs": "Entidades", "criteria": "Critérios de aceitação",
        "validity": "Validade", "status": "Status", "edition": "Edição OAL",
        "permitted_actors": "Atores permitidos",
        "spec_version": "Versão da especificação do projeto", "source": "Idioma de referência",
    },
}


def esc(value: object) -> str:
    escapes = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
        "$": r"\$", "#": r"\#", "_": r"\_",
        "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}", "—": "---", "–": "--",
        "↔": r"\(\leftrightarrow\)",
    }
    return "".join(escapes.get(char, char) for char in str(value))


def render(data: dict, lang: str) -> str:
    label = LABELS[lang]
    lines = [
        r"\documentclass[10pt,a4paper]{article}",
        r"\usepackage[margin=22mm]{geometry}",
        r"\usepackage{fontspec}",
        r"\setmainfont{Arial}",
        r"\usepackage{unicode-math}",
        r"\setmathfont{Cambria Math}",
        r"\usepackage{hyperref}",
        r"\setlength{\parskip}{5pt}",
        r"\setlength{\parindent}{0pt}",
        r"\begin{document}",
        rf"\title{{{esc(data['title'][lang])}}}",
        r"\author{" + r" \and ".join(esc(author) for author in data["authors"]) + "}",
        rf"\date{{OAL {esc(data['oal_edition'])} \quad {esc(label['spec_version'])}: {esc(data['project_specification_version'])}}}",
        r"\maketitle",
        rf"\textbf{{{esc(label['status'])}:}} {esc(data['status'][lang])}",
        rf"\textbf{{{esc(label['source'])}:}} {esc(data['reference_language'])}",
    ]

    def section(title: str) -> None:
        lines.append(rf"\section{{{esc(title)}}}")

    def subsection(title: str) -> None:
        lines.append(rf"\subsection{{{esc(title)}}}")

    def entries(items: list[dict]) -> None:
        lines.append(r"\begin{itemize}")
        for entry in items:
            lines.append(rf"\item \textbf{{{esc(entry['id'])}.}} {esc(entry['text'][lang])}")
        lines.append(r"\end{itemize}")

    section(label["purpose"])
    lines.append(esc(data["purpose"][lang]))
    subsection(label["scope"]); entries(data["scope"])
    subsection(label["actors"])
    for actor in data["actors"]:
        lines.append(rf"\textbf{{{esc(actor['id'])} --- {esc(actor['name'][lang])}.}} {esc(actor['description'][lang])}")
    subsection(label["needs"]); entries(data["needs"])
    subsection(label["assumptions"]); entries(data["assumptions"])
    subsection(label["out_of_scope"]); entries(data["out_of_scope"])

    section(label["entities"])
    for entity in data["entities"]:
        subsection(entity["id"] + " -- " + entity["name"][lang])
        lines.append(esc(entity["description"][lang]))
        lines.append(rf"\textbf{{{esc(label['validity'])}:}} {esc(entity['validity'][lang])}")

    section(label["rules"]); entries(data["rules"])
    section(label["capabilities"]); entries(data["capabilities"])
    section(label["use_cases"])
    for uc in data["use_cases"]:
        subsection(uc["id"] + " -- " + uc["title"][lang])
        lines.append(rf"\textbf{{{esc(label['objective'])}:}} {esc(uc['objective'][lang])}")
        lines.append(rf"\textbf{{{esc(label['trigger'])}:}} {esc(uc['trigger'][lang])}")
        lines.append(rf"\textbf{{{esc(label['actors'])}:}} {esc(uc['actor'])}")
        lines.append(rf"\textbf{{{esc(label['permitted_actors'])}:}} {esc(', '.join(uc['permitted_actors']))}")
        for field in ["inputs", "preconditions", "main_flow", "alternatives", "results", "effects", "guarantees"]:
            lines.append(rf"\paragraph{{{esc(label[field])}}}")
            entries(uc[field])
        for field, values in [("dependencies", uc["dependencies"]), ("needs_refs", uc["needs"]),
                              ("rule_refs", uc["rules"]), ("entity_refs", uc["entities"])]:
            lines.append(rf"\textbf{{{esc(label[field])}:}} {esc(', '.join(values))}")
        lines.append(rf"\paragraph{{{esc(label['criteria'])}}}")
        entries(uc["criteria"])

    section(label["quality"]); entries(data["quality_obligations"])
    section(label["glossary"])
    for entry in data["glossary"]:
        lines.append(rf"\textbf{{{esc(entry['term'][lang])}.}} {esc(entry['meaning'][lang])}")
    section(label["evolution"])
    lines.append(esc(data["evolution"][lang]))
    lines.append(r"\end{document}")
    return "\n\n".join(lines) + "\n"


def main() -> int:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    expected = {"en", "pt-BR"}
    if set(data["languages"]) != expected:
        raise ValueError("Expected English and Brazilian Portuguese content")
    for lang, filename in [("en", "UCS.tex"), ("pt-BR", "UCS.pt-br.tex")]:
        text = render(data, lang)
        path = HERE / filename
        if "--check" in sys.argv:
            if not path.is_file() or path.read_text(encoding="utf-8") != text:
                raise ValueError(f"Out-of-date LaTeX: {filename}")
        else:
            path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
