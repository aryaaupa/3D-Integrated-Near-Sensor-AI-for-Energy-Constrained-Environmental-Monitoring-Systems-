#!/usr/bin/env bash
set -euo pipefail

REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
EXP="$REPO/ieee_revision/experiments"
WORKSPACE_ROOT=${WORKSPACE_ROOT:-/workspace/scratch/ae4887560717}
VENV=${VENV:-$WORKSPACE_ROOT/timeloop-env}
ACCELERGY_CONFIG_SOURCE="$REPO/ieee_revision/setup_evidence/accelergy_config.yaml"

source "$VENV/bin/activate"

for command in "accelergy -h" "timeloop-model --help" "timeloop-mapper --help"; do
  bash -c "$command" >/dev/null
done

python "$EXP/scripts/build_inputs.py" prepare
mkdir -p "$EXP/raw_outputs/mapping_search" "$EXP/logs"
printf 'kind\tworkload\tarchitecture_or_variant\texit_status\ttimestamp_utc\n' > "$EXP/logs/run_manifest.tsv"

workloads=(
  alexnet_conv1_activation_intensive
  alexnet_conv2_compute_intensive
)

validate_run() {
  local run_dir=$1
  local prefix=$2
  test -s "$run_dir/$prefix.stats.txt"
  test -s "$run_dir/$prefix.map.txt"
  test -s "$run_dir/$prefix.map+stats.xml"
  test -s "$run_dir/$prefix.ERT.yaml"
  test -s "$run_dir/$prefix.ART.yaml"
  test -s "$run_dir/$prefix.accelergy.log"
  if rg -qi 'encountered an error|failed to run accelergy|traceback|(^|[[:space:]])error([:[:space:]]|$)' \
    "$run_dir/$prefix.accelergy.log" "$run_dir/stdout_stderr.txt"; then
    echo "Error marker found in $run_dir" >&2
    return 1
  fi
}

run_mapper() {
  local workload=$1
  local run_dir="$EXP/raw_outputs/mapping_search/$workload"
  local input="$EXP/planar/${workload}_mapper_input.yaml"
  mkdir -p "$run_dir"
  test ! -e "$run_dir/completed.marker"
  cp "$ACCELERGY_CONFIG_SOURCE" "$run_dir/accelergy_config.yaml"
  cp "$input" "$run_dir/input.yaml"
  (
    cd "$run_dir"
    set +e
    timeloop-mapper input.yaml > stdout_stderr.txt 2>&1
    status=$?
    set -e
    printf '\nEXIT_STATUS=%s\n' "$status" >> stdout_stderr.txt
    test "$status" -eq 0
  )
  validate_run "$run_dir" timeloop-mapper
  printf 'mapping_search\t%s\tplanar\t0\t%s\n' "$workload" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$EXP/logs/run_manifest.tsv"
  printf 'PASS\n' > "$run_dir/completed.marker"
}

for workload in "${workloads[@]}"; do
  run_mapper "$workload"
done

python "$EXP/scripts/build_inputs.py" finalize

run_model() {
  local workload=$1
  local architecture=$2
  local input=$3
  local run_dir="$EXP/raw_outputs/$workload/$architecture"
  mkdir -p "$run_dir"
  test ! -e "$run_dir/completed.marker"
  cp "$ACCELERGY_CONFIG_SOURCE" "$run_dir/accelergy_config.yaml"
  cp "$input" "$run_dir/input.yaml"
  (
    cd "$run_dir"
    set +e
    timeloop-model input.yaml > stdout_stderr.txt 2>&1
    status=$?
    set -e
    printf '\nEXIT_STATUS=%s\n' "$status" >> stdout_stderr.txt
    test "$status" -eq 0
  )
  validate_run "$run_dir" timeloop-model
  printf 'main\t%s\t%s\t0\t%s\n' "$workload" "$architecture" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$EXP/logs/run_manifest.tsv"
  printf 'PASS\n' > "$run_dir/completed.marker"
}

for workload in "${workloads[@]}"; do
  run_model "$workload" planar "$EXP/planar/${workload}_model_input.yaml"
  run_model "$workload" integrated_3d "$EXP/integrated_3d/${workload}_model_input.yaml"
done

sensitivity_workload=alexnet_conv1_activation_intensive
for capacity in 2MiB 4MiB 8MiB 16MiB; do
  input="$EXP/integrated_3d/sensitivity/${sensitivity_workload}_${capacity}_model_input.yaml"
  run_dir="$EXP/raw_outputs/sensitivity/$sensitivity_workload/$capacity"
  mkdir -p "$run_dir"
  test ! -e "$run_dir/completed.marker"
  cp "$ACCELERGY_CONFIG_SOURCE" "$run_dir/accelergy_config.yaml"
  cp "$input" "$run_dir/input.yaml"
  (
    cd "$run_dir"
    set +e
    timeloop-model input.yaml > stdout_stderr.txt 2>&1
    status=$?
    set -e
    printf '\nEXIT_STATUS=%s\n' "$status" >> stdout_stderr.txt
    test "$status" -eq 0
  )
  validate_run "$run_dir" timeloop-model
  printf 'sensitivity\t%s\t%s\t0\t%s\n' "$sensitivity_workload" "$capacity" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$EXP/logs/run_manifest.tsv"
  printf 'PASS\n' > "$run_dir/completed.marker"
done

echo "All mapping, main, and sensitivity runs completed successfully."
