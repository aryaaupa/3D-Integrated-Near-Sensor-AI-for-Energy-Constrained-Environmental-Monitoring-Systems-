#!/usr/bin/env python3
"""Generate all SPICE figures from committed CSV/raw waveform evidence."""

from __future__ import annotations

import csv
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/timeloop-spice-matplotlib-cache")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "processed"
FIGURES = ROOT / "figures"
COLORS = {"planar": "#B4493B", "vertical": "#2878B5"}


def save(fig: plt.Figure, name: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIGURES / f"{name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def load_results() -> list[dict[str, str]]:
    with (PROCESSED / "link_results.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9, "figure.dpi": 150})
    rows = load_results()
    nominal = {r["architecture"]: r for r in rows if r["role"] == "nominal"}

    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.8))
    names = ["Planar bump\nproxy", "Vertical TSV"]
    archs = ["planar", "vertical"]
    energies = [float(nominal[a]["supply_energy_per_toggle_fJ"]) for a in archs]
    delays = [float(nominal[a]["mean_propagation_delay_ps"]) for a in archs]
    axes[0].bar(names, energies, color=[COLORS[a] for a in archs], width=0.62)
    axes[0].set_ylabel("Supply energy per toggle (fJ)")
    axes[0].set_title("Transistor-level link energy")
    axes[1].bar(names, delays, color=[COLORS[a] for a in archs], width=0.62)
    axes[1].set_ylabel("Mean propagation delay (ps)")
    axes[1].set_title("Transistor-level link delay")
    for ax, values in zip(axes, [energies, delays]):
        ax.grid(axis="y", alpha=0.25); ax.set_axisbelow(True)
        for i, value in enumerate(values): ax.text(i, value * 1.02, f"{value:.2f}", ha="center", va="bottom", fontsize=8)
    fig.tight_layout(); save(fig, "nominal_energy_delay")

    ordered = sorted(rows, key=lambda r: float(r["link_capacitance_fF"]))
    caps = [float(r["link_capacitance_fF"]) for r in ordered]
    energy = [float(r["supply_energy_per_toggle_fJ"]) for r in ordered]
    delay = [float(r["mean_propagation_delay_ps"]) for r in ordered]
    fig, ax1 = plt.subplots(figsize=(4.3, 3.1))
    ax2 = ax1.twinx()
    ax1.plot(caps, energy, "o-", color="#2878B5", label="Energy")
    ax2.plot(caps, delay, "s--", color="#E18727", label="Delay")
    ax1.axvline(40, color="#2878B5", alpha=0.25, linewidth=1)
    ax1.axvline(160, color="#B4493B", alpha=0.25, linewidth=1)
    ax1.annotate("Measured TSV", xy=(40, energy[caps.index(40.0)]), xytext=(48, 28),
                 textcoords="data", fontsize=7, color="#2878B5",
                 arrowprops={"arrowstyle": "-", "color": "#2878B5", "alpha": 0.6})
    ax1.annotate("Planar lower bound", xy=(160, energy[caps.index(160.0)]), xytext=(112, 88),
                 textcoords="data", fontsize=7, color="#B4493B",
                 arrowprops={"arrowstyle": "-", "color": "#B4493B", "alpha": 0.6})
    ax1.set_xlabel("Interconnect capacitance (fF)")
    ax1.set_ylabel("Supply energy per toggle (fJ)", color="#2878B5")
    ax2.set_ylabel("Mean propagation delay (ps)", color="#E18727")
    ax1.grid(alpha=0.25); fig.tight_layout(); save(fig, "capacitance_sensitivity")

    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.8), sharey=True)
    for ax, arch, title in zip(axes, archs, names):
        case = nominal[arch]["case"]
        data = np.loadtxt(ROOT / "raw_outputs" / case / "waveform.txt")
        mask = (data[:, 0] >= 1.05e-9) & (data[:, 0] <= 1.72e-9)
        time_ns = data[mask, 0] * 1e9
        ax.plot(time_ns, data[mask, 3], color="#555555", linewidth=1.0, label="Input")
        ax.plot(time_ns, data[mask, 5], color="#7A5195", linewidth=1.4, label="Link node")
        ax.plot(time_ns, data[mask, 7], color="#54A24B", linewidth=1.1, label="Receiver output")
        ax.set_title(title.replace("\n", " ")); ax.set_xlabel("Time (ns)"); ax.grid(alpha=0.22)
    axes[0].set_ylabel("Voltage (V)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0, 1, 0.88)); save(fig, "nominal_waveforms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
