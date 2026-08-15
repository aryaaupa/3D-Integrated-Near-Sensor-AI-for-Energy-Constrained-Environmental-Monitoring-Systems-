#!/usr/bin/env python3
"""Extend the frozen planar/localized experiment to repository AlexNet layers 3-5.

This script reuses the original input builder and result parser.  It changes no
architecture, precision, energy accounting, or planar-to-localized comparison
rule.  Each new layer is mapped once on the planar reference and that mapping is
then frozen for both model runs.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import re
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yaml


REPO = Path(__file__).resolve().parents[3]
EXP = Path(__file__).resolve().parents[1]
SCRIPTS = EXP / "scripts"
NEW = (
    "alexnet_conv3",
    "alexnet_conv4_dense",
    "alexnet_conv5_dense",
)
ALL = (
    "alexnet_conv1_activation_intensive",
    "alexnet_conv2_compute_intensive",
    *NEW,
)
DISPLAY = {
    "alexnet_conv1_activation_intensive": "CONV1",
    "alexnet_conv2_compute_intensive": "CONV2",
    "alexnet_conv3": "CONV3",
    "alexnet_conv4_dense": "CONV4",
    "alexnet_conv5_dense": "CONV5",
}
REQUIRED = (
    "timeloop-model.stats.txt",
    "timeloop-model.map.txt",
    "timeloop-model.map+stats.xml",
    "timeloop-model.ERT.yaml",
    "timeloop-model.ART.yaml",
    "timeloop-model.accelergy.log",
    "stdout_stderr.txt",
    "input.yaml",
)


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def configure_builder():
    builder = load_module("frozen_build_inputs", "build_inputs.py")
    for layer, slug in ((3, NEW[0]), (4, NEW[1]), (5, NEW[2])):
        builder.WORKLOADS[slug] = {
            "display_name": (
                f"AlexNet CONV{layer}" if layer == 3
                else f"AlexNet-derived dense CONV{layer} configuration"
            ),
            "source": REPO / f"workspace/example_designs/layer_shapes/CONV/AlexNet/AlexNet_layer{layer}.yaml",
            "classification": "workload-dependence extension",
        }
    return builder


def run(command: list[str], cwd: Path, log: Path) -> None:
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w") as stream:
        stream.write("COMMAND=" + " ".join(command) + "\n")
        completed = subprocess.run(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT)
        stream.write(f"\nEXIT_STATUS={completed.returncode}\n")
    if completed.returncode:
        raise subprocess.CalledProcessError(completed.returncode, command)


def validate_run(run_dir: Path, prefix: str) -> None:
    required = (
        f"{prefix}.stats.txt", f"{prefix}.map.txt", f"{prefix}.map+stats.xml",
        f"{prefix}.ERT.yaml", f"{prefix}.ART.yaml", f"{prefix}.accelergy.log",
        "stdout_stderr.txt", "input.yaml",
    )
    for filename in required:
        path = run_dir / filename
        if not path.is_file() or path.stat().st_size == 0:
            print(f"RUN_DIRECTORY_CONTENTS={sorted(p.name for p in run_dir.iterdir())}")
            log = run_dir / "stdout_stderr.txt"
            if log.is_file():
                print(f"--- {log} ---")
                print(log.read_text(errors="replace"))
            raise FileNotFoundError(path)
    combined = (run_dir / "stdout_stderr.txt").read_text(errors="replace")
    combined += (run_dir / f"{prefix}.accelergy.log").read_text(errors="replace")
    if "EXIT_STATUS=0" not in combined:
        raise RuntimeError(f"Missing exit-zero marker in {run_dir}")
    if re.search(r"encountered an error|failed to run accelergy|traceback|(^|\s)error([:\s]|$)",
                 combined, re.IGNORECASE | re.MULTILINE):
        raise RuntimeError(f"Error marker found in {run_dir}")


def execute() -> None:
    builder = configure_builder()
    builder.prepare()
    config = REPO / "ieee_revision/setup_evidence/accelergy_config.yaml"
    manifest = EXP / "logs/workload_extension_manifest.tsv"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text("kind\tworkload\tarchitecture\texit_status\n")

    for workload in NEW:
        run_dir = EXP / "raw_outputs/mapping_search" / workload
        run_dir.mkdir(parents=True, exist_ok=True)
        input_path = EXP / "planar" / f"{workload}_mapper_input.yaml"
        (run_dir / "accelergy_config.yaml").write_bytes(config.read_bytes())
        (run_dir / "input.yaml").write_bytes(input_path.read_bytes())
        run(["timeloop-mapper", "input.yaml"], run_dir, run_dir / "stdout_stderr.txt")
        validate_run(run_dir, "timeloop-mapper")
        (run_dir / "completed.marker").write_text("PASS\n")
        with manifest.open("a") as stream:
            stream.write(f"mapping_search\t{workload}\tplanar\t0\n")

    builder.finalize()
    for workload in NEW:
        for architecture in ("planar", "integrated_3d"):
            run_dir = EXP / "raw_outputs" / workload / architecture
            run_dir.mkdir(parents=True, exist_ok=True)
            input_path = EXP / architecture / f"{workload}_model_input.yaml"
            (run_dir / "accelergy_config.yaml").write_bytes(config.read_bytes())
            (run_dir / "input.yaml").write_bytes(input_path.read_bytes())
            run(["timeloop-model", "input.yaml"], run_dir, run_dir / "stdout_stderr.txt")
            validate_run(run_dir, "timeloop-model")
            (run_dir / "completed.marker").write_text("PASS\n")
            with manifest.open("a") as stream:
                stream.write(f"main\t{workload}\t{architecture}\t0\n")

    extractor = load_module("frozen_extract_results", "extract_results.py")
    extractor.WORKLOADS = ALL
    extractor.main()


def validate() -> None:
    validator = load_module("frozen_validate_helpers", "validate_results.py")
    results = { (r["workload"], r["architecture"]): r
                for r in csv.DictReader((EXP / "processed/results.csv").open()) }
    comparisons = {r["workload"]: r
                   for r in csv.DictReader((EXP / "processed/comparison.csv").open())}
    trace = list(csv.DictReader((EXP / "processed/traceability.csv").open()))
    checks = []
    assert len(results) == 2 * len(ALL)
    assert len(trace) == 16 * 2 * len(ALL)

    for workload in ALL:
        docs = {}
        for architecture in ("planar", "integrated_3d"):
            run_dir = EXP / "raw_outputs" / workload / architecture
            for filename in REQUIRED:
                path = run_dir / filename
                assert path.is_file() and path.stat().st_size > 0, path
            validate_run(run_dir, "timeloop-model")
            docs[architecture] = yaml.safe_load((run_dir / "input.yaml").read_text())
            row = results[(workload, architecture)]
            assert float(row["total_energy_pJ"]) >= 0
            assert float(row["energy_per_compute_pJ"]) >= 0
            assert 0 <= float(row["utilization"]) <= 1

        p = results[(workload, "planar")]
        s = results[(workload, "integrated_3d")]
        assert docs["planar"]["problem"] == docs["integrated_3d"]["problem"]
        assert validator.normalized_mapping(docs["planar"]) == validator.normalized_mapping(docs["integrated_3d"])
        assert validator.architecture_without_top(docs["planar"]) == validator.architecture_without_top(docs["integrated_3d"])
        assert validator.find_component(docs["planar"], "mac[") == validator.find_component(docs["integrated_3d"], "mac[")
        assert int(p["total_MACs"]) == int(s["total_MACs"])
        assert int(p["cycles"]) == int(s["cycles"])
        assert math.isclose(float(p["utilization"]), float(s["utilization"]), abs_tol=1e-8)
        expected = (float(p["total_energy_pJ"]) - float(s["total_energy_pJ"])) / float(p["total_energy_pJ"]) * 100
        assert math.isclose(float(comparisons[workload]["total_energy_reduction_percent"]),
                            expected, rel_tol=1e-7, abs_tol=1e-7)
        checks.append(f"PASS {workload}: raw outputs complete; problem, mapping, compute, MACs, cycles, and utilization match")

    for row in trace:
        for source in row["raw_source_file"].split("; "):
            assert (REPO / source).is_file(), source
    checks.append("PASS traceability: every extended metric resolves to an existing raw source")
    checks.append("PASS formulas: all five energy reductions recomputed from parsed totals")
    report = EXP / "processed/workload_extension_validation.txt"
    report.write_text("\n".join(checks) + "\nWORKLOAD_EXTENSION_VALIDATION=PASS\n")
    print(report.read_text(), end="")


def plot() -> None:
    summary = {r["workload"]: r for r in csv.DictReader((EXP / "workloads/workload_summary.csv").open())}
    comparison = {r["workload"]: r for r in csv.DictReader((EXP / "processed/comparison.csv").open())}
    output_rows = []
    for workload in ALL:
        row = summary[workload]
        tensor_elements = sum(int(row[k]) for k in (
            "weight_volume_elements", "input_activation_volume_elements", "output_activation_volume_elements"))
        intensity = int(row["mac_count"]) / tensor_elements
        output_rows.append({
            "workload": workload,
            "label": DISPLAY[workload],
            "macs_per_tensor_element": f"{intensity:.8f}",
            "total_energy_reduction_percent": comparison[workload]["total_energy_reduction_percent"],
            "intensity_derivation": "mac_count/(weight_volume_elements+input_activation_volume_elements+output_activation_volume_elements)",
            "energy_source": "processed/comparison.csv from paired raw Timeloop stats",
        })

    out_csv = EXP / "processed/workload_dependence.csv"
    with out_csv.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=output_rows[0].keys())
        writer.writeheader(); writer.writerows(output_rows)

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 7, "axes.labelsize": 7,
        "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    })
    fig, ax = plt.subplots(figsize=(3.5, 2.35))
    xs = [float(r["macs_per_tensor_element"]) for r in output_rows]
    ys = [float(r["total_energy_reduction_percent"]) for r in output_rows]
    ax.scatter(xs, ys, s=28, color="#356A96", edgecolors="#20262E", linewidths=0.45, zorder=3)
    offsets = {"CONV1": (4, -10), "CONV2": (4, 5), "CONV3": (4, 5), "CONV4": (4, -10), "CONV5": (4, 5)}
    for row, x, y in zip(output_rows, xs, ys):
        ax.annotate(row["label"], (x, y), xytext=offsets[row["label"]], textcoords="offset points",
                    fontsize=6.2, fontweight="bold")
    ax.set_xlabel("Architecture-oriented intensity (MACs per tensor element)")
    ax.set_ylabel("Planar-to-localized energy reduction (%)")
    ax.set_ylim(0, max(75, math.ceil(max(ys) / 5) * 5 + 5))
    ax.grid(True, color="#D8DADD", linewidth=0.45, zorder=0)
    for spine in ax.spines.values(): spine.set_linewidth(0.65)
    fig.subplots_adjust(left=0.17, right=0.98, bottom=0.20, top=0.98)
    out = EXP / "figures/workload_dependence"
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.02)
    fig.savefig(out.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.02)
    fig.savefig(out.with_suffix(".png"), dpi=600, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)

    lines = [
        "# Five-layer workload-dependence extension", "",
        "The table and figure are generated from the five paired Timeloop/Accelergy runs. No regression or trend line is fitted.", "",
        "| Layer | MACs/tensor element | Planar-to-localized energy reduction |", "|---|---:|---:|",
    ]
    for row in output_rows:
        lines.append(f"| {row['label']} | {float(row['macs_per_tensor_element']):.2f} | {float(row['total_energy_reduction_percent']):.2f}% |")
    lines += [
        "", "**Caption:** Workload dependence of the controlled memory-localization experiment. The x-axis is the deterministic architecture-oriented intensity indicator, defined as MAC count divided by the sum of weight, input-activation, and output-activation tensor elements. The y-axis is the planar-to-localized Timeloop/Accelergy total-energy reduction under a separately frozen planar mapping for each layer. Points are shown individually; no statistical relationship is fitted or claimed.",
        "", "**Insertion:** Place in the Results section immediately after the per-workload energy comparison. It supports only the observation that the benefit varies across the five evaluated layer configurations; it does not establish a universal intensity-energy law.", "",
    ]
    (EXP / "WORKLOAD_DEPENDENCE.md").write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("execute", "validate", "plot"))
    args = parser.parse_args()
    {"execute": execute, "validate": validate, "plot": plot}[args.phase]()


if __name__ == "__main__":
    main()
