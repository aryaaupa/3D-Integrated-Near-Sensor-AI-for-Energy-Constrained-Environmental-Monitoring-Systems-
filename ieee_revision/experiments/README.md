# Reproducible planar versus 3D-proxy Timeloop/Accelergy evaluation

This directory contains a minimal two-workload, two-architecture comparison
based on the verified environment in `ieee_revision/setup_evidence/`.

## Design

- **Planar:** official Eyeriss-like 168-PE int16 architecture with external
  LPDDR4 as the highest memory level.
- **Integrated 3D proxy:** identical workload, PE array, precision, lower
  buffers, loop factors, permutations, and clock; the LPDDR4 level is replaced
  by a 2 MiB CACTI-backed localized stacked SRAM.
- **Workloads:** AlexNet CONV1 (activation/memory-intensive relative to the
  second case) and AlexNet CONV2 (relatively compute-intensive).

This is not a transistor-level, physical TSV, or thermal simulation. It models
the architectural energy consequence of terminating high-level data traffic in
localized SRAM rather than external DRAM.

## Reproduction

From the repository root in the verified workspace:

```bash
source /workspace/scratch/ae4887560717/timeloop-env/bin/activate
python -m pip install -r ieee_revision/experiments/scripts/requirements.txt
ieee_revision/experiments/scripts/run_experiments.sh
python ieee_revision/experiments/scripts/extract_results.py
python ieee_revision/experiments/scripts/validate_results.py
python ieee_revision/experiments/scripts/plot_results.py
python ieee_revision/experiments/scripts/write_manuscript_results.py
```

The run script first maps each workload on the planar reference, then freezes
that mapping for both main cases. It refuses to overwrite a completed raw run.
Raw outputs from each run are isolated below `raw_outputs/`.

## Outputs

- `workloads/workload_summary.csv`: deterministic workload dimensions/volumes
- `planar/`, `integrated_3d/`: complete mapper/model inputs
- `raw_outputs/mapping_search/`: planar mapping-search evidence
- `raw_outputs/<workload>/<architecture>/`: four main raw runs
- `raw_outputs/sensitivity/`: four capacity-sensitivity raw runs
- `processed/results.csv`: parsed absolute metrics
- `processed/comparison.csv`: deterministic planar-to-3D formulas
- `processed/sensitivity.csv`: capacity sensitivity
- `processed/traceability.csv`: per-metric raw-source mapping
- `processed/validation_report.txt`: fairness and sanity-check results
- `figures/`: PDF and 300-dpi PNG figures generated from CSV files
- `MANUSCRIPT_RESULTS.md`: CSV-generated manuscript-ready findings

Energy values in `results.csv` come from the Timeloop stats Summary section;
component breakdowns and access counts are parsed from named component blocks.
The parser converts µJ to pJ and fJ/compute to pJ/compute. Latency uses the
documented 1 ns clock period. See `assumptions.md` for every parameter source.

## Important interpretation

The fixed mapping produces the same number of highest-level events in both
cases. The 3D proxy redirects them from external DRAM to local stacked SRAM;
therefore external DRAM traffic is eliminated in the proxy while total
highest-level events are unchanged. Cycles and latency are also unchanged.
Separately reported network/interconnect energy is unavailable and recorded as
`NA`, not zero.
