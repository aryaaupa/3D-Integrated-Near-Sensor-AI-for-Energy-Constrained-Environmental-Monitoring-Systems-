#!/usr/bin/env python3
"""Generate all manuscript figures exclusively from committed CSV inputs."""

from __future__ import annotations

import csv
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "figure_data"
OUT = ROOT / "figures"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = "#34699A"
ORANGE = "#C97B35"
GREEN = "#4F7F6A"
GRAY = "#ECEFF2"
DARK = "#20262E"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 9,
        "legend.fontsize": 7,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def rows(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save(fig: plt.Figure, stem: str) -> None:
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def box(ax, xy, wh, title, subtitle, color=BLUE):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor="white", edgecolor=color, linewidth=1.4
    )
    ax.add_patch(patch)
    title_text = textwrap.fill(title, width=20)
    subtitle_text = textwrap.fill(subtitle, width=28)
    ax.text(x + w / 2, y + h * 0.64, title_text, ha="center", va="center",
            fontsize=7.5, fontweight="bold", color=DARK, linespacing=1.0)
    ax.text(x + w / 2, y + h * 0.27, subtitle_text, ha="center", va="center",
            fontsize=5.9, color=DARK, linespacing=1.0)


def arrow(ax, start, end, color=DARK):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=10,
                                linewidth=1.1, color=color))


def figure1():
    data = rows("figure1_architecture_nodes.csv")
    fig, ax = plt.subplots(figsize=(3.5, 4.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    colors = [GREEN, ORANGE, BLUE]
    ys = [0.70, 0.40, 0.10]
    for item, y, color in zip(data, ys, colors):
        box(ax, (0.12, y), (0.76, 0.19), item["tier"], item["role"], color)
    arrow(ax, (0.50, 0.70), (0.50, 0.61), GREEN)
    arrow(ax, (0.50, 0.40), (0.50, 0.31), ORANGE)
    ax.text(0.94, 0.50, "dense vertical\ncommunication", rotation=90,
            ha="center", va="center", color=DARK, fontsize=7)
    ax.plot([0.90, 0.90], [0.18, 0.80], color=DARK, linewidth=1.0)
    ax.set_title("Three-tier near-sensor organization", pad=4, fontweight="bold")
    save(fig, "fig1_architecture")


def figure2():
    data = rows("figure2_workflow_nodes.csv")
    fig, ax = plt.subplots(figsize=(7.0, 3.3))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    for path, y, color in [("Architecture path", 0.63, BLUE), ("Circuit path", 0.18, ORANGE)]:
        source_path = path.split()[0]
        subset = [r for r in data if r["path"] == source_path]
        ax.text(0.02, y + 0.25, path, ha="left", va="center", fontweight="bold", color=color)
        xs = [0.02, 0.265, 0.51, 0.755]
        for i, (item, x) in enumerate(zip(subset, xs)):
            short_titles = {
                "Accelergy plus CACTI": "Accelergy + CACTI",
                "Parser and validator": "Parser + validator",
                "PTM model plus link netlist": "PTM + link netlist",
                "Cross-level interpretation": "Cross-level\ninterpretation",
            }
            box(ax, (x, y), (0.205, 0.22), short_titles.get(item["node"], item["node"]), item["output"], color)
            if i < len(subset) - 1:
                arrow(ax, (x + 0.205, y + 0.11), (xs[i + 1] - 0.008, y + 0.11), color)
    arrow(ax, (0.858, 0.42), (0.858, 0.54), DARK)
    ax.text(0.50, 0.49, "Independent evidence paths; percentages are not combined",
            ha="center", va="center", fontsize=7, color=DARK)
    ax.set_title("Two-level evaluation and traceability workflow", pad=3, fontweight="bold")
    save(fig, "fig2_evaluation_workflow")


def figure3():
    data = rows("figure3_hierarchy.csv")
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    for architecture, x0, color in [("Planar", 0.06, ORANGE), ("Localized", 0.55, BLUE)]:
        subset = sorted([r for r in data if r["architecture"] == architecture], key=lambda r: int(r["level"]))
        ax.text(x0 + 0.19, 0.93, architecture, ha="center", va="center",
                fontsize=10, fontweight="bold", color=color)
        for i, item in enumerate(subset):
            y = 0.68 - i * 0.18
            box(ax, (x0, y), (0.38, 0.13), item["component"], item["placement"], color)
            if i < len(subset) - 1:
                arrow(ax, (x0 + 0.19, y), (x0 + 0.19, y - 0.055), color)
    ax.text(0.50, 0.84, "Only highest level changes", ha="center", va="center",
            fontsize=7, fontweight="bold", color=DARK)
    arrow(ax, (0.44, 0.745), (0.54, 0.745), DARK)
    ax.set_title("Controlled planar and localized-memory hierarchies", pad=3, fontweight="bold")
    save(fig, "fig3_controlled_hierarchy")


def figure4():
    data = rows("architecture_results.csv")
    fig, ax = plt.subplots(figsize=(3.5, 2.65))
    workloads = ["CONV1", "CONV2"]
    x = [0, 1]
    width = 0.34
    planar = [float(next(r["total_energy_uJ"] for r in data if r["workload"] == w and r["architecture"] == "Planar")) for w in workloads]
    local = [float(next(r["total_energy_uJ"] for r in data if r["workload"] == w and r["architecture"] == "Localized")) for w in workloads]
    ax.bar([v - width / 2 for v in x], planar, width, label="Planar", color=ORANGE)
    ax.bar([v + width / 2 for v in x], local, width, label="Localized", color=BLUE)
    ax.set_xticks(x, workloads)
    ax.set_ylabel("Total energy (µJ)")
    ax.set_ylim(0, 8000)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False)
    ax.set_title("Workload-dependent total energy", fontweight="bold")
    for i, (p, q) in enumerate(zip(planar, local)):
        ax.text(i - width / 2, p + 120, f"{p:,.0f}", ha="center", va="bottom", fontsize=6.5)
        ax.text(i + width / 2, q + 120, f"{q:,.0f}", ha="center", va="bottom", fontsize=6.5)
    save(fig, "fig4_total_energy")


def figure5():
    data = rows("architecture_results.csv")
    fig, ax = plt.subplots(figsize=(3.5, 2.65))
    workloads = ["CONV1", "CONV2"]
    x = [0, 1]
    width = 0.34
    planar = [float(next(r["energy_per_compute_pJ"] for r in data if r["workload"] == w and r["architecture"] == "Planar")) for w in workloads]
    local = [float(next(r["energy_per_compute_pJ"] for r in data if r["workload"] == w and r["architecture"] == "Localized")) for w in workloads]
    ax.bar([v - width / 2 for v in x], planar, width, label="Planar", color=ORANGE)
    ax.bar([v + width / 2 for v in x], local, width, label="Localized", color=BLUE)
    ax.set_xticks(x, workloads)
    ax.set_ylabel("Energy per compute (pJ)")
    ax.set_ylim(0, 76)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False)
    ax.set_title("Energy normalized by Timeloop computes", fontweight="bold")
    for i, (p, q) in enumerate(zip(planar, local)):
        ax.text(i - width / 2, p + 1.2, f"{p:.2f}", ha="center", va="bottom", fontsize=6.5)
        ax.text(i + width / 2, q + 1.2, f"{q:.2f}", ha="center", va="bottom", fontsize=6.5)
    save(fig, "fig5_energy_per_compute")


