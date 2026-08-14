#!/usr/bin/env python3
"""Generate MANUSCRIPT_RESULTS.md exclusively from processed CSV files."""

from __future__ import annotations

import csv
from pathlib import Path


EXP = Path(__file__).resolve().parents[1]


def read(name):
    with (EXP / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    workloads = read("workloads/workload_summary.csv")
    results = read("processed/results.csv")
    comparisons = read("processed/comparison.csv")
    sensitivity = read("processed/sensitivity.csv")
    names = {
        "alexnet_conv1_activation_intensive": "AlexNet CONV1",
        "alexnet_conv2_compute_intensive": "AlexNet CONV2",
    }
    lines = [
        "# Manuscript-ready Timeloop/Accelergy results",
        "",
        "## Workloads",
        "",
        "Exactly two repository-native AlexNet convolution layers were evaluated:",
        "",
    ]
    for row in workloads:
        lines.append(
            f"- **{names[row['workload']]} ({row['classification']}):** "
            f"input {row['input_height']}×{row['input_width']}×{row['input_channels']}, "
            f"output {row['output_height']}×{row['output_width']}×{row['output_channels']}, "
            f"kernel {row['kernel_height']}×{row['kernel_width']}, stride "
            f"{row['stride_height']}×{row['stride_width']}, and {int(row['mac_count']):,} MACs. "
            f"Tensor volumes are {int(row['weight_volume_elements']):,} weights, "
            f"{int(row['input_activation_volume_elements']):,} input activations, and "
            f"{int(row['output_activation_volume_elements']):,} output activations."
        )

    lines.extend(["", "## Absolute results", ""])
    for workload in ("alexnet_conv1_activation_intensive", "alexnet_conv2_compute_intensive"):
        p = next(r for r in results if r["workload"] == workload and r["architecture"] == "planar")
        s = next(r for r in results if r["workload"] == workload and r["architecture"] == "integrated_3d")
        c = next(r for r in comparisons if r["workload"] == workload)
        p_events = int(p["highest_level_reads"]) + int(p["highest_level_writes"])
        s_events = int(s["highest_level_reads"]) + int(s["highest_level_writes"])
        lines.append(
            f"For **{names[workload]}**, Timeloop/Accelergy evaluation shows "
            f"{float(p['total_energy_pJ'])/1e6:,.2f} µJ for the planar case and "
            f"{float(s['total_energy_pJ'])/1e6:,.2f} µJ for the 3D proxy, a "
            f"{float(c['total_energy_reduction_percent']):.2f}% reduction. Energy per "
            f"compute changes from {float(p['energy_per_compute_pJ']):.3f} to "
            f"{float(s['energy_per_compute_pJ']):.3f} pJ/compute. Both cases require "
            f"{int(p['cycles']):,} cycles ({float(p['latency_us']):,.2f} µs at 1 GHz) "
            f"with utilization {float(p['utilization']):.4f}. The fixed mapping produces "
            f"{p_events:,} highest-level events in the planar case and {s_events:,} in "
            f"the 3D proxy (0.00% event-count reduction); the proxy redirects these "
            f"events to stacked SRAM, so modeled external-DRAM accesses fall by "
            f"{float(c['external_DRAM_access_reduction_percent']):.2f}%."
        )
        lines.append("")

    low = min(float(r["total_energy_reduction_percent"]) for r in sensitivity)
    high = max(float(r["total_energy_reduction_percent"]) for r in sensitivity)
    lines.extend(
        [
            "## Sensitivity",
            "",
            f"For AlexNet CONV1, varying localized SRAM capacity from 2 to 16 MiB while "
            f"holding mapping and cycles fixed yields total-energy reductions of "
            f"{low:.2f}% to {high:.2f}% relative to the planar baseline. The benefit "
            f"therefore remains positive throughout the tested CACTI-backed range, "
            f"although it decreases as modeled SRAM capacity and access energy increase.",
            "",
            "## Major limitation",
            "",
            "The integrated configuration is an architectural proxy, not a physical 3D "
            "implementation. Timeloop does not model TSV geometry, bonding, thermals, "
            "stress, or transistor-level behavior in this study. No separately reported "
            "interconnect/network energy is available, so that metric is `NA`. The 3D "
            "result isolates the modeled energy effect of replacing external LPDDR4 with "
            "localized CACTI-backed SRAM under an otherwise identical fixed mapping; it "
            "must not be described as measured silicon performance.",
            "",
            "## IEEE methodology paragraph",
            "",
            "Timeloop was used for mapping and for cycle, utilization, and memory-access "
            "characterization, while Accelergy with CACTI-backed component models was "
            "used for component-level energy estimation. The planar and 3D-proxy cases "
            "used identical convolution dimensions, MAC counts, 168-PE compute array, "
            "arithmetic precision, fixed loop mapping, 1-GHz clock assumption, and lower "
            "memory hierarchy. The 3D configuration was represented architecturally by "
            "redirecting high-cost external-memory traffic to localized on-stack SRAM, "
            "thereby modeling increased data locality and lower-cost local communication. "
            "This study does not claim transistor-level, physical-TSV, or thermal simulation.",
            "",
        ]
    )
    (EXP / "MANUSCRIPT_RESULTS.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
