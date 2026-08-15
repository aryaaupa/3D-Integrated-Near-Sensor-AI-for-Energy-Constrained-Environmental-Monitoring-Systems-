#!/usr/bin/env python3
"""Generate four IEEE-style manuscript figures from verified repository evidence.

The numerical summary is read from the committed architecture and SPICE CSVs.
The diagram labels are cross-checked against TABLES.md before rendering.
"""

from __future__ import annotations

import csv
import math
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "figure_data"
OUT = ROOT / "publication_figures"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#1F4E79"
BLUE = "#4C78A8"
TEAL = "#2A7F73"
ORANGE = "#D0792A"
GOLD = "#C9A227"
LIGHT_BLUE = "#EAF2F8"
LIGHT_TEAL = "#E8F3F0"
LIGHT_ORANGE = "#FBF0E6"
LIGHT_GRAY = "#F2F4F5"
MID_GRAY = "#68727A"
DARK = "#1D242A"
WHITE = "#FFFFFF"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 8,
        "axes.titlesize": 9,
        "axes.labelsize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "savefig.facecolor": "white",
    }
)


def csv_rows(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def verify_sources() -> tuple[dict[tuple[str, str], dict[str, str]], dict[str, dict[str, str]]]:
    architecture = {
        (row["workload"], row["architecture"]): row
        for row in csv_rows("architecture_results.csv")
    }
    spice = {row["case"]: row for row in csv_rows("spice_link_results.csv")}

    expected_architecture = {
        ("CONV1", "Planar"): (7343.23, 732050, 0.8571),
        ("CONV1", "Localized"): (2256.65, 732050, 0.8571),
        ("CONV2", "Planar"): (3103.78, 3110400, 0.8571),
        ("CONV2", "Localized"): (2261.55, 3110400, 0.8571),
    }
    for key, expected in expected_architecture.items():
        row = architecture[key]
        actual = (
            float(row["total_energy_uJ"]),
            int(row["cycles"]),
            float(row["utilization"]),
        )
        if actual != expected:
            raise ValueError(f"Architecture evidence mismatch for {key}: {actual} != {expected}")

    expected_spice = {
        "planar_bump_160fF": (160.0, 95.489, 27.36712),
        "vertical_40fF": (40.0, 34.59825, 14.675375),
    }
    for key, expected in expected_spice.items():
        row = spice[key]
        actual = (
            float(row["capacitance_fF"]),
            float(row["energy_per_toggle_fJ"]),
            float(row["mean_delay_ps"]),
        )
        if actual != expected:
            raise ValueError(f"SPICE evidence mismatch for {key}: {actual} != {expected}")

    conv1_reduction = 100 * (7343.23 - 2256.65) / 7343.23
    conv2_reduction = 100 * (3103.78 - 2261.55) / 3103.78
    link_energy_reduction = 100 * (95.489 - 34.59825) / 95.489
    link_delay_reduction = 100 * (27.36712 - 14.675375) / 27.36712
    checks = [
        (conv1_reduction, 69.26897292),
        (conv2_reduction, 27.13562173),
        (link_energy_reduction, 63.7672925677),
        (link_delay_reduction, 46.3758882922),
    ]
    for actual, expected in checks:
        if not math.isclose(actual, expected, rel_tol=0, abs_tol=2e-8):
            raise ValueError(f"Derived percentage mismatch: {actual} != {expected}")

    manuscript_tables = (ROOT / "TABLES.md").read_text(encoding="utf-8")
    required_labels = [
        "14 × 12 = 168 PEs",
        "12 entries",
        "192 entries",
        "16 entries",
        "128 KiB",
        "1 ns (nominal 1 GHz)",
        "External LPDDR4, 64-bit access width",
        "2-MiB CACTI-backed SRAM, 64-bit access width",
    ]
    missing = [label for label in required_labels if label not in manuscript_tables]
    if missing:
        raise ValueError(f"Verified architecture labels missing from TABLES.md: {missing}")
    return architecture, spice


def save_all(fig: plt.Figure, stem: str) -> None:
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(OUT / f"{stem}.svg", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(OUT / f"{stem}.png", dpi=600, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def setup_canvas(figsize: tuple[float, float]) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def rounded_box(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    detail: str = "",
    *,
    edge: str = NAVY,
    face: str = WHITE,
    title_size: float = 7.4,
    detail_size: float = 6.2,
    linewidth: float = 1.2,
    rounding: float = 0.018,
    title_wrap: int = 30,
    detail_wrap: int = 44,
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.012,rounding_size={rounding}",
        linewidth=linewidth,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(patch)
    title_y = y + h * (0.64 if detail else 0.50)
    rendered_title = (
        "\n".join(textwrap.fill(part, width=title_wrap) for part in title.splitlines())
        if title_wrap > 0 else title
    )
    ax.text(
        x + w / 2,
        title_y,
        rendered_title,
        ha="center",
        va="center",
        fontsize=title_size,
        fontweight="bold",
        color=DARK,
        linespacing=1.05,
    )
    if detail:
        rendered_detail = (
            "\n".join(textwrap.fill(part, width=detail_wrap) for part in detail.splitlines())
            if detail_wrap > 0 else detail
        )
        ax.text(
            x + w / 2,
            y + h * 0.27,
            rendered_detail,
            ha="center",
            va="center",
            fontsize=detail_size,
            color=DARK,
            linespacing=1.05,
        )


def arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = DARK,
    dashed: bool = False,
    both: bool = False,
    width: float = 1.1,
) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="<|-|>" if both else "-|>",
            mutation_scale=9,
            linewidth=width,
            linestyle="--" if dashed else "-",
            color=color,
            shrinkA=1,
            shrinkB=1,
        )
    )


def figure_a() -> None:
    fig, ax = setup_canvas((3.5, 4.25))
    ax.text(0.5, 0.975, "Proposed three-tier near-sensor architecture", ha="center", va="top",
            fontsize=9.2, fontweight="bold", color=DARK)

    tiers = [
        (0.12, 0.70, 0.76, 0.18, "Sensing and front-end tier",
         "Sensor interface, acquisition, and conditioning\nConceptual tier; sensing accuracy and thermal behavior not simulated",
         TEAL, LIGHT_TEAL),
        (0.12, 0.43, 0.76, 0.18, "Localized-memory tier",
         "Working-set storage near compute\nEvaluated architectural proxy: 2-MiB localized SRAM",
         ORANGE, LIGHT_ORANGE),
        (0.12, 0.13, 0.76, 0.21, "Compute tier",
         "168-PE array (14 x 12)\n128-KiB global SRAM + PE-local RFs + integer MACs",
         NAVY, LIGHT_BLUE),
    ]
    for x, y, w, h, title, detail, edge, face in tiers:
        rounded_box(ax, x, y, w, h, title, detail, edge=edge, face=face, title_size=8, detail_size=6.1)

    arrow(ax, (0.50, 0.695), (0.50, 0.62), color=MID_GRAY, both=True, width=1.3)
    arrow(ax, (0.50, 0.425), (0.50, 0.35), color=MID_GRAY, both=True, width=1.3)
    ax.text(0.955, 0.515, "conceptual vertical\ninter-tier communication", rotation=90,
            ha="center", va="center", fontsize=6.2, color=MID_GRAY)
    ax.plot([0.925, 0.925], [0.22, 0.79], color=MID_GRAY, linewidth=0.8)

    ax.add_patch(Rectangle((0.04, 0.015), 0.92, 0.065, facecolor=LIGHT_GRAY, edgecolor="none"))
    ax.text(0.50, 0.048,
            "Architectural organization only - no physical dimensions, TSV count,\n"
            "floorplan, or thermal field is implied.",
            ha="center", va="center", fontsize=5.7, color=DARK, linespacing=1.05)
    save_all(fig, "figure_A_three_tier_architecture")


def hierarchy_column(ax: plt.Axes, x: float, title: str, top_title: str, top_detail: str,
                     color: str, top_face: str) -> None:
    ax.text(x + 0.17, 0.745, title, ha="center", va="center", fontsize=9,
            fontweight="bold", color=color)
    levels = [
        (0.565, top_title, top_detail, top_face),
        (0.405, "128-KiB global SRAM", "Identical shared on-chip buffer", WHITE),
        (0.245, "PE-local register files", "Input: 12 | Weight: 192 | Partial sum: 16 entries per PE", WHITE),
        (0.085, "168-PE MAC array", "14 x 12 array; identical compute capability", WHITE),
    ]
    for idx, (y, name, detail, face) in enumerate(levels):
        rounded_box(ax, x, y, 0.34, 0.115, name, detail, edge=color, face=face,
                    title_size=6.7, detail_size=5.15, linewidth=1.15)
        if idx < len(levels) - 1:
            arrow(ax, (x + 0.17, y - 0.006), (x + 0.17, y - 0.045), color=color, both=True, width=0.9)


def figure_b() -> None:
    fig, ax = setup_canvas((7.0, 4.65))
    ax.text(0.5, 0.982, "Controlled planar-versus-localized architecture comparison",
            ha="center", va="top", fontsize=9.5, fontweight="bold", color=DARK)

    rounded_box(
        ax, 0.055, 0.825, 0.89, 0.095,
        "Held identical in both configurations",
        "168 PEs (14 x 12) | RFs: 12 input, 192 weight, 16 partial-sum entries/PE | 128-KiB global SRAM\n"
        "8-b inputs/weights | 16-b partial sums/outputs | fixed mapping | 1-ns clock",
        edge=MID_GRAY, face=LIGHT_GRAY, title_size=6.8, detail_size=5.15,
        title_wrap=80, detail_wrap=110,
    )

    hierarchy_column(ax, 0.08, "Planar baseline", "External LPDDR4", "64-bit highest-level access",
                     ORANGE, LIGHT_ORANGE)
    hierarchy_column(ax, 0.58, "Localized configuration", "2-MiB localized SRAM",
                     "64-bit highest-level access; CACTI-backed", NAVY, LIGHT_BLUE)

    ax.text(0.50, 0.685, "ONLY CONTROLLED\nARCHITECTURAL CHANGE", ha="center", va="center",
            fontsize=5.7, fontweight="bold", color=DARK, linespacing=1.0)
    arrow(ax, (0.43, 0.625), (0.57, 0.625), color=DARK, both=True, width=1.0)

    ax.add_patch(Rectangle((0.055, 0.005), 0.89, 0.05, facecolor=LIGHT_GRAY, edgecolor="none"))
    ax.text(0.50, 0.030,
            "Fixed mapping: highest-level event counts, Timeloop cycles, and PE utilization remain unchanged.",
            ha="center", va="center", fontsize=6.1, fontweight="bold", color=DARK)
    save_all(fig, "figure_B_controlled_planar_vs_localized")


def workflow_box(ax: plt.Axes, x: float, y: float, w: float, title: str, detail: str,
                 color: str, face: str) -> None:
    rounded_box(ax, x, y, w, 0.16, title, detail, edge=color, face=face,
                title_size=6.25, detail_size=4.85, linewidth=1.1,
                title_wrap=0, detail_wrap=0)


def figure_c() -> None:
    fig, ax = setup_canvas((7.2, 4.35))
    ax.text(0.5, 0.98, "Two-level evaluation methodology", ha="center", va="top",
            fontsize=9.5, fontweight="bold", color=DARK)

    ax.add_patch(FancyBboxPatch((0.025, 0.54), 0.79, 0.34,
                               boxstyle="round,pad=0.012,rounding_size=0.018",
                               facecolor="#F7FAFD", edgecolor=BLUE, linewidth=1.0, linestyle="--"))
    ax.text(0.045, 0.85, "ARCHITECTURE PATH", ha="left", va="center", fontsize=7,
            fontweight="bold", color=BLUE)
    arch_nodes = [
        (0.045, 0.625, 0.15, "Workloads", "AlexNet CONV1\nAlexNet-derived\ndense CONV2"),
        (0.215, 0.625, 0.105, "Timeloop", "Fixed mappings"),
        (0.34, 0.625, 0.18, "Architecture\nstatistics", "Action counts\nCycles | utilization"),
        (0.54, 0.625, 0.14, "Accelergy\n+ CACTI", "Component action\nenergies"),
        (0.70, 0.625, 0.095, "Output", "Architecture-level\nenergy"),
    ]
    for x, y, w, title, detail in arch_nodes:
        workflow_box(ax, x, y, w, title, detail, BLUE, WHITE)
    for left, right in zip(arch_nodes[:-1], arch_nodes[1:]):
        arrow(ax, (left[0] + left[2], 0.705), (right[0] - 0.006, 0.705), color=BLUE, width=0.9)

    ax.add_patch(FancyBboxPatch((0.025, 0.10), 0.79, 0.34,
                               boxstyle="round,pad=0.012,rounding_size=0.018",
                               facecolor="#FEFAF6", edgecolor=ORANGE, linewidth=1.0, linestyle="--"))
    ax.text(0.045, 0.42, "CIRCUIT PATH", ha="left", va="center", fontsize=7,
            fontweight="bold", color=ORANGE)
    circ_nodes = [
        (0.045, 0.185, 0.14, "45nm_HP.pm\nPTM model card", "Exact committed file"),
        (0.205, 0.185, 0.115, "ngspice 42", "Transient\nsimulation"),
        (0.34, 0.185, 0.225, "Representative link\ntestbench", "CMOS driver -> capacitive link\n-> receiver"),
        (0.585, 0.185, 0.21, "Circuit outputs", "Switching energy/toggle\nPropagation delay"),
    ]
    for x, y, w, title, detail in circ_nodes:
        workflow_box(ax, x, y, w, title, detail, ORANGE, WHITE)
    for left, right in zip(circ_nodes[:-1], circ_nodes[1:]):
        arrow(ax, (left[0] + left[2], 0.265), (right[0] - 0.006, 0.265), color=ORANGE, width=0.9)

    rounded_box(ax, 0.845, 0.315, 0.13, 0.27, "Cross-level\ninterpretation",
                "Independent evidence\nNo co-simulation\nPercentages not combined",
                edge=MID_GRAY, face=LIGHT_GRAY, title_size=5.9, detail_size=4.8,
                title_wrap=0, detail_wrap=0)
    arrow(ax, (0.815, 0.705), (0.855, 0.55), color=MID_GRAY, dashed=True, width=0.9)
    arrow(ax, (0.815, 0.275), (0.855, 0.35), color=MID_GRAY, dashed=True, width=0.9)
    save_all(fig, "figure_C_two_level_methodology")


def figure_d(architecture: dict[tuple[str, str], dict[str, str]],
             spice: dict[str, dict[str, str]]) -> None:
    fig = plt.figure(figsize=(7.1, 4.15))
    grid = fig.add_gridspec(1, 2, width_ratios=[1.08, 0.92], wspace=0.28)
    ax_energy = fig.add_subplot(grid[0, 0])
    ax_link = fig.add_subplot(grid[0, 1])
    fig.suptitle("Verified architecture- and link-level evidence summary", y=0.99,
                 fontsize=9.5, fontweight="bold", color=DARK)

    workloads = ["CONV1", "CONV2"]
    labels = ["AlexNet\nCONV1", "AlexNet-derived\ndense CONV2"]
    planar = [float(architecture[(w, "Planar")]["total_energy_uJ"]) for w in workloads]
    localized = [float(architecture[(w, "Localized")]["total_energy_uJ"]) for w in workloads]
    reductions = [100 * (p - q) / p for p, q in zip(planar, localized)]
    x = [0, 1]
    width = 0.34
    ax_energy.bar([v - width / 2 for v in x], planar, width, color=ORANGE, label="Planar")
    ax_energy.bar([v + width / 2 for v in x], localized, width, color=BLUE, label="Localized")
    ax_energy.set_xticks(x, labels)
    ax_energy.set_ylabel("Total energy (µJ)")
    ax_energy.set_ylim(0, 8200)
    ax_energy.grid(axis="y", alpha=0.22, linewidth=0.6)
    ax_energy.set_axisbelow(True)
    ax_energy.set_title("Architecture level: Timeloop/Accelergy", fontsize=8, fontweight="bold")
    ax_energy.legend(frameon=False, loc="upper right")
    for i, (p, q, reduction) in enumerate(zip(planar, localized, reductions)):
        ax_energy.text(i - width / 2, p + 130, f"{p:,.2f}", ha="center", va="bottom", fontsize=6.1)
        ax_energy.text(i + width / 2, q + 130, f"{q:,.2f}", ha="center", va="bottom", fontsize=6.1)
        ax_energy.text(i, max(p, q) + 420, f"-{reduction:.2f}%", ha="center", va="bottom",
                       fontsize=7.2, fontweight="bold", color=NAVY)
    ax_energy.text(0.5, -0.19, "Timeloop cycles and utilization unchanged within each workload pair",
                   transform=ax_energy.transAxes, ha="center", va="top", fontsize=6.1,
                   fontweight="bold", color=DARK)

    ax_link.set_xlim(0, 1)
    ax_link.set_ylim(0, 1)
    ax_link.axis("off")
    ax_link.set_title("Circuit level: ngspice 42 representative link", fontsize=8, fontweight="bold", pad=4)
    rounded_box(ax_link, 0.05, 0.80, 0.39, 0.13, "Planar-link proxy",
                "160 fF | conservative derived load", edge=ORANGE, face=LIGHT_ORANGE,
                title_size=6.8, detail_size=5.4)
    rounded_box(ax_link, 0.56, 0.80, 0.39, 0.13, "Vertical-link reference",
                "40 fF | TSV reference", edge=TEAL, face=LIGHT_TEAL,
                title_size=6.8, detail_size=5.4)
    arrow(ax_link, (0.45, 0.865), (0.55, 0.865), color=MID_GRAY, width=1.0)

    planar_row = spice["planar_bump_160fF"]
    vertical_row = spice["vertical_40fF"]
    metrics = [
        ("Supply energy / toggle", float(planar_row["energy_per_toggle_fJ"]),
         float(vertical_row["energy_per_toggle_fJ"]), "fJ", 63.77),
        ("Mean propagation delay", float(planar_row["mean_delay_ps"]),
         float(vertical_row["mean_delay_ps"]), "ps", 46.38),
    ]
    y_values = [0.57, 0.31]
    for (label, p, v, unit, reduction), y in zip(metrics, y_values):
        ax_link.text(0.05, y + 0.11, label, ha="left", va="center", fontsize=6.6,
                     fontweight="bold", color=DARK)
        rounded_box(ax_link, 0.05, y - 0.02, 0.32, 0.11, f"{p:.3f} {unit}", "Planar proxy",
                    edge=ORANGE, face=WHITE, title_size=7.0, detail_size=5.2)
        arrow(ax_link, (0.39, y + 0.035), (0.58, y + 0.035), color=MID_GRAY, width=1.0)
        ax_link.text(0.485, y + 0.085, f"-{reduction:.2f}%", ha="center", va="center",
                     fontsize=6.7, fontweight="bold", color=NAVY)
        rounded_box(ax_link, 0.61, y - 0.02, 0.34, 0.11, f"{v:.3f} {unit}", "Vertical reference",
                    edge=TEAL, face=WHITE, title_size=7.0, detail_size=5.2)

    ax_link.add_patch(Rectangle((0.05, 0.035), 0.90, 0.095, facecolor=LIGHT_GRAY, edgecolor="none"))
    ax_link.text(0.50, 0.083,
                 "Architecture and circuit results are separate;\nlink delay is not inference latency.",
                 ha="center", va="center", fontsize=5.9, fontweight="bold", color=DARK)
    fig.subplots_adjust(left=0.075, right=0.985, top=0.90, bottom=0.18)
    save_all(fig, "figure_D_verified_evidence_summary")


def main() -> None:
    architecture, spice = verify_sources()
    figure_a()
    figure_b()
    figure_c()
    figure_d(architecture, spice)
    print("PUBLICATION_FIGURE_VALIDATION=PASS")
    print(f"OUTPUT_DIRECTORY={OUT}")


if __name__ == "__main__":
    main()
