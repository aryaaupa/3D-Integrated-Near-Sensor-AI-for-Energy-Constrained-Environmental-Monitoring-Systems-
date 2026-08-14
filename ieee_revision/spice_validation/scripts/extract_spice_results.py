#!/usr/bin/env python3
"""Parse raw ngspice logs; never transcribe measurements manually."""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw_outputs"
PROCESSED = ROOT / "processed"
MANIFEST = ROOT / "logs" / "run_manifest.csv"
METRICS = ("supply_charge_cycle", "propagation_rise", "propagation_fall", "link_fall_time", "link_rise_time")
PATTERN = re.compile(r"^(%s)\s*=\s*([-+0-9.eE]+)" % "|".join(METRICS), re.MULTILINE)


def fmt(value: float) -> str:
    return format(value, ".12g")


def main() -> int:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    rows = []
    trace = []
    with MANIFEST.open(newline="", encoding="utf-8") as handle:
        manifest = list(csv.DictReader(handle))
    for case in manifest:
        source = RAW / case["name"] / "ngspice_stdout_stderr.txt"
        text = source.read_text(encoding="utf-8")
        parsed = {name: float(value) for name, value in PATTERN.findall(text)}
        missing = set(METRICS) - set(parsed)
        if missing:
            raise SystemExit(f"missing measurements in {source}: {sorted(missing)}")
        # I(VDD) is negative when the source delivers current. At exactly 1 V,
        # -integral(I(VDD)dt) is joules per 1 ns cycle; divide by two toggles.
        energy_cycle_j = -parsed["supply_charge_cycle"]
        energy_toggle_fj = energy_cycle_j * 1e15 / 2.0
        delay_rise_ps = parsed["propagation_rise"] * 1e12
        delay_fall_ps = parsed["propagation_fall"] * 1e12
        row = {
            "case": case["name"],
            "architecture": case["architecture"],
            "role": case["role"],
            "link_capacitance_fF": fmt(float(case["c_ff"])),
            "link_resistance_ohm": fmt(float(case["r_ohm"])),
            "supply_energy_per_cycle_fJ": fmt(energy_cycle_j * 1e15),
            "supply_energy_per_toggle_fJ": fmt(energy_toggle_fj),
            "propagation_rise_ps": fmt(delay_rise_ps),
            "propagation_fall_ps": fmt(delay_fall_ps),
            "mean_propagation_delay_ps": fmt((delay_rise_ps + delay_fall_ps) / 2.0),
            "link_rise_time_ps": fmt(parsed["link_rise_time"] * 1e12),
            "link_fall_time_ps": fmt(parsed["link_fall_time"] * 1e12),
        }
        rows.append(row)
        for metric, value in row.items():
            if metric in {"case", "architecture", "role"}:
                continue
            method = "manifest parameter" if metric in {"link_capacitance_fF", "link_resistance_ohm"} else "parsed ngspice .measure; deterministic unit conversion"
            raw_source = ROOT / ("logs/run_manifest.csv" if method == "manifest parameter" else source.relative_to(ROOT))
            trace.append({
                "case": case["name"], "metric": metric, "value": value,
                "raw_source_file": str(raw_source.relative_to(ROOT)), "extraction_method": method,
            })

    fields = list(rows[0])
    with (PROCESSED / "link_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)

    nominal = {r["architecture"]: r for r in rows if r["role"] == "nominal"}
    planar, vertical = nominal["planar"], nominal["vertical"]
    pe = float(planar["supply_energy_per_toggle_fJ"])
    ve = float(vertical["supply_energy_per_toggle_fJ"])
    pd = float(planar["mean_propagation_delay_ps"])
    vd = float(vertical["mean_propagation_delay_ps"])
    comparison = [{
        "planar_case": planar["case"], "vertical_case": vertical["case"],
        "energy_per_toggle_reduction_percent": fmt((pe - ve) / pe * 100.0),
        "mean_delay_reduction_percent": fmt((pd - vd) / pd * 100.0),
        "capacitance_reduction_percent": fmt((float(planar["link_capacitance_fF"]) - float(vertical["link_capacitance_fF"])) / float(planar["link_capacitance_fF"]) * 100.0),
    }]
    with (PROCESSED / "link_comparison.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(comparison[0])); writer.writeheader(); writer.writerows(comparison)

    with (PROCESSED / "traceability.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(trace[0])); writer.writeheader(); writer.writerows(trace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
