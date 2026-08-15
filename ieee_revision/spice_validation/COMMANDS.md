# Exact commands used for the final run

All commands were executed from the repository root.

```bash
export SPICE_TOOL_DIR=/tmp/spice_validation_tools_20260814
export PYTHON_BIN=/workspace/scratch/ae4887560717/timeloop-env/bin/python
ieee_revision/spice_validation/scripts/run_all.sh --overwrite
```

The pipeline expands to:

```bash
ieee_revision/spice_validation/scripts/bootstrap_ngspice.sh "$SPICE_TOOL_DIR"
"$PYTHON_BIN" ieee_revision/spice_validation/scripts/run_spice.py \
  --ngspice "$SPICE_TOOL_DIR/root/usr/bin/ngspice" \
  --library-dir "$SPICE_TOOL_DIR/root/usr/lib/x86_64-linux-gnu" \
  --overwrite
"$PYTHON_BIN" ieee_revision/spice_validation/scripts/extract_spice_results.py
"$PYTHON_BIN" ieee_revision/spice_validation/scripts/bridge_timeloop.py
"$PYTHON_BIN" ieee_revision/spice_validation/scripts/validate_spice.py
"$PYTHON_BIN" ieee_revision/spice_validation/scripts/plot_spice_results.py
"$PYTHON_BIN" ieee_revision/spice_validation/scripts/write_spice_summary.py
```

The bootstrap script retrieves hash-pinned Ubuntu 24.04 ngspice and LibXft
packages into `/tmp`; it does not install them system-wide or alter the
Timeloop/Accelergy environment.
