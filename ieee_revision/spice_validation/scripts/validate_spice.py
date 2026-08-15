#!/usr/bin/env python3
"""Fail closed on missing, inconsistent, or physically invalid SPICE evidence."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw_outputs"
PROCESSED = ROOT / "processed"
MODEL_SHA = "c9ed2e513523c57a76912a35b2860cb85e4aaa3402b69757d84efa9cc2fb8410"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    messages = []
    with (ROOT / "logs/run_manifest.csv").open(newline="", encoding="utf-8") as handle:
        manifest = list(csv.DictReader(handle))
    if len(manifest) != 5 or any(row["exit_status"] != "0" for row in manifest):
        raise SystemExit("expected five successful SPICE runs")
    for row in manifest:
        out = RAW / row["name"]
        required = ["input.cir", "model.pm", "waveform.txt", "ngspice_stdout_stderr.txt", "completed.marker"]
        for name in required:
            path = out / name
            if not path.is_file() or path.stat().st_size == 0:
                raise SystemExit(f"missing or empty: {path}")
        if digest(out / "model.pm") != MODEL_SHA:
            raise SystemExit(f"model hash mismatch: {out / 'model.pm'}")
        log = (out / "ngspice_stdout_stderr.txt").read_text(encoding="utf-8", errors="replace").lower()
        if "error" in log or "failed" in log:
            raise SystemExit(f"ngspice error text in {out}")
        messages.append(f"PASS {row['name']}: exit 0, nonempty raw evidence, exact PTM model hash")

    with (PROCESSED / "link_results.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        positive = ["supply_energy_per_cycle_fJ", "supply_energy_per_toggle_fJ", "propagation_rise_ps", "propagation_fall_ps", "mean_propagation_delay_ps", "link_rise_time_ps", "link_fall_time_ps"]
        if any(float(row[key]) <= 0 for key in positive):
            raise SystemExit(f"nonpositive measured result: {row['case']}")
    ordered = sorted((float(r["link_capacitance_fF"]), float(r["supply_energy_per_toggle_fJ"])) for r in rows)
    if any(b[1] <= a[1] for a, b in zip(ordered, ordered[1:])):
        raise SystemExit("energy is not strictly increasing with link capacitance")
    messages.append("PASS results: positive measurements and monotonic energy-capacitance sensitivity")

    nominal = {r["architecture"]: r for r in rows if r["role"] == "nominal"}
    if set(nominal) != {"planar", "vertical"}:
        raise SystemExit("missing nominal planar or vertical case")
    p, v = nominal["planar"], nominal["vertical"]
    if not (float(v["supply_energy_per_toggle_fJ"]) < float(p["supply_energy_per_toggle_fJ"])):
        raise SystemExit("nominal vertical energy must be below conservative planar proxy")
    messages.append("PASS fairness: nominal netlists differ only in case label and CLINK")

    p_lines = (RAW / p["case"] / "input.cir").read_text().splitlines()
    v_lines = (RAW / v["case"] / "input.cir").read_text().splitlines()
    normalize = lambda lines: [line for line in lines if not line.startswith("* planar_") and not line.startswith("* vertical_") and not line.startswith(".param CLINK=")]
    if normalize(p_lines) != normalize(v_lines):
        raise SystemExit("nominal circuit mismatch beyond CLINK")

    with (PROCESSED / "traceability.csv").open(newline="", encoding="utf-8") as handle:
        trace = list(csv.DictReader(handle))
    for row in trace:
        if not (ROOT / row["raw_source_file"]).is_file():
            raise SystemExit(f"traceability source missing: {row['raw_source_file']}")
    messages.append(f"PASS traceability: {len(trace)} metric rows point to existing sources")

    with (PROCESSED / "system_bridge.csv").open(newline="", encoding="utf-8") as handle:
        bridge = list(csv.DictReader(handle))
    if len(bridge) != 12:
        raise SystemExit("expected 12 workload/architecture/activity bridge rows")
    if any(row["timeloop_word_bits"] != "8" for row in bridge):
        raise SystemExit("highest-level Timeloop word width must be 8 bits in every bridge row")
    if any(float(row["diagnostic_link_energy_uJ"]) <= 0 for row in bridge):
        raise SystemExit("diagnostic link energy must be positive")
    messages.append("PASS bridge: 12 rows, top-memory 8-bit words, positive diagnostic link energy")
    messages.append("FINAL_VALIDATION=PASS")
    report = "\n".join(messages) + "\n"
    (PROCESSED / "validation_report.txt").write_text(report, encoding="utf-8")
    print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
