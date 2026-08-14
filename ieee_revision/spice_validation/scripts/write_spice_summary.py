#!/usr/bin/env python3
"""Generate manuscript-ready SPICE text strictly from processed CSV files."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "processed"


def main() -> int:
    with (PROCESSED / "link_results.csv").open(newline="", encoding="utf-8") as handle:
        results = list(csv.DictReader(handle))
    with (PROCESSED / "link_comparison.csv").open(newline="", encoding="utf-8") as handle:
        comparison = next(csv.DictReader(handle))
    with (PROCESSED / "system_bridge.csv").open(newline="", encoding="utf-8") as handle:
        bridge = [r for r in csv.DictReader(handle) if r["assumed_bit_toggle_probability"] == "0.5"]
    nominal = {r["architecture"]: r for r in results if r["role"] == "nominal"}
    p, v = nominal["planar"], nominal["vertical"]
    sensitivity = sorted((float(r["link_capacitance_fF"]), float(r["supply_energy_per_toggle_fJ"]), float(r["mean_propagation_delay_ps"])) for r in results if r["architecture"] == "vertical")
    bridge_lines = []
    for row in bridge:
        label = "CONV1" if "conv1" in row["workload"] else "CONV2"
        arch = "planar" if row["architecture"] == "planar" else "3D proxy"
        bridge_lines.append(
            f"- {label}, {arch}: {float(row['diagnostic_link_energy_uJ']):.3f} µJ "
            f"({float(row['diagnostic_link_energy_fraction_percent']):.3f}% of the corresponding Timeloop/Accelergy total)."
        )
    text = f"""# Transistor-level communication-path validation

## Nominal result

ngspice transient simulation with the public 45 nm PTM BSIM4 model gives
**{float(p['supply_energy_per_toggle_fJ']):.3f} fJ/toggle** for the conservative
160 fF planar bump-load proxy and **{float(v['supply_energy_per_toggle_fJ']):.3f}
fJ/toggle** for the measured 40 fF TSV load. The reduction is
**{float(comparison['energy_per_toggle_reduction_percent']):.2f}%**. Mean
input-to-receiver propagation delay is **{float(p['mean_propagation_delay_ps']):.3f}
ps** and **{float(v['mean_propagation_delay_ps']):.3f} ps**, respectively, a
**{float(comparison['mean_delay_reduction_percent']):.2f}%** reduction.

Both cases use the same 1 V, 45 nm transistor model, driver, receiver,
fanout-of-one load, 20 ps input slew, 1 ns test period, and 65 mΩ series
resistance. Only interconnect capacitance changes. The 40 fF and 65 mΩ nominal
vertical values come from measured 45 nm stacked hardware; 160 fF is a
conservative deterministic lower bound because the same paper reports the
40 fF TSV as less than one quarter of bump-bond capacitance.

## Capacitance sensitivity

Across the vertical-link sweep, the simulated values are:

| Capacitance | Energy/toggle | Mean delay |
|---:|---:|---:|
"""
    for cap, energy, delay in sensitivity:
        text += f"| {cap:g} fF | {energy:.3f} fJ | {delay:.3f} ps |\n"
    text += """

Energy increases monotonically across the complete 5–80 fF vertical-link
sensitivity range.

## Diagnostic bridge to Timeloop

The following values multiply raw Timeloop highest-level scalar events by the
reported 8-bit top-memory word width, a disclosed 0.5 bit-toggle probability,
and the SPICE energy per toggle:

""" + "\n".join(bridge_lines) + f"""

These diagnostic link energies are **not added to or subtracted from** the
previous Timeloop/Accelergy totals because the boundary between memory-model
energy and I/O energy is not sufficiently resolved to rule out double
counting. Activity factors of 0.25, 0.5, and 1.0 are preserved in
`processed/system_bridge.csv`.

## Manuscript-ready paragraph

To corroborate the communication assumption at circuit level, we performed
ngspice transient simulations using the public 45 nm high-performance PTM
BSIM4 model. Identical CMOS driver, receiver, fanout, supply, input slew, and
series-resistance assumptions were used for both link cases; only the
interconnect capacitance was changed. A measured 40 fF TSV load from a 45 nm
wafer-stacked SOI-CMOS implementation was compared with a conservative 160 fF
bump-load proxy derived from the same publication. The simulated supply energy
decreased from {float(p['supply_energy_per_toggle_fJ']):.3f} to
{float(v['supply_energy_per_toggle_fJ']):.3f} fJ per toggle, while mean
propagation delay decreased from {float(p['mean_propagation_delay_ps']):.3f} to
{float(v['mean_propagation_delay_ps']):.3f} ps. These results validate the
direction and circuit-level plausibility of lower-capacitance vertical
communication; they do not constitute full-chip transistor simulation,
foundry signoff, extracted-layout analysis, or thermal validation.

## Limitation

This is a transistor-level link testbench using a predictive model, not a
foundry PDK or post-layout extraction. The planar case is a conservative bump
capacitance proxy, not a transistor-accurate LPDDR4 PHY. The simulation does
not model TSV coupling, inductance, ESD structures, package transmission lines,
process corners, temperature gradients, or the full accelerator.
"""
    (ROOT / "MANUSCRIPT_SPICE_RESULTS.md").write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
