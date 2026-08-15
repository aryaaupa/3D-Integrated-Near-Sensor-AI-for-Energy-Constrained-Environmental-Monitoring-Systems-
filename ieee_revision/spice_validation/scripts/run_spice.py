#!/usr/bin/env python3
"""Generate isolated netlists and execute all transistor-level link cases."""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "netlists" / "link_driver_template.cir"
MODEL = ROOT / "models" / "45nm_HP.pm"
RAW = ROOT / "raw_outputs"
LOGS = ROOT / "logs"

CASES = [
    # The nominal 40 fF / 0.065 ohm TSV is measured 45 nm hardware.
    {"name": "vertical_5fF", "architecture": "vertical", "c_ff": 5.0, "r_ohm": 0.065, "role": "sensitivity"},
    {"name": "vertical_20fF", "architecture": "vertical", "c_ff": 20.0, "r_ohm": 0.065, "role": "sensitivity"},
    {"name": "vertical_40fF", "architecture": "vertical", "c_ff": 40.0, "r_ohm": 0.065, "role": "nominal"},
    {"name": "vertical_80fF", "architecture": "vertical", "c_ff": 80.0, "r_ohm": 0.065, "role": "sensitivity"},
    # The source states 40 fF is less than one quarter of bump capacitance.
    # Exactly 160 fF is therefore a conservative lower-bound planar proxy.
    {"name": "planar_bump_160fF", "architecture": "planar", "c_ff": 160.0, "r_ohm": 0.065, "role": "nominal"},
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ngspice", required=True, type=Path)
    parser.add_argument("--library-dir", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    if not args.ngspice.is_file():
        raise SystemExit(f"ngspice executable not found: {args.ngspice}")
    RAW.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    template = TEMPLATE.read_text(encoding="utf-8")
    manifest_rows = []
    env = os.environ.copy()
    if args.library_dir:
        env["LD_LIBRARY_PATH"] = str(args.library_dir)

    for case in CASES:
        out = RAW / case["name"]
        marker = out / "completed.marker"
        if marker.exists() and not args.overwrite:
            raise SystemExit(f"refusing to overwrite completed run: {out}")
        out.mkdir(parents=True, exist_ok=True)
        netlist = template.replace("{{CASE_NAME}}", case["name"])
        netlist = netlist.replace("{{R_LINK_OHM}}", str(case["r_ohm"]))
        netlist = netlist.replace("{{C_LINK_FF}}", str(case["c_ff"]))
        (out / "input.cir").write_text(netlist, encoding="utf-8")
        shutil.copyfile(MODEL, out / "model.pm")
        started = datetime.now(timezone.utc)
        proc = subprocess.run(
            [str(args.ngspice), "-b", "input.cir"],
            cwd=out,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        (out / "ngspice_stdout_stderr.txt").write_text(proc.stdout, encoding="utf-8")
        finished = datetime.now(timezone.utc)
        if proc.returncode != 0:
            raise SystemExit(f"{case['name']} failed with exit {proc.returncode}")
        required = [out / "waveform.txt", out / "ngspice_stdout_stderr.txt"]
        if not all(path.is_file() and path.stat().st_size > 0 for path in required):
            raise SystemExit(f"{case['name']} did not generate nonempty raw outputs")
        marker.write_text(
            f"EXIT_STATUS=0\nSTARTED_UTC={started.isoformat()}\nFINISHED_UTC={finished.isoformat()}\n",
            encoding="utf-8",
        )
        manifest_rows.append({
            **case,
            "exit_status": 0,
            "started_utc": started.isoformat(),
            "finished_utc": finished.isoformat(),
            "netlist_sha256": sha256(out / "input.cir"),
            "model_sha256": sha256(out / "model.pm"),
        })

    with (LOGS / "run_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest_rows[0]))
        writer.writeheader()
        writer.writerows(manifest_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
