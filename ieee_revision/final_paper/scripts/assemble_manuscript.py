#!/usr/bin/env python3
"""Assemble modular manuscript files and a Word-template-friendly text copy."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SECTIONS = [
    "ABSTRACT.md",
    "SECTION_I_INTRODUCTION.md",
    "SECTION_II_RELATED_WORK.md",
    "SECTION_III_ARCHITECTURE.md",
    "SECTION_IV_METHODOLOGY.md",
    "SECTION_V_RESULTS.md",
    "SECTION_VI_PHYSICAL_THERMAL.md",
    "SECTION_VII_DISCUSSION.md",
    "SECTION_VIII_CONCLUSION.md",
]


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8").strip()


def markdown_header() -> str:
    return """# 3D-Integrated Near-Sensor AI for Energy-Constrained Environmental Monitoring Systems

ARYA UPADHYAY, Member, IEEE

Department of Electrical and Computer Engineering, The University of Texas at Austin, Austin, TX 78712 USA

Corresponding author: Arya Upadhyay (e-mail: arya.upadhyay@utexas.edu).
"""


def assemble_markdown() -> str:
    parts = [markdown_header(), read("ABSTRACT.md")]
    parts.append("# Index Terms\n\nThree-dimensional integration, edge artificial intelligence, near-sensor computing, memory hierarchy, data movement, Timeloop, Accelergy, CACTI, ngspice, thermal co-design.")
    parts.extend(read(name) for name in SECTIONS[1:])
    parts.append(read("TABLES.md"))
    parts.append(read("REFERENCES_IEEE.md"))
    return "\n\n".join(parts).strip() + "\n"


def table_to_tsv(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        if re.match(r"^\|(?:\s*:?-+:?\s*\|)+$", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        out.append("\t".join(cells))
    return out


def to_plain(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    table: list[str] = []

    def flush_table() -> None:
        nonlocal table
        if table:
            out.extend(table_to_tsv(table))
            table = []

    equation_lines = {
        r"N_{\mathrm{MAC}} = P Q K C R S,": "N_MAC = P × Q × K × C × R × S,",
        r"I_{\mathrm{tensor}} = \frac{N_{\mathrm{MAC}}}{N_W + N_I + N_O},": "I_tensor = N_MAC / (N_W + N_I + N_O),",
        r"E_{\mathrm{total}}(w) = \sum_i \sum_a N_{i,a}(w)\,\epsilon_{i,a},": "E_total(w) = Σ_i Σ_a N_i,a(w) × ε_i,a,",
        r"\Delta E(w) = 100\frac{E_{\mathrm{planar}}(w)-E_{\mathrm{local}}(w)}{E_{\mathrm{planar}}(w)}.": "ΔE(w) = 100 × [E_planar(w) − E_local(w)] / E_planar(w).",
        r"E_{\mathrm{cycle}} = \left|\int_{1.05\,\mathrm{ns}}^{2.05\,\mathrm{ns}} V_{DD} I_{DD}(t)\,dt\right|.": "E_cycle = |∫ from 1.05 ns to 2.05 ns of V_DD × I_DD(t) dt|.",
        r"t_{pd}=\frac{t_{pLH}+t_{pHL}}{2}.": "t_pd = (t_pLH + t_pHL) / 2.",
    }

    for line in lines:
        if line.startswith("|") and line.endswith("|"):
            table.append(line)
            continue
        flush_table()
        if line.startswith("#"):
            line = re.sub(r"^#+\s*", "", line)
        line = equation_lines.get(line, line)
        line = line.replace("**", "").replace("`", "")
        line = re.sub(r"(?<!\w)\*([^*]+)\*", r"\1", line)
        line = line.replace("\\[", "").replace("\\]", "")
        line = line.replace("\\(", "").replace("\\)", "")
        line = line.replace(r"E_{\mathrm{toggle}}=E_{\mathrm{cycle}}/2", "E_toggle = E_cycle / 2")
        line = line.replace(r"V_{DD}", "V_DD")
        line = line.replace("\\mathrm", "")
        line = line.replace("\\frac", "/").replace("\\sum", "Σ")
        line = line.replace("\\Delta", "Δ").replace("\\epsilon", "ε")
        line = line.replace("\\,", " ")
        out.append(line)
    flush_table()
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    markdown = assemble_markdown()
    (ROOT / "FULL_REVISED_MANUSCRIPT.md").write_text(markdown, encoding="utf-8")
    (ROOT / "COPY_PASTE_MANUSCRIPT.txt").write_text(to_plain(markdown), encoding="utf-8")


if __name__ == "__main__":
    main()
