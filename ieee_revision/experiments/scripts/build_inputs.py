#!/usr/bin/env python3
"""Build reproducible planar and fixed-mapping 3D-proxy Timeloop inputs."""

from __future__ import annotations

import argparse
import csv
import copy
from pathlib import Path

from ruamel.yaml import YAML


REPO = Path(__file__).resolve().parents[3]
EXP = Path(__file__).resolve().parents[1]
TEMPLATE = (
    REPO
    / "workspace/tutorial_exercises/01_accelergy_timeloop_2020_ispass"
    / "timeloop+accelergy/ref-output/intmac/parsed-processed-input.yaml"
)

WORKLOADS = {
    "alexnet_conv1_activation_intensive": {
        "display_name": "AlexNet CONV1 (activation/memory-intensive)",
        "source": REPO / "workspace/example_designs/layer_shapes/CONV/AlexNet/AlexNet_layer1.yaml",
        "classification": "activation/memory-intensive",
    },
    "alexnet_conv2_compute_intensive": {
        "display_name": "AlexNet CONV2 (compute-intensive)",
        "source": REPO / "workspace/example_designs/layer_shapes/CONV/AlexNet/AlexNet_layer2.yaml",
        "classification": "relatively compute-intensive",
    },
}

STACKED_DEPTHS = {
    "2MiB": 262_144,
    "4MiB": 524_288,
    "8MiB": 1_048_576,
    "16MiB": 2_097_152,
}


def yaml_rt() -> YAML:
    yaml = YAML(typ="rt")
    yaml.preserve_quotes = True
    yaml.width = 100
    return yaml


def load_yaml(path: Path):
    with path.open() as stream:
        return yaml_rt().load(stream)


def dump_yaml(data, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as stream:
        yaml_rt().dump(data, stream)


def dimensions(instance: dict) -> dict:
    c = int(instance["C"])
    m = int(instance["M"])
    p = int(instance["P"])
    q = int(instance["Q"])
    r = int(instance["R"])
    s = int(instance["S"])
    n = int(instance.get("N", 1))
    hs = int(instance.get("Hstride", 1))
    ws = int(instance.get("Wstride", 1))
    hd = int(instance.get("Hdilation", 1))
    wd = int(instance.get("Wdilation", 1))
    input_h = (p - 1) * ws + (r - 1) * wd + 1
    input_w = (q - 1) * hs + (s - 1) * hd + 1
    return {
        "batch": n,
        "input_height": input_h,
        "input_width": input_w,
        "input_channels": c,
        "output_height": p,
        "output_width": q,
        "output_channels": m,
        "kernel_height": r,
        "kernel_width": s,
        "stride_height": hs,
        "stride_width": ws,
        "mac_count": n * c * m * r * s * p * q,
        "weight_volume_elements": c * m * r * s,
        "input_activation_volume_elements": n * c * input_h * input_w,
        "output_activation_volume_elements": n * m * p * q,
    }


def write_workload_summary(rows: list[dict]) -> None:
    fieldnames = [
        "workload",
        "classification",
        "source_file",
        "batch",
        "input_height",
        "input_width",
        "input_channels",
        "output_height",
        "output_width",
        "output_channels",
        "kernel_height",
        "kernel_width",
        "stride_height",
        "stride_width",
        "mac_count",
        "weight_volume_elements",
        "input_activation_volume_elements",
        "output_activation_volume_elements",
    ]
    output = EXP / "workloads/workload_summary.csv"
    with output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def prepare() -> None:
    rows = []
    for slug, metadata in WORKLOADS.items():
        base = load_yaml(TEMPLATE)
        workload_doc = load_yaml(metadata["source"])
        base["problem"] = copy.deepcopy(workload_doc["problem"])
        base["problem"]["instance"].setdefault("N", 1)
        base["problem"]["instance"].setdefault("Hstride", 1)
        base["problem"]["instance"].setdefault("Wstride", 1)
        base["problem"]["instance"].setdefault("Hdilation", 1)
        base["problem"]["instance"].setdefault("Wdilation", 1)
        dump_yaml(base, EXP / f"planar/{slug}_mapper_input.yaml")

        row = {
            "workload": slug,
            "classification": metadata["classification"],
            "source_file": str(metadata["source"].relative_to(REPO)),
        }
        row.update(dimensions(base["problem"]["instance"]))
        rows.append(row)
    write_workload_summary(rows)


def fixed_model_input(mapper_input: Path, mapping_file: Path):
    data = load_yaml(mapper_input)
    mapping = load_yaml(mapping_file)
    data["mapping"] = copy.deepcopy(mapping["mapping"])
    for key in ("architecture_constraints", "mapper", "mapspace"):
        data.pop(key, None)
    return data


def make_stacked_variant(planar, depth: int):
    variant = copy.deepcopy(planar)
    local = variant["architecture"]["subtree"][0]["local"]
    top = next(component for component in local if str(component["name"]).startswith("DRAM["))
    top["name"] = "stacked_sram[1..1]"
    top["class"] = "smartbuffer_SRAM"
    attrs = top["attributes"]
    attrs.pop("type", None)
    attrs["depth"] = depth
    attrs["width"] = 64
    attrs["n_banks"] = 32
    attrs["datawidth"] = 8
    # Match the official top-level DRAM's unconstrained bandwidth so that the
    # controlled comparison changes memory technology/placement, not cycles.
    attrs.pop("read_bandwidth", None)
    attrs.pop("write_bandwidth", None)
    for entry in variant["mapping"]:
        if entry.get("target") == "DRAM":
            entry["target"] = "stacked_sram"
    return variant


def finalize() -> None:
    sensitivity_slug = "alexnet_conv1_activation_intensive"
    for slug in WORKLOADS:
        mapper_input = EXP / f"planar/{slug}_mapper_input.yaml"
        mapping = EXP / f"raw_outputs/mapping_search/{slug}/timeloop-mapper.map.yaml"
        if not mapping.is_file() or mapping.stat().st_size == 0:
            raise FileNotFoundError(f"Missing successful mapper output: {mapping}")
        fixed = fixed_model_input(mapper_input, mapping)
        dump_yaml(fixed, EXP / f"planar/{slug}_model_input.yaml")
        dump_yaml({"mapping": fixed["mapping"]}, EXP / f"workloads/{slug}_fixed_mapping.yaml")

        stacked = make_stacked_variant(fixed, STACKED_DEPTHS["2MiB"])
        dump_yaml(stacked, EXP / f"integrated_3d/{slug}_model_input.yaml")

        if slug == sensitivity_slug:
            for label, depth in STACKED_DEPTHS.items():
                variant = make_stacked_variant(fixed, depth)
                dump_yaml(
                    variant,
                    EXP / f"integrated_3d/sensitivity/{slug}_{label}_model_input.yaml",
                )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare", "finalize"))
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare()
    else:
        finalize()


if __name__ == "__main__":
    main()
