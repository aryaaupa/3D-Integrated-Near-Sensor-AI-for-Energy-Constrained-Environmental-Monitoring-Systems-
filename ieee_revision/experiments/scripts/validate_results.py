#!/usr/bin/env python3
"""Validate raw runs, fairness invariants, CSV formulas, and traceability."""

from __future__ import annotations

import csv
import copy
import json
import math
import re
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[3]
EXP = Path(__file__).resolve().parents[1]
WORKLOADS = ("alexnet_conv1_activation_intensive", "alexnet_conv2_compute_intensive")
REQUIRED = (
    "timeloop-model.stats.txt",
    "timeloop-model.map.txt",
    "timeloop-model.map+stats.xml",
    "timeloop-model.ERT.yaml",
    "timeloop-model.ART.yaml",
    "timeloop-model.accelergy.log",
    "stdout_stderr.txt",
    "input.yaml",
)


def load_csv(name: str) -> list[dict]:
    with (EXP / "processed" / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


def normalized_mapping(doc: dict) -> list[dict]:
    result = json.loads(json.dumps(doc["mapping"]))
    for entry in result:
        if entry.get("target") == "stacked_sram":
            entry["target"] = "DRAM"
    return result


def find_component(doc: dict, prefix: str) -> dict:
    return next(
        component
        for component in doc["architecture"]["subtree"][0]["local"]
        if str(component["name"]).startswith(prefix)
    )


def architecture_without_top(doc: dict) -> dict:
    architecture = copy.deepcopy(doc["architecture"])
    local = architecture["subtree"][0]["local"]
    architecture["subtree"][0]["local"] = [
        component
        for component in local
        if not str(component["name"]).startswith(("DRAM[", "stacked_sram["))
    ]
    return architecture


def approx(a: float, b: float, tolerance: float = 1e-7) -> bool:
    return math.isclose(a, b, rel_tol=tolerance, abs_tol=tolerance)


def main() -> None:
    checks = []
    results = load_csv("results.csv")
    comparisons = load_csv("comparison.csv")
    traceability = load_csv("traceability.csv")
    assert len(results) == 4
    assert len(traceability) == 16 * 4

    for workload in WORKLOADS:
        docs = {}
        rows = {}
        for architecture in ("planar", "integrated_3d"):
            run_dir = EXP / "raw_outputs" / workload / architecture
            for filename in REQUIRED:
                path = run_dir / filename
                assert path.is_file() and path.stat().st_size > 0, path
            assert "EXIT_STATUS=0" in (run_dir / "stdout_stderr.txt").read_text()
            error_text = (
                (run_dir / "stdout_stderr.txt").read_text()
                + (run_dir / "timeloop-model.accelergy.log").read_text()
            )
            assert not re.search(
                r"encountered an error|failed to run accelergy|traceback|(^|\s)error([:\s]|$)",
                error_text,
                re.IGNORECASE | re.MULTILINE,
            )
            docs[architecture] = yaml.safe_load((run_dir / "input.yaml").read_text())
            rows[architecture] = next(
                row for row in results if row["workload"] == workload and row["architecture"] == architecture
            )
            for field in (
                "total_energy_pJ",
                "energy_per_compute_pJ",
                "DRAM_or_highest_level_energy_pJ",
                "SRAM_or_local_buffer_energy_pJ",
                "compute_energy_pJ",
            ):
                assert float(rows[architecture][field]) >= 0
            assert 0 <= float(rows[architecture]["utilization"]) <= 1

        assert docs["planar"]["problem"] == docs["integrated_3d"]["problem"]
        assert normalized_mapping(docs["planar"]) == normalized_mapping(docs["integrated_3d"])
        assert architecture_without_top(docs["planar"]) == architecture_without_top(docs["integrated_3d"])
        assert find_component(docs["planar"], "mac[") == find_component(docs["integrated_3d"], "mac[")
        assert int(rows["planar"]["total_MACs"]) == int(rows["integrated_3d"]["total_MACs"])
        assert int(rows["planar"]["cycles"]) == int(rows["integrated_3d"]["cycles"])
        assert approx(float(rows["planar"]["utilization"]), float(rows["integrated_3d"]["utilization"]))
        checks.append(f"PASS {workload}: identical problem, mapping, MAC, compute, cycles, utilization")

        comp = next(row for row in comparisons if row["workload"] == workload)
        p = rows["planar"]
        s = rows["integrated_3d"]
        formulas = {
            "total_energy_reduction_percent": (float(p["total_energy_pJ"]) - float(s["total_energy_pJ"])) / float(p["total_energy_pJ"]) * 100,
            "cycle_reduction_percent": (float(p["cycles"]) - float(s["cycles"])) / float(p["cycles"]) * 100,
            "latency_reduction_percent": (float(p["latency_us"]) - float(s["latency_us"])) / float(p["latency_us"]) * 100,
            "energy_per_compute_reduction_percent": (float(p["energy_per_compute_pJ"]) - float(s["energy_per_compute_pJ"])) / float(p["energy_per_compute_pJ"]) * 100,
            "highest_level_memory_access_reduction_percent": (
                (int(p["highest_level_reads"]) + int(p["highest_level_writes"]))
                - (int(s["highest_level_reads"]) + int(s["highest_level_writes"]))
            ) / (int(p["highest_level_reads"]) + int(p["highest_level_writes"])) * 100,
            "external_DRAM_access_reduction_percent": (
                (int(p["external_DRAM_reads"]) + int(p["external_DRAM_writes"]))
                - (int(s["external_DRAM_reads"]) + int(s["external_DRAM_writes"]))
            ) / (int(p["external_DRAM_reads"]) + int(p["external_DRAM_writes"])) * 100,
        }
        for field, expected in formulas.items():
            assert approx(float(comp[field]), expected, 1e-6), (field, comp[field], expected)
        checks.append(f"PASS {workload}: comparison formulas recomputed consistently")

    sources = {row["raw_source_file"].split("; ")[0] for row in traceability}
    for source in sources:
        assert (REPO / source).is_file(), source
    checks.append("PASS traceability: every listed raw source file exists")

    for capacity in ("2MiB", "4MiB", "8MiB", "16MiB"):
        run_dir = EXP / "raw_outputs/sensitivity" / WORKLOADS[0] / capacity
        for filename in REQUIRED:
            path = run_dir / filename
            assert path.is_file() and path.stat().st_size > 0, path
        combined = (
            (run_dir / "stdout_stderr.txt").read_text()
            + (run_dir / "timeloop-model.accelergy.log").read_text()
        )
        assert "EXIT_STATUS=0" in combined
        assert not re.search(
            r"encountered an error|failed to run accelergy|traceback|(^|\s)error([:\s]|$)",
            combined,
            re.IGNORECASE | re.MULTILINE,
        )
    checks.append("PASS sensitivity: four capacity runs have complete, error-free raw artifacts")
    checks.append("PASS all four main runs and all four sensitivity runs exited successfully")
    output = EXP / "processed/validation_report.txt"
    output.write_text("\n".join(checks) + "\nFINAL_VALIDATION=PASS\n")
    print(output.read_text(), end="")


if __name__ == "__main__":
    main()
