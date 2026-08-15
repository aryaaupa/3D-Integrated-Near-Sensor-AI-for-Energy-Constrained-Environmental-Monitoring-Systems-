#!/usr/bin/env python3
"""Generate all manuscript figures exclusively from committed CSV inputs."""

from __future__ import annotations

import csv
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle


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


def save_ieee(fig: plt.Figure, stem: str) -> None:
    """Save compact manuscript schematics as vector and 600-dpi raster files."""
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.015)
    fig.savefig(OUT / f"{stem}.svg", bbox_inches="tight", pad_inches=0.015)
    fig.savefig(OUT / f"{stem}.png", dpi=600, bbox_inches="tight", pad_inches=0.015)
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


def _iso_point(x: float, y: float, origin: tuple[float, float], ux, uy):
    return (origin[0] + x * ux[0] + y * uy[0], origin[1] + x * ux[1] + y * uy[1])


def _iso_rect(ax, origin, ux, uy, x, y, w, h, *, edge=DARK, face="white", lw=0.55):
    points = [_iso_point(px, py, origin, ux, uy) for px, py in
              ((x, y), (x + w, y), (x + w, y + h), (x, y + h))]
    ax.add_patch(Polygon(points, closed=True, facecolor=face, edgecolor=edge, linewidth=lw))
    return points


def _silicon_tier(ax, origin, ux, uy, thickness, label, face):
    top = [_iso_point(x, y, origin, ux, uy) for x, y in ((0, 0), (1, 0), (1, 1), (0, 1))]
    lower = [(x, y - thickness) for x, y in top]
    ax.add_patch(Polygon([top[1], top[2], lower[2], lower[1]], closed=True,
                         facecolor="#D9DEE2", edgecolor=DARK, linewidth=0.55))
    ax.add_patch(Polygon([top[2], top[3], lower[3], lower[2]], closed=True,
                         facecolor="#E7EAEC", edgecolor=DARK, linewidth=0.55))
    ax.add_patch(Polygon(top, closed=True, facecolor=face, edgecolor=DARK, linewidth=0.7))
    ax.text(top[3][0] - 0.012, top[3][1] + 0.016, label, ha="left", va="bottom",
            fontsize=6.2, fontweight="bold", color=DARK)
    return top, lower


def figure1():
    fig, ax = plt.subplots(figsize=(3.5, 2.15))
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ux, uy = (0.55, 0.0), (0.21, 0.12)
    origins = [(0.12, 0.77), (0.12, 0.51), (0.12, 0.25)]
    faces = ["#F7F8F8", "#F7F1EC", "#EEF3F7"]
    labels = ["Sensor Tier", "Localized SRAM Tier", "Compute Tier"]
    tiers = [_silicon_tier(ax, o, ux, uy, 0.035, label, face)
             for o, label, face in zip(origins, labels, faces)]

    # Sparse sensor/front-end tiles; no sensor modality or dimensions are implied.
    for ix in range(4):
        for iy in range(2):
            _iso_rect(ax, origins[0], ux, uy, 0.12 + ix * 0.19, 0.20 + iy * 0.30,
                      0.12, 0.17, edge="#596168", face="white", lw=0.35)

    # Local storage banks.
    for ix in range(4):
        _iso_rect(ax, origins[1], ux, uy, 0.10 + ix * 0.205, 0.22, 0.15, 0.54,
                  edge=ORANGE, face="#FBF5EF", lw=0.45)
    ax.text(0.49, 0.575, "2-MiB SRAM", ha="center", va="center", fontsize=5.4, color=DARK)

    # Compute die: verified global buffer plus a compact depiction of the 168-PE array.
    _iso_rect(ax, origins[2], ux, uy, 0.06, 0.18, 0.18, 0.64,
              edge=BLUE, face="#F3F7FA", lw=0.55)
    ax.text(0.235, 0.325, "128-KiB\nGB", ha="center", va="center", fontsize=4.8,
            color=DARK, linespacing=0.9)
    for ix in range(7):
        for iy in range(4):
            _iso_rect(ax, origins[2], ux, uy, 0.34 + ix * 0.075, 0.19 + iy * 0.145,
                      0.055, 0.09, edge=BLUE, face="white", lw=0.3)
    ax.text(0.585, 0.335, "168-PE array", ha="center", va="center", fontsize=5.4,
            fontweight="bold", color=DARK)

    # Four representative vertical inter-tier paths, explicitly schematic.
    for x in (0.25, 0.42, 0.59, 0.76):
        ax.plot([x, x], [0.345, 0.745], color="#555B60", linewidth=0.45, zorder=0)
        for y in (0.49, 0.75):
            ax.plot(x, y, marker="o", markersize=1.9, markerfacecolor=BLUE,
                    markeredgecolor="#555B60", markeredgewidth=0.3)
    ax.text(0.905, 0.51, "vertical inter-tier\ncommunication", rotation=90,
            ha="center", va="center", fontsize=5.0, color="#555B60", linespacing=0.95)
    save_ieee(fig, "fig1_architecture")


