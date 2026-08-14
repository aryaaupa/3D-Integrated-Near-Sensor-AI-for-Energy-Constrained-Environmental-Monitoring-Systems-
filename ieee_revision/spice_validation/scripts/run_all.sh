#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$script_dir/.." && pwd)"
tool_dir="${SPICE_TOOL_DIR:-/tmp/timeloop_spice_toolchain}"
python_bin="${PYTHON_BIN:-python3}"

"$script_dir/bootstrap_ngspice.sh" "$tool_dir" > "$root/logs/bootstrap_ngspice.txt" 2>&1
"$python_bin" "$script_dir/run_spice.py" \
  --ngspice "$tool_dir/root/usr/bin/ngspice" \
  --library-dir "$tool_dir/root/usr/lib/x86_64-linux-gnu" "$@"
"$python_bin" "$script_dir/extract_spice_results.py"
"$python_bin" "$script_dir/bridge_timeloop.py"
"$python_bin" "$script_dir/validate_spice.py"
"$python_bin" "$script_dir/plot_spice_results.py"
"$python_bin" "$script_dir/write_spice_summary.py"
