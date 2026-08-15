# Reproducible transistor-level communication validation

This directory supplements, but does not replace, the verified architectural
evaluation in `ieee_revision/experiments/`. It contains real ngspice transient
simulations of one identical 45 nm CMOS driver/receiver path under two
interconnect-loading conditions:

- nominal vertical TSV: 40 fF, 65 mΩ;
- conservative planar bump proxy: 160 fF, 65 mΩ.

Only link capacitance changes in the nominal comparison. Using the same series
resistance deliberately avoids inventing a planar resistance and biases the
test against overstating the vertical advantage.

## Reproduce

From the repository root, with the previously verified Python environment:

```bash
source /workspace/scratch/ae4887560717/timeloop-env/bin/activate
python -m pip install -r ieee_revision/spice_validation/scripts/requirements.txt
ieee_revision/spice_validation/scripts/run_all.sh --overwrite
```

`bootstrap_ngspice.sh` downloads two hash-pinned Ubuntu 24.04 packages into
`/tmp`, extracts them without modifying the system Python or Timeloop
environment, and verifies ngspice before execution. The 45 nm PTM model is
committed verbatim with its source hash.

## Evidence map

- `models/`: exact public PTM model card
- `netlists/`: single fair-comparison template
- `raw_outputs/`: generated input, model, waveform, simulator log, and marker
  for all five runs
- `processed/link_results.csv`: values parsed from ngspice `.measure` output
- `processed/link_comparison.csv`: nominal deterministic differences
- `processed/system_bridge.csv`: disclosed activity-factor bridge to Timeloop
- `processed/traceability.csv`: raw-source mapping
- `processed/validation_report.txt`: fail-closed validation output
- `figures/`: CSV/waveform-generated PDF and PNG figures
- `MANUSCRIPT_SPICE_RESULTS.md`: CSV-generated wording and limitations

This study validates a representative communication primitive. It is not a
full-accelerator transistor simulation or a claim of silicon measurement.