def _compact_node(ax, x, y, w, label, edge, fill="white"):
    ax.add_patch(Rectangle((x, y), w, 0.20, facecolor=fill, edgecolor=edge, linewidth=0.7))
    ax.text(x + w / 2, y + 0.10, label, ha="center", va="center", fontsize=6.1,
            fontweight="bold", color=DARK, linespacing=0.95)


def figure2():
    fig, ax = plt.subplots(figsize=(7.0, 1.55))
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    xs = [0.035, 0.205, 0.375, 0.545]
    widths = [0.13, 0.13, 0.13, 0.15]
    architecture = ["Workload", "Timeloop", "Accelergy /\nCACTI", "Architecture\nenergy"]
    circuit = ["PTM model", "ngspice", "Link testbench", "Energy / delay"]
    for labels, y, color, fill in ((architecture, 0.64, BLUE, "#F3F7FA"),
                                    (circuit, 0.16, ORANGE, "#FBF5EF")):
        for i, (x, w, label) in enumerate(zip(xs, widths, labels)):
            _compact_node(ax, x, y, w, label, color, fill if i in (0, 2) else "white")
            if i < 3:
                arrow(ax, (x + w, y + 0.10), (xs[i + 1], y + 0.10), color)

    _compact_node(ax, 0.795, 0.37, 0.17, "Separate cross-level\ninterpretation", DARK, "#F5F5F5")
    arrow(ax, (0.695, 0.74), (0.795, 0.52), DARK)
    arrow(ax, (0.695, 0.26), (0.795, 0.46), DARK)
    ax.text(0.008, 0.74, "ARCH.", ha="left", va="center", fontsize=5.4,
            fontweight="bold", color=BLUE)
    ax.text(0.008, 0.26, "CIRCUIT", ha="left", va="center", fontsize=5.4,
            fontweight="bold", color=ORANGE)
    save_ieee(fig, "fig2_evaluation_workflow")


def figure3():
    fig, ax = plt.subplots(figsize=(7.0, 2.45))
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    columns = [(0.11, "PLANAR", "LPDDR4", ORANGE, "#FBF1E8"),
               (0.61, "LOCALIZED", "2-MiB SRAM", BLUE, "#EAF1F6")]
    levels = [(0.76, None), (0.54, "128-KiB SRAM"), (0.32, "PE RFs"), (0.10, "168-PE array")]
    for x, heading, top, color, top_fill in columns:
        ax.text(x + 0.14, 0.965, heading, ha="center", va="top", fontsize=7.2,
                fontweight="bold", color=DARK)
        for i, (y, label) in enumerate(levels):
            text = top if i == 0 else label
            fill = top_fill if i == 0 else "white"
            edge = color if i == 0 else "#4E555A"
            ax.add_patch(Rectangle((x, y), 0.28, 0.105, facecolor=fill,
                                   edgecolor=edge, linewidth=0.8 if i == 0 else 0.6))
            ax.text(x + 0.14, y + 0.0525, text, ha="center", va="center", fontsize=6.2,
                    fontweight="bold" if i in (0, 3) else "normal", color=DARK)
            if i < len(levels) - 1:
                ax.plot([x + 0.14, x + 0.14], [y, levels[i + 1][0] + 0.105],
                        color="#4E555A", linewidth=0.65)
                ax.add_patch(FancyArrowPatch((x + 0.14, y - 0.015),
                                             (x + 0.14, levels[i + 1][0] + 0.11),
                                             arrowstyle="-|>", mutation_scale=6,
                                             linewidth=0.6, color="#4E555A"))

    # The dashed region spans both columns and contains only frozen components.
    ax.add_patch(Rectangle((0.065, 0.055), 0.87, 0.64, facecolor="none",
                           edgecolor="#596168", linewidth=0.7, linestyle=(0, (3, 2))))
    ax.text(0.50, 0.715, "IDENTICAL: mapping, precision, clock, lower hierarchy, compute",
            ha="center", va="center", fontsize=5.6, fontweight="bold", color="#4E555A",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    ax.annotate("only controlled change", xy=(0.50, 0.812), xytext=(0.50, 0.895),
                ha="center", va="center", fontsize=5.3, color="#4E555A",
                arrowprops=dict(arrowstyle="-[,widthB=10.5,lengthB=0.5", lw=0.55,
                                color="#4E555A"))
    save_ieee(fig, "fig3_controlled_hierarchy")


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
    ax.set_xticks(x, ["AlexNet\nCONV1", "Dense\nCONV2"])
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
    ax.set_xticks(x, ["AlexNet\nCONV1", "Dense\nCONV2"])
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