def figure6():
    data = rows("capacity_sensitivity.csv")
    x = [int(r["capacity_MiB"]) for r in data]
    energy = [float(r["total_energy_uJ"]) for r in data]
    reduction = [float(r["energy_reduction_percent"]) for r in data]
    fig, ax = plt.subplots(figsize=(3.5, 2.65))
    ax.plot(x, energy, marker="o", color=BLUE, linewidth=1.6)
    ax.axhline(7343.23, color=ORANGE, linestyle="--", linewidth=1.1, label="Planar baseline")
    ax.set_xscale("log", base=2)
    ax.set_xticks(x, [str(v) for v in x])
    ax.set_xlabel("Localized SRAM capacity (MiB)")
    ax.set_ylabel("CONV1 total energy (µJ)")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, loc="lower right")
    ax.set_title("Localized-memory capacity sensitivity", fontweight="bold")
    for a, b, r in zip(x, energy, reduction):
        ax.annotate(f"{r:.1f}%", (a, b), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=6.5)
    save(fig, "fig6_capacity_sensitivity")


def figure7():
    data = rows("spice_link_results.csv")
    ordered = sorted(data, key=lambda r: float(r["capacitance_fF"]))
    x = [float(r["capacitance_fF"]) for r in ordered]
    y = [float(r["energy_per_toggle_fJ"]) for r in ordered]
    fig, ax = plt.subplots(figsize=(3.5, 2.65))
    ax.plot(x, y, marker="o", color=BLUE, linewidth=1.6)
    ax.scatter([40], [34.59825], color=GREEN, s=38, zorder=3, label="Nominal vertical")
    ax.scatter([160], [95.489], color=ORANGE, s=38, zorder=3, label="Planar proxy")
    ax.set_xlabel("Lumped link capacitance (fF)")
    ax.set_ylabel("Supply energy per toggle (fJ)")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    ax.set_title("ngspice link switching energy", fontweight="bold")
    save(fig, "fig7_spice_energy_vs_capacitance")


def figure8():
    data = rows("spice_link_results.csv")
    ordered = sorted(data, key=lambda r: float(r["capacitance_fF"]))
    x = [float(r["capacitance_fF"]) for r in ordered]
    y = [float(r["mean_delay_ps"]) for r in ordered]
    fig, ax = plt.subplots(figsize=(3.5, 2.65))
    ax.plot(x, y, marker="o", color=BLUE, linewidth=1.6)
    ax.scatter([40], [14.675375], color=GREEN, s=38, zorder=3, label="Nominal vertical")
    ax.scatter([160], [27.36712], color=ORANGE, s=38, zorder=3, label="Planar proxy")
    ax.set_xlabel("Lumped link capacitance (fF)")
    ax.set_ylabel("Mean propagation delay (ps)")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    ax.set_title("ngspice link delay", fontweight="bold")
    save(fig, "fig8_spice_delay_vs_capacitance")


def main():
    figure1()
    figure2()
    figure3()
    figure4()
    figure5()
    figure6()
    figure7()
    figure8()


if __name__ == "__main__":
    main()
