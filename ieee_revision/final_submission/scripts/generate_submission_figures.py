#!/usr/bin/env python3
"""Generate final main and supplementary figures only from committed CSV data."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "figure_data"
MAIN = ROOT / "figures" / "main"
SUPP = ROOT / "figures" / "supplementary"
MAIN.mkdir(parents=True, exist_ok=True)
SUPP.mkdir(parents=True, exist_ok=True)

DARK = "#20262E"
BLUE = "#6F9DBD"
ORANGE = "#D7A06B"
GRID = "#D9DDE0"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 7,
    "axes.labelsize": 7, "legend.fontsize": 6.5,
    "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
    "axes.linewidth": 0.65, "pdf.fonttype": 42,
    "ps.fonttype": 42, "svg.fonttype": "none",
})


def read(name):
    with (DATA / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def save(fig, directory, stem):
    for suffix, kwargs in (("pdf", {}), ("svg", {}), ("png", {"dpi": 600})):
        fig.savefig(directory / f"{stem}.{suffix}", bbox_inches="tight",
                    pad_inches=0.02, **kwargs)
    plt.close(fig)


def style(ax, grid=True):
    if grid:
        ax.grid(axis="y", color=GRID, linewidth=0.45)
        ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color(DARK)
        spine.set_linewidth(0.65)


def paired():
    rows = read("architecture_results.csv")
    order = list(dict.fromkeys(r["workload"] for r in rows))
    labels = [next(r["label"] for r in rows if r["workload"] == w) for w in order]
    short = ["AlexNet\nCONV1", "AlexNet-derived\ndense CONV2", "AlexNet\nCONV3",
             "AlexNet-derived\ndense CONV4", "AlexNet-derived\ndense CONV5"]
    planar = [next(r for r in rows if r["workload"] == w and r["architecture"] == "Planar") for w in order]
    local = [next(r for r in rows if r["workload"] == w and r["architecture"] == "Localized") for w in order]
    return order, labels, short, planar, local


def figure4_energy():
    _, _, labels, planar, local = paired()
    x = list(range(5)); width = 0.31
    p = [float(r["total_energy_uJ"]) for r in planar]
    q = [float(r["total_energy_uJ"]) for r in local]
    fig, ax = plt.subplots(figsize=(7.0, 2.65))
    ax.bar([v-width/2 for v in x], p, width, label="Planar", color=ORANGE,
           edgecolor=DARK, linewidth=0.45)
    ax.bar([v+width/2 for v in x], q, width, label="Localized", color=BLUE,
           edgecolor=DARK, linewidth=0.45)
    ax.set_xticks(x, labels); ax.set_ylabel("Total energy (uJ)")
    ax.set_ylim(0, 8500); ax.set_xlim(-0.55, 4.55)
    ax.legend(frameon=False, ncol=2, loc="upper right")
    style(ax)
    for i, (a, b) in enumerate(zip(p, q)):
        reduction = 100 * (a-b) / a
        y = max(a, b) + 170
        ax.plot([i-width/2, i-width/2, i+width/2, i+width/2],
                [y-65, y, y, y-65], color=DARK, linewidth=0.55)
        ax.text(i, y+55, f"{reduction:.1f}% reduction", ha="center",
                va="bottom", fontsize=6.2, fontweight="bold")
    fig.subplots_adjust(left=0.085, right=0.995, bottom=0.20, top=0.97)
    save(fig, MAIN, "fig4_five_workload_energy")


def figure5_component_energy():
    order, _, labels, planar, local = paired()
    fig, ax = plt.subplots(figsize=(7.0, 2.75))
    width = 0.32
    positions = []
    tick_positions = []
    for i, (p_row, l_row) in enumerate(zip(planar, local)):
        for j, row in enumerate((p_row, l_row)):
            x = i + (-width / 2 if j == 0 else width / 2)
            positions.append(x)
            highest = float(row["highest_level_energy_uJ"])
            lower = float(row["lower_buffer_energy_uJ"])
            compute = float(row["compute_energy_uJ"])
            ax.bar(x, highest, width, color=ORANGE if j == 0 else BLUE,
                   edgecolor=DARK, linewidth=0.4,
                   label=("Highest memory: LPDDR4" if i == 0 and j == 0 else
                          "Highest memory: localized SRAM" if i == 0 and j == 1 else None))
            ax.bar(x, lower, width, bottom=highest, color="#CBD3D8",
                   edgecolor=DARK, linewidth=0.4,
                   label="Unchanged lower buffers" if i == 0 and j == 0 else None)
            ax.bar(x, compute, width, bottom=highest + lower, color="#66736B",
                   edgecolor=DARK, linewidth=0.4,
                   label="Unchanged compute" if i == 0 and j == 0 else None)
        tick_positions.append(i)
    ax.set_xticks(tick_positions, [f"{label}\nP        L" for label in labels])
    ax.set_ylabel("Component energy (uJ)")
    ax.set_ylim(0, 7800)
    ax.set_xlim(-0.55, 4.55)
    ax.legend(frameon=False, ncol=2, loc="upper right", columnspacing=1.0,
              handlelength=1.4)
    style(ax)
    fig.subplots_adjust(left=0.085, right=0.995, bottom=0.18, top=0.98)
    save(fig, MAIN, "fig5_component_energy")


def figure6_capacity():
    rows = read("capacity_sensitivity.csv")
    x = [int(r["capacity_MiB"]) for r in rows]
    y = [float(r["total_energy_uJ"]) for r in rows]
    reduction = [float(r["energy_reduction_percent"]) for r in rows]
    baseline = float(rows[0]["planar_energy_uJ"])
    fig, ax = plt.subplots(figsize=(3.5, 2.45))
    ax.plot(x, y, marker="o", color=BLUE, markeredgecolor=DARK,
            markeredgewidth=0.45, linewidth=1.1)
    ax.axhline(baseline, color=ORANGE, linestyle="--", linewidth=0.9,
               label="Planar LPDDR4")
    ax.set_xscale("log", base=2); ax.set_xticks(x, [str(v) for v in x])
    ax.set_xlabel("Localized SRAM capacity (MiB)")
    ax.set_ylabel("CONV1 total energy (uJ)")
    ax.set_ylim(1500, 7800); ax.legend(frameon=False, loc="upper right")
    style(ax)
    for a, b, r in zip(x, y, reduction):
        ax.annotate(f"{r:.1f}%", (a, b), xytext=(0, 6),
                    textcoords="offset points", ha="center", fontsize=6.1)
    save(fig, MAIN, "fig6_capacity_sensitivity")


def link_plot(metric, ylabel, stem):
    rows = sorted(read("link_results.csv"), key=lambda r: float(r["capacitance_fF"]))
    x = [float(r["capacitance_fF"]) for r in rows]
    y = [float(r[metric]) for r in rows]
    fig, ax = plt.subplots(figsize=(3.5, 2.45))
    ax.plot(x, y, color=DARK, linewidth=0.8, zorder=1)
    ax.scatter(x, y, color=BLUE, edgecolors=DARK, linewidths=0.45, s=24, zorder=2)
    for r, a, b in zip(rows, x, y):
        if r["role"] == "vertical_reference":
            ax.scatter([a], [b], color=BLUE, edgecolors=DARK, s=38, zorder=3)
            ax.annotate("40-fF TSV reference", (a, b), xytext=(5, 7),
                        textcoords="offset points", fontsize=6.0)
        if r["role"] == "planar_proxy":
            ax.scatter([a], [b], color=ORANGE, edgecolors=DARK, s=38, zorder=3)
            ax.annotate("160-fF planar proxy", (a, b), xytext=(-4, -12),
                        textcoords="offset points", ha="right", fontsize=6.0)
    ax.set_xlabel("Lumped link capacitance (fF)"); ax.set_ylabel(ylabel)
    style(ax); save(fig, MAIN, stem)


def supplementary():
    order, _, labels, planar, local = paired()
    comparison = {r["workload"]: r for r in read("comparison.csv")}

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.55), sharey=True)
    reduction = [float(comparison[w]["energy_reduction_percent"]) for w in order]
    x_values = [
        [float(comparison[w]["planar_highest_level_energy_share_percent"]) for w in order],
        [float(r["intensity"]) for r in planar],
    ]
    x_labels = [
        "Planar highest-memory energy fraction (%)",
        "Tensor-intensity indicator (MACs/tensor element)",
    ]
    panel_titles = ["(a) Exposed highest-memory fraction", "(b) Tensor-intensity indicator"]
    offsets = [[(-4,-16),(-4,5),(4,-10),(4,12),(4,-18)],
               [(4,-16),(-4,5),(4,-10),(4,-20),(4,8)]]
    aligns = [["right","right","left","left","left"],
              ["left","right","left","left","left"]]
    for ax, x, xlabel, title, offs, has in zip(
            axes, x_values, x_labels, panel_titles, offsets, aligns):
        ax.scatter(x, reduction, s=28, color=BLUE, edgecolors=DARK, linewidths=0.45)
        for label, a, b, off, align in zip(labels, x, reduction, offs, has):
            ax.annotate(label, (a, b), xytext=off, textcoords="offset points",
                        ha=align, fontsize=5.6)
        ax.set_xlabel(xlabel)
        ax.set_title(title, fontsize=7, fontweight="bold")
        ax.set_ylim(0, 75)
        style(ax)
    axes[0].set_ylabel("Planar-to-localized total-energy reduction (%)")
    fig.text(0.5, 0.01, "Five evaluated workloads; points are descriptive and no trend is fitted.",
             ha="center", va="bottom", fontsize=6.0, color=DARK)
    fig.subplots_adjust(left=0.08, right=0.995, bottom=0.23, top=0.90, wspace=0.22)
    save(fig, SUPP, "figS1_mechanism_comparison")

    fig, ax = plt.subplots(figsize=(7.0, 2.5)); width=0.31; xx=list(range(5))
    p=[float(r["energy_per_compute_pJ"]) for r in planar]
    q=[float(r["energy_per_compute_pJ"]) for r in local]
    ax.bar([v-width/2 for v in xx],p,width,label="Planar",color=ORANGE,edgecolor=DARK,linewidth=.45)
    ax.bar([v+width/2 for v in xx],q,width,label="Localized",color=BLUE,edgecolor=DARK,linewidth=.45)
    ax.set_xticks(xx,labels); ax.set_ylabel("Energy per compute (pJ)")
    ax.legend(frameon=False,ncol=2); style(ax)
    save(fig,SUPP,"figS2_energy_per_compute")

    fig, ax = plt.subplots(figsize=(7.0,2.45))
    accesses=[int(r["external_dram_accesses"]) for r in planar]
    ax.bar(range(5),accesses,color=ORANGE,edgecolor=DARK,linewidth=.45)
    ax.set_xticks(range(5),labels); ax.set_ylabel("Planar external-DRAM actions")
    ax.ticklabel_format(axis="y",style="sci",scilimits=(0,0)); style(ax)
    ax.text(.99,.94,"Localized configuration: 0 external-DRAM actions by construction",
            transform=ax.transAxes,ha="right",va="top",fontsize=6.1)
    save(fig,SUPP,"figS4_external_dram_actions")


def main():
    figure4_energy(); figure5_component_energy(); figure6_capacity()
    link_plot("energy_per_toggle_fJ", "Supply energy per toggle (fJ)", "fig7_link_energy")
    link_plot("mean_delay_ps", "Mean propagation delay (ps)", "fig8_link_delay")
    supplementary()


if __name__ == "__main__":
    main()
