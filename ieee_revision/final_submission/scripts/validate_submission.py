#!/usr/bin/env python3
"""Validate final submission figures, calculations, citations, and boundaries."""

from __future__ import annotations

import csv
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "figure_data"
MANUSCRIPT = ROOT / "01_MANUSCRIPT_FINAL.md"


def rows(name):
    with (DATA / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def main():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    arch = rows("architecture_results.csv")
    comp = {r["workload"]: r for r in rows("comparison.csv")}
    workloads = list(dict.fromkeys(r["workload"] for r in arch))
    require(len(workloads) == 5 and len(arch) == 10, "five workloads and ten architecture rows")

    for workload in workloads:
        planar = next(r for r in arch if r["workload"] == workload and r["architecture"] == "Planar")
        local = next(r for r in arch if r["workload"] == workload and r["architecture"] == "Localized")
        reduction = 100 * (float(planar["total_energy_uJ"]) - float(local["total_energy_uJ"])) / float(planar["total_energy_uJ"])
        require(math.isclose(reduction, float(comp[workload]["energy_reduction_percent"]), abs_tol=1e-7),
                f"{workload} energy reduction formula")
        require(planar["cycles"] == local["cycles"], f"{workload} paired cycles")
        require(planar["utilization"] == local["utilization"], f"{workload} paired utilization")
        require(planar["total_macs"] == local["total_macs"], f"{workload} paired MAC count")
        require(float(planar["total_energy_uJ"]) >= 0 and float(local["total_energy_uJ"]) >= 0,
                f"{workload} nonnegative energy")
        require(0 <= float(planar["utilization"]) <= 1, f"{workload} utilization bound")

    sensitivity = rows("capacity_sensitivity.csv")
    require(len(sensitivity) == 4, "four capacity-sensitivity points")
    for row in sensitivity:
        expected = 100 * (float(row["planar_energy_uJ"]) - float(row["total_energy_uJ"])) / float(row["planar_energy_uJ"])
        require(math.isclose(expected, float(row["energy_reduction_percent"]), abs_tol=1e-7),
                f"{row['capacity_MiB']} MiB sensitivity formula")

    link = rows("link_results.csv")
    require(len(link) == 5, "five link-capacitance points")
    ordered = sorted(link, key=lambda r: float(r["capacitance_fF"]))
    require(all(float(a["energy_per_toggle_fJ"]) < float(b["energy_per_toggle_fJ"]) for a, b in zip(ordered, ordered[1:])),
            "monotonic link energy over evaluated capacitances")
    require(all(float(a["mean_delay_ps"]) < float(b["mean_delay_ps"]) for a, b in zip(ordered, ordered[1:])),
            "monotonic link delay over evaluated capacitances")
    vertical = next(r for r in link if r["role"] == "vertical_reference")
    planar = next(r for r in link if r["role"] == "planar_proxy")
    er = 100 * (float(planar["energy_per_toggle_fJ"]) - float(vertical["energy_per_toggle_fJ"])) / float(planar["energy_per_toggle_fJ"])
    dr = 100 * (float(planar["mean_delay_ps"]) - float(vertical["mean_delay_ps"])) / float(planar["mean_delay_ps"])
    require(math.isclose(er, 63.7672925677, abs_tol=1e-8), "nominal link-energy reduction")
    require(math.isclose(dr, 46.3758882922, abs_tol=1e-8), "nominal link-delay reduction")

    main_stems = ["fig1_architecture", "fig2_controlled_comparison", "fig3_methodology",
                  "fig4_five_workload_energy", "fig5_capacity_sensitivity",
                  "fig6_link_energy", "fig7_link_delay"]
    supp_stems = ["figS1_intensity_vs_reduction", "figS2_energy_per_compute",
                  "figS3_component_energy", "figS4_external_dram_actions"]
    for directory, stems in ((ROOT / "figures/main", main_stems), (ROOT / "figures/supplementary", supp_stems)):
        for stem in stems:
            for suffix in ("pdf", "svg", "png"):
                path = directory / f"{stem}.{suffix}"
                require(path.is_file() and path.stat().st_size > 5000, f"nonempty figure {path.relative_to(ROOT)}")

    references = set(int(n) for n in re.findall(r"^\[(\d+)\]", manuscript, flags=re.MULTILINE))
    citations = set()
    body = manuscript.split("## References", 1)[0]
    for group in re.findall(r"\[(\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)\]", body):
        for part in re.split(r",\s*", group):
            if "-" in part:
                a, b = map(int, part.split("-")); citations.update(range(a, b + 1))
            else:
                citations.add(int(part))
    require(references == set(range(1, 19)), "references are unique and contiguous [1]-[18]")
    require(citations == references, "every reference is cited and every citation resolves")

    require(manuscript.count("**Fig. ") == 7, "seven main figure captions")
    require(manuscript.count("**TABLE ") == 5, "five main tables")
    require("AlexNet CONV2 |" not in manuscript, "CONV2 is not mislabeled as canonical")
    require("AlexNet CONV4 |" not in manuscript, "CONV4 is not mislabeled as canonical")
    require("AlexNet CONV5 |" not in manuscript, "CONV5 is not mislabeled as canonical")

    prohibited_positive = [
        r"demonstrat(?:e|es|ed) thermal improvement",
        r"higher PE utilization",
        r"inference speedup",
        r"post-layout validation",
        r"fabricated silicon results",
        r"accuracy improvement",
        r"thermal uniformity improvement",
        r"60-80%",
        r"45-70%",
    ]
    for pattern in prohibited_positive:
        require(not re.search(pattern, manuscript, flags=re.IGNORECASE), f"unsupported phrase absent: {pattern}")

    require("No co-simulation" not in manuscript, "no misleading co-simulation label")
    require("not co-simulated" in manuscript, "independent evaluation boundary stated")
    require("no sensing-accuracy-versus-temperature" not in manuscript.lower(), "temperature boundary uses scientific prose")

    required_files = [
        "01_MANUSCRIPT_FINAL.md", "02_MANUSCRIPT_COPY_PASTE.txt",
        "03_RESPONSE_TO_REVIEWERS_FINAL.md", "04_SUPPLEMENTARY_MATERIAL.md",
        "05_CLAIM_AUDIT_FINAL.md", "06_REFERENCES_FINAL.md",
        "07_REFERENCE_AUDIT_FINAL.md", "08_FIGURE_CAPTIONS_FINAL.md",
        "09_TABLES_FINAL.md", "10_CHANGELOG_FROM_PRIOR_REVISION.md",
        "11_SUBMISSION_CHECKLIST.md", "12_README.md",
        "MANUSCRIPT_FINAL_CLEAN.md", "MANUSCRIPT_FINAL_MARKED.md",
    ]
    for name in required_files:
        require((ROOT / name).is_file() and (ROOT / name).stat().st_size > 100,
                f"required package file {name}")

    print("FINAL_SUBMISSION_VALIDATION=PASS")


if __name__ == "__main__":
    main()
