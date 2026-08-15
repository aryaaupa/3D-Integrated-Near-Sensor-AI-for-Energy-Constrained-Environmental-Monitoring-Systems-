#!/usr/bin/env python3
"""Parse Timeloop stats into results, comparisons, sensitivity, and traceability CSVs."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
EXP = Path(__file__).resolve().parents[1]
PROCESSED = EXP / "processed"
WORKLOADS = (
    "alexnet_conv1_activation_intensive",
    "alexnet_conv2_compute_intensive",
)
ARCHITECTURES = ("planar", "integrated_3d")
LOCAL_COMPONENTS = ("shared_glb", "ifmap_spad", "weights_spad", "psum_spad")
RESULT_FIELDS = (
    "workload",
    "architecture",
    "total_energy_pJ",
    "energy_per_compute_pJ",
    "cycles",
    "utilization",
    "DRAM_or_highest_level_energy_pJ",
    "SRAM_or_local_buffer_energy_pJ",
    "compute_energy_pJ",
    "interconnect_or_network_energy_pJ",
    "highest_level_reads",
    "highest_level_writes",
    "local_memory_reads",
    "local_memory_writes",
    "total_MACs",
    "latency_us",
    "external_DRAM_reads",
    "external_DRAM_writes",
)


def number(value: str) -> float:
    return float(value.replace(",", ""))


def parse_stats(path: Path) -> dict:
    components = defaultdict(lambda: {"energy": 0.0, "reads": 0, "writes": 0})
    current = None
    total_energy_pj = None
    energy_per_compute_pj = None
    cycles = None
    utilization = None
    macs = None
    in_fj_table = False

    for line in path.read_text().splitlines():
        heading = re.match(r"^=== (.+) ===$", line)
        if heading:
            current = heading.group(1)
            continue
        if line in ("Networks", "Operational Intensity Stats", "Summary Stats"):
            current = None
        if current:
            match = re.match(r"^\s*Leakage energy \(total\)\s*:\s*([0-9.eE+-]+) pJ$", line)
            if match:
                components[current]["energy"] += number(match.group(1))
                continue
            match = re.match(r"^\s*Energy \(total\)\s*:\s*([0-9.eE+-]+) pJ$", line)
            if match:
                components[current]["energy"] += number(match.group(1))
                continue
            match = re.match(r"^\s*Scalar reads \(per-instance\)\s*:\s*(\d+)$", line)
            if match:
                components[current]["reads"] += int(match.group(1))
                continue
            match = re.match(r"^\s*Scalar fills \(per-instance\)\s*:\s*(\d+)$", line)
            if match:
                components[current]["writes"] += int(match.group(1))
                continue
            match = re.match(r"^\s*Scalar updates \(per-instance\)\s*:\s*(\d+)$", line)
            if match:
                components[current]["writes"] += int(match.group(1))
                continue

        match = re.match(r"^Utilization:\s*([0-9.]+)%$", line)
        if match:
            utilization = number(match.group(1)) / 100.0
        match = re.match(r"^Cycles:\s*(\d+)$", line)
        if match:
            cycles = int(match.group(1))
        match = re.match(r"^Energy:\s*([0-9.eE+-]+) uJ$", line)
        if match:
            total_energy_pj = number(match.group(1)) * 1_000_000.0
        match = re.match(r"^Computes =\s*(\d+)$", line)
        if match:
            macs = int(match.group(1))
        if line == "fJ/Compute":
            in_fj_table = True
        elif in_fj_table:
            match = re.match(r"^\s*Total\s*=\s*([0-9.eE+-]+)$", line)
            if match:
                energy_per_compute_pj = number(match.group(1)) / 1000.0
                in_fj_table = False

    required = (total_energy_pj, energy_per_compute_pj, cycles, utilization, macs)
    if any(value is None for value in required):
        raise ValueError(f"Missing summary metric in {path}")
    return {
        "components": dict(components),
        "total_energy_pJ": total_energy_pj,
        "energy_per_compute_pJ": energy_per_compute_pj,
        "cycles": cycles,
        "utilization": utilization,
        "total_MACs": macs,
    }


def fmt(value):
    if isinstance(value, str):
        return value
    if isinstance(value, int):
        return str(value)
    return f"{value:.10g}"


def result_row(workload: str, architecture: str) -> tuple[dict, list[dict]]:
    run_dir = EXP / "raw_outputs" / workload / architecture
    stats_path = run_dir / "timeloop-model.stats.txt"
    parsed = parse_stats(stats_path)
    components = parsed["components"]
    top_name = "DRAM" if architecture == "planar" else "stacked_sram"
    top = components[top_name]
    local_energy = sum(components[name]["energy"] for name in LOCAL_COMPONENTS)
    local_reads = sum(components[name]["reads"] for name in LOCAL_COMPONENTS)
    local_writes = sum(components[name]["writes"] for name in LOCAL_COMPONENTS)
    if architecture == "integrated_3d":
        local_reads += top["reads"]
        local_writes += top["writes"]
    row = {
        "workload": workload,
        "architecture": architecture,
        "total_energy_pJ": parsed["total_energy_pJ"],
        "energy_per_compute_pJ": parsed["energy_per_compute_pJ"],
        "cycles": parsed["cycles"],
        "utilization": parsed["utilization"],
        "DRAM_or_highest_level_energy_pJ": top["energy"],
        "SRAM_or_local_buffer_energy_pJ": local_energy,
        "compute_energy_pJ": components["mac"]["energy"],
        "interconnect_or_network_energy_pJ": "NA",
        "highest_level_reads": top["reads"],
        "highest_level_writes": top["writes"],
        "local_memory_reads": local_reads,
        "local_memory_writes": local_writes,
        "total_MACs": parsed["total_MACs"],
        "latency_us": parsed["cycles"] / 1000.0,
        "external_DRAM_reads": top["reads"] if architecture == "planar" else 0,
        "external_DRAM_writes": top["writes"] if architecture == "planar" else 0,
    }
    source = str(stats_path.relative_to(REPO))
    input_source = str((run_dir / "input.yaml").relative_to(REPO))
    methods = {
        "total_energy_pJ": "Parse Summary Stats Energy (uJ); multiply by 1e6",
        "energy_per_compute_pJ": "Parse Total fJ/Compute; divide by 1000",
        "cycles": "Parse Summary Stats Cycles",
        "utilization": "Parse Summary Stats Utilization percent; divide by 100",
        "DRAM_or_highest_level_energy_pJ": f"Sum {top_name} leakage and per-dataspace Energy (total)",
        "SRAM_or_local_buffer_energy_pJ": "Sum leakage and Energy (total) for shared_glb and three PE scratchpads",
        "compute_energy_pJ": "Parse mac Energy (total)",
        "interconnect_or_network_energy_pJ": "NA: stats Networks section contains no separately reported energy",
        "highest_level_reads": f"Sum {top_name} Scalar reads (per-instance) across dataspaces",
        "highest_level_writes": f"Sum {top_name} Scalar fills plus Scalar updates across dataspaces",
        "local_memory_reads": "Sum local-buffer Scalar reads; 3D also includes stacked_sram reads",
        "local_memory_writes": "Sum local-buffer Scalar fills and updates; 3D also includes stacked_sram writes",
        "total_MACs": "Parse Computes from Summary Stats",
        "latency_us": "cycles * 1 ns / 1000 ns/us using input global_cycle_seconds=1e-9",
        "external_DRAM_reads": "Planar: parsed DRAM reads; 3D: deterministic zero because input has no DRAM component",
        "external_DRAM_writes": "Planar: parsed DRAM fills+updates; 3D: deterministic zero because input has no DRAM component",
    }
    trace = []
    for metric in RESULT_FIELDS[2:]:
        trace.append(
            {
                "metric": metric,
                "workload": workload,
                "architecture": architecture,
                "value": fmt(row[metric]),
                "raw_source_file": f"{source}; {input_source}" if metric == "latency_us" else source,
                "extraction_method": methods[metric],
            }
        )
    return row, trace


def reduction(planar: float, stacked: float) -> float:
    if planar == 0:
        return 0.0 if stacked == 0 else float("nan")
    return (planar - stacked) / planar * 100.0


def write_csv(path: Path, fieldnames: tuple | list, rows: list[dict]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: fmt(value) for key, value in row.items()})


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    rows = []
    traces = []
    for workload in WORKLOADS:
        for architecture in ARCHITECTURES:
            row, trace = result_row(workload, architecture)
            rows.append(row)
            traces.extend(trace)
    write_csv(PROCESSED / "results.csv", RESULT_FIELDS, rows)

    comparisons = []
    for workload in WORKLOADS:
        planar = next(r for r in rows if r["workload"] == workload and r["architecture"] == "planar")
        stacked = next(r for r in rows if r["workload"] == workload and r["architecture"] == "integrated_3d")
        planar_top = planar["highest_level_reads"] + planar["highest_level_writes"]
        stacked_top = stacked["highest_level_reads"] + stacked["highest_level_writes"]
        planar_dram = planar["external_DRAM_reads"] + planar["external_DRAM_writes"]
        stacked_dram = stacked["external_DRAM_reads"] + stacked["external_DRAM_writes"]
        comparisons.append(
            {
                "workload": workload,
                "total_energy_reduction_percent": reduction(planar["total_energy_pJ"], stacked["total_energy_pJ"]),
                "cycle_reduction_percent": reduction(planar["cycles"], stacked["cycles"]),
                "latency_reduction_percent": reduction(planar["latency_us"], stacked["latency_us"]),
                "highest_level_memory_access_reduction_percent": reduction(planar_top, stacked_top),
                "external_DRAM_access_reduction_percent": reduction(planar_dram, stacked_dram),
                "energy_per_compute_reduction_percent": reduction(planar["energy_per_compute_pJ"], stacked["energy_per_compute_pJ"]),
            }
        )
    comparison_fields = tuple(comparisons[0].keys())
    write_csv(PROCESSED / "comparison.csv", comparison_fields, comparisons)

    planar_a = next(r for r in rows if r["workload"] == WORKLOADS[0] and r["architecture"] == "planar")
    sensitivity = []
    for label, capacity in (("2MiB", 2), ("4MiB", 4), ("8MiB", 8), ("16MiB", 16)):
        path = EXP / "raw_outputs/sensitivity" / WORKLOADS[0] / label / "timeloop-model.stats.txt"
        parsed = parse_stats(path)
        sensitivity.append(
            {
                "workload": WORKLOADS[0],
                "localized_memory_capacity_MiB": capacity,
                "total_energy_pJ": parsed["total_energy_pJ"],
                "planar_total_energy_pJ": planar_a["total_energy_pJ"],
                "total_energy_reduction_percent": reduction(planar_a["total_energy_pJ"], parsed["total_energy_pJ"]),
                "cycles": parsed["cycles"],
                "raw_source_file": str(path.relative_to(REPO)),
            }
        )
    write_csv(PROCESSED / "sensitivity.csv", tuple(sensitivity[0].keys()), sensitivity)
    write_csv(
        PROCESSED / "traceability.csv",
        ("metric", "workload", "architecture", "value", "raw_source_file", "extraction_method"),
        traces,
    )


if __name__ == "__main__":
    main()
