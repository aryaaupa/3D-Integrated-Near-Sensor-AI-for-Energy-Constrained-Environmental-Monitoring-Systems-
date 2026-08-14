#!/usr/bin/env python3
"""Traceably combine SPICE toggle energy with Timeloop scalar event counts."""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT.parent / "experiments"
PROCESSED = ROOT / "processed"
ACTIVITY_FACTORS = (0.25, 0.5, 1.0)


def fmt(value: float) -> str:
    return format(value, ".12g")


def main() -> int:
    with (PROCESSED / "link_results.csv").open(newline="", encoding="utf-8") as handle:
        link_rows = list(csv.DictReader(handle))
    nominal_link = {r["architecture"]: r for r in link_rows if r["role"] == "nominal"}
    with (EXPERIMENTS / "processed/results.csv").open(newline="", encoding="utf-8") as handle:
        system_rows = list(csv.DictReader(handle))

    rows = []
    for system in system_rows:
        link_arch = "planar" if system["architecture"] == "planar" else "vertical"
        link = nominal_link[link_arch]
        stats = EXPERIMENTS / "raw_outputs" / system["workload"] / system["architecture"] / "timeloop-model.stats.txt"
        text = stats.read_text(encoding="utf-8")
        top_name = "DRAM" if system["architecture"] == "planar" else "stacked_sram"
        word_match = re.search(
            rf"=== {re.escape(top_name)} ===.*?Word bits\s*:\s*(\d+)",
            text,
            flags=re.DOTALL,
        )
        if not word_match:
            raise SystemExit(f"Word bits missing in {stats}")
        word_bits = int(word_match.group(1))
        events = int(system["highest_level_reads"]) + int(system["highest_level_writes"])
        toggle_fj = float(link["supply_energy_per_toggle_fJ"])
        system_energy_uj = float(system["total_energy_pJ"]) / 1e6
        for activity in ACTIVITY_FACTORS:
            toggled_bits = events * word_bits * activity
            link_energy_uj = toggled_bits * toggle_fj * 1e-9
            rows.append({
                "workload": system["workload"],
                "architecture": system["architecture"],
                "spice_link_case": link["case"],
                "timeloop_highest_level_scalar_events": events,
                "timeloop_word_bits": word_bits,
                "assumed_bit_toggle_probability": fmt(activity),
                "estimated_toggled_bits": fmt(toggled_bits),
                "spice_energy_per_toggle_fJ": link["supply_energy_per_toggle_fJ"],
                "diagnostic_link_energy_uJ": fmt(link_energy_uj),
                "timeloop_accelergy_total_energy_uJ": fmt(system_energy_uj),
                "diagnostic_link_energy_fraction_percent": fmt(link_energy_uj / system_energy_uj * 100.0),
                "timeloop_raw_source_file": str(stats.relative_to(ROOT.parent.parent)),
                "spice_raw_source_file": f"ieee_revision/spice_validation/raw_outputs/{link['case']}/ngspice_stdout_stderr.txt",
            })
    with (PROCESSED / "system_bridge.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
