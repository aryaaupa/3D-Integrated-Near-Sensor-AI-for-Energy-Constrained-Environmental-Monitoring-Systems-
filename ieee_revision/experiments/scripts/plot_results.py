#!/usr/bin/env python3
"""Generate publication figures exclusively from processed CSV files."""

from __future__ import annotations

import csv
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/timeloop-matplotlib-cache")

import matplotlib.pyplot as plt
import numpy as np


EXP = Path(__file__).resolve().parents[1]
PROCESSED = EXP / "processed"
FIGURES = EXP / "figures"
LABELS = {
    "alexnet_conv1_activation_intensive": "AlexNet CONV1\nactivation-intensive",
    "alexnet_conv2_compute_intensive": "AlexNet CONV2\ncompute-intensive",
    "planar": "Planar",
    "integrated_3d": "3D proxy",
}
COLORS = {"planar": "#4472C4", "integrated_3d": "#ED7D31"}


def read_csv(name):
    with (PROCESSED / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


def save(fig, name):
    fig.savefig(FIGURES / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIGURES / f"{name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    FIGURES.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.size": 9,
        "axes.labelsize": 9,
        "axes.titlesize": 10,
        "legend.fontsize": 8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
    rows = read_csv("results.csv")
    workloads = ["alexnet_conv1_activation_intensive", "alexnet_conv2_compute_intensive"]
    architectures = ["planar", "integrated_3d"]

    ordered = [next(r for r in rows if r["workload"] == w and r["architecture"] == a) for w in workloads for a in architectures]
    xlabels = [f"{LABELS[r['workload']]}\n{LABELS[r['architecture']]}" for r in ordered]
    x = np.arange(len(ordered))
    compute = np.array([float(r["compute_energy_pJ"]) / 1e6 for r in ordered])
    local = np.array([float(r["SRAM_or_local_buffer_energy_pJ"]) / 1e6 for r in ordered])
    top = np.array([float(r["DRAM_or_highest_level_energy_pJ"]) / 1e6 for r in ordered])
    total = np.array([float(r["total_energy_pJ"]) / 1e6 for r in ordered])
    residual = np.maximum(0, total - compute - local - top)
    fig, ax = plt.subplots(figsize=(7.2, 3.7))
    ax.bar(x, compute, label="Compute", color="#4C78A8")
    ax.bar(x, local, bottom=compute, label="On-chip buffers", color="#72B7B2")
    ax.bar(x, top, bottom=compute + local, label="DRAM / stacked SRAM", color="#F58518")
    ax.bar(x, residual, bottom=compute + local + top, label="Other/rounding", color="#BAB0AC")
    ax.set_ylabel("Energy (µJ)")
    ax.set_title("Timeloop/Accelergy energy breakdown")
    ax.set_xticks(x, xlabels)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.16))
    save(fig, "energy_breakdown")

    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    width = 0.34
    for index, architecture in enumerate(architectures):
        values = [float(next(r for r in rows if r["workload"] == w and r["architecture"] == architecture)["total_energy_pJ"]) / 1e6 for w in workloads]
        ax.bar(np.arange(2) + (index - 0.5) * width, values, width, label=LABELS[architecture], color=COLORS[architecture])
    ax.set_xticks(np.arange(2), [LABELS[w] for w in workloads])
    ax.set_ylabel("Total energy (µJ)")
    ax.set_title("Absolute total energy")
    ax.grid(axis="y", alpha=0.25)
    ax.legend()
    save(fig, "total_energy_comparison")

    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    for index, architecture in enumerate(architectures):
        values = [
            int(next(r for r in rows if r["workload"] == w and r["architecture"] == architecture)["external_DRAM_reads"])
            + int(next(r for r in rows if r["workload"] == w and r["architecture"] == architecture)["external_DRAM_writes"])
            for w in workloads
        ]
        ax.bar(np.arange(2) + (index - 0.5) * width, values, width, label=LABELS[architecture], color=COLORS[architecture])
    ax.set_xticks(np.arange(2), [LABELS[w] for w in workloads])
    ax.set_ylabel("External DRAM scalar accesses")
    ax.set_title("High-cost external-memory traffic")
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.grid(axis="y", alpha=0.25)
    ax.legend()
    save(fig, "memory_access_comparison")

    sensitivity = read_csv("sensitivity.csv")
    capacity = np.array([float(r["localized_memory_capacity_MiB"]) for r in sensitivity])
    improvement = np.array([float(r["total_energy_reduction_percent"]) for r in sensitivity])
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(capacity, improvement, marker="o", linewidth=1.8, color="#ED7D31")
    ax.set_xlabel("Localized stacked-memory capacity (MiB)")
    ax.set_ylabel("Total energy reduction vs planar (%)")
    ax.set_title("3D-proxy capacity sensitivity (AlexNet CONV1)")
    ax.set_xticks(capacity)
    ax.grid(alpha=0.3)
    save(fig, "sensitivity")


if __name__ == "__main__":
    main()
