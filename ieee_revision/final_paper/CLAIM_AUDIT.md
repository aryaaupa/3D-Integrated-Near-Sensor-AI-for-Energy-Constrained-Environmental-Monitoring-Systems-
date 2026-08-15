# Quantitative claim audit

Every experimental or configuration number in the manuscript is covered below. Repeated appearances of the same value in the abstract, main text, tables, and conclusion share one audit entry. Citation numbering, bibliographic years/pages, postal codes, section numbers, figure numbers, and Git/checksum identifiers are metadata and are audited separately in `reference_audit.md` or `TRACEABILITY.md`.

Abbreviations: `A-results` = `ieee_revision/experiments/processed/results.csv`; `A-trace` = `ieee_revision/experiments/processed/traceability.csv`; `A-compare` = `ieee_revision/experiments/processed/comparison.csv`; `A-sens` = `ieee_revision/experiments/processed/sensitivity.csv`; `S-results` = `ieee_revision/spice_validation/processed/link_results.csv`; `S-trace` = `ieee_revision/spice_validation/processed/traceability.csv`. Architecture files are at commit `4291da55dc45f433f6836ec0b39e96b04ccc2068`; SPICE files are at commit `9dfd8e40ac959f1a66d024014859a340a15df101`.

## Workload and architecture claims

| Claim | Section(s) | Value | Raw source / line-file-output | Calculation | Verified? |
|---|---|---:|---|---|---|
| CONV1 dimensions | I, IV-B, Table I | input 227×227×3; output 55×55×96; kernel 11×11; stride 4 | `experiments/workloads/alexnet_conv1_activation_intensive.yaml`; paired raw `input.yaml` problem block | Direct fields | Yes |
| CONV2 dimensions | I, IV-B, Table I | input 31×31×96; output 27×27×256; kernel 5×5; stride 1 | `experiments/workloads/alexnet_conv2_compute_intensive.yaml`; paired raw `input.yaml` problem block | Direct fields | Yes |
| CONV1 MACs | IV-B, V-B, Table I | 105,415,200 | A-results `total_MACs`; all CONV1 raw `timeloop-model.stats.txt`, `Computes` | 55×55×96×3×11×11 | Yes |
| CONV2 MACs | IV-B, V-B, Table I | 447,897,600 | A-results `total_MACs`; all CONV2 raw stats, `Computes` | 27×27×256×96×5×5 | Yes |
| CONV1 tensor volumes | IV-B, Table I | weights 34,848; input 154,587; output 290,400 | Workload YAML dimensions | 11×11×3×96; 227×227×3; 55×55×96 | Yes |
| CONV2 tensor volumes | IV-B, Table I | weights 614,400; input 92,256; output 186,624 | Workload YAML dimensions | 5×5×96×256; 31×31×96; 27×27×256 | Yes |
| Tensor-intensity indicators | I, IV-B, V-B, Table I | CONV1 219.69; CONV2 501.41 MAC/combined element | Workload summary CSV and YAML dimensions | MACs/(weights+input+output) | Yes |
| Complete tensor footprints | IV-B | CONV1 770,235 B; CONV2 1,079,904 B | Workload summary fields plus declared precisions | weights+inputs at 1 B; outputs at 2 B | Yes |
| Compute array | Abstract, IV-C, Table II, VIII | 14×12 = 168 PEs | Paired raw `input.yaml`, compute mesh attributes; architecture validator | 14×12 | Yes |
| Precision and MAC | IV-C, Table II | 8-bit inputs/weights; 16-bit psums/output; 8-bit multiplier + 16-bit adder | Paired raw `input.yaml`, component attributes | Direct fields | Yes |
| Per-PE RF capacities | IV-C, Table II | input 12; weight 192; psum 16 entries | Paired raw `input.yaml`, storage attributes | Direct fields | Yes |
| Global SRAM | III-B, IV-C, Table II | 16,384×64 bit = 128 KiB | Paired raw `input.yaml`, shared-glb attributes | 16,384×64/8/1024 | Yes |
| Technology and clock | Abstract, IV-C, Table II | 45 nm; 1 ns; nominal 1 GHz | Paired raw `input.yaml`, technology and `global_cycle_seconds=1e-9` | 1/(1 ns) | Yes |
| Highest-level organizations | III, IV-F, Table II | LPDDR4 64-bit; localized SRAM 2 MiB, 64-bit | Planar/localized architecture YAML and raw `input.yaml` | Direct fields | Yes |
| Planar LPDDR4 action energy | IV-E | 512 pJ per read/write/update vector action | Planar raw ERT YAML, DRAM action entries | Direct generated ERT value | Yes |
| Nominal local-SRAM action energy | IV-E | read 127.645 pJ; write/update 110.308 pJ; leakage 0.0525126 pJ/cycle | Localized raw ERT YAML, stacked-SRAM action entries | Direct generated ERT values | Yes |

## Architecture result claims

| Claim | Section(s) | Value | Raw source / line-file-output | Calculation | Verified? |
|---|---|---:|---|---|---|
| CONV1 total energy | Abstract, I, V-A, Table III, VIII | planar 7,343.23 µJ; local 2,256.65 µJ | A-results `total_energy_pJ`; respective raw stats `Summary Stats/Energy (uJ)` | pJ/10^6 | Yes |
| CONV2 total energy | Abstract, I, V-A, Table III, VIII | planar 3,103.78 µJ; local 2,261.55 µJ | A-results and respective raw stats `Summary Stats/Energy (uJ)` | pJ/10^6 | Yes |
| Total-energy reductions | Abstract, I, V-A, V-B, V-D, VII, VIII | CONV1 69.27%; CONV2 27.14% | A-compare `total_energy_reduction_percent` | 100×(planar−local)/planar | Yes |
| Energy per compute | Abstract, V-A, Table III | CONV1 69.660→21.407 pJ; CONV2 6.930→5.049 pJ | A-results `energy_per_compute_pJ`; raw stats `Total fJ/Compute` | fJ/1000 | Yes |
| Energy/compute reductions | Abstract, V-A | CONV1 69.27%; CONV2 27.14% | A-compare `energy_per_compute_reduction_percent` | 100×(planar−local)/planar | Yes |
| Cycles | Abstract, I, V-A, Table III, VIII | CONV1 732,050; CONV2 3,110,400; identical by pair | A-results `cycles`; raw stats `Summary Stats/Cycles` | Direct parse | Yes |
| Nominal cycle-derived latency | V-A, Table III | CONV1 732.05 µs; CONV2 3,110.40 µs | A-trace `latency_us`; raw stats and `input.yaml` | cycles×1 ns/1000 ns/µs | Yes |
| Utilization | I, V-A, Table III | 0.8571 in all four runs | A-results `utilization`; raw stats utilization percent | percent/100 | Yes |
| CONV1 component energy | V-B | highest 6,775.052→1,688.475 µJ; lower buffers 526.162 µJ; compute 42.013 µJ | A-results corresponding energy columns; A-trace maps to raw stats | pJ/10^6 and round to 0.001 µJ | Yes |
| CONV2 component energy | V-B | highest 1,121.624→279.387 µJ; lower buffers 1,803.648 µJ; compute 178.510 µJ | A-results corresponding energy columns; A-trace maps to raw stats | pJ/10^6 and round to 0.001 µJ | Yes |
| CONV1 highest-level events | V-C, Table III | 105,569,787 reads; 290,400 writes; unchanged by pair | A-results; raw stats scalar reads and fills+updates | Sum across dataspaces | Yes |
| CONV2 highest-level events | V-C, Table III | 17,338,752 reads; 186,624 writes; unchanged by pair | A-results; raw stats scalar reads and fills+updates | Sum across dataspaces | Yes |
| Highest-level event-count reduction | II-B, V-C | 0% | A-compare | 100×(planar events−local events)/planar events | Yes |
| Planar external-DRAM totals | V-C, Table III | CONV1 105,860,187; CONV2 17,525,376 | A-results external read/write columns | reads+writes | Yes |
| Local external-DRAM totals and reduction | V-C, Table III | 0 events; 100% reduction at external interface | Localized `input.yaml` contains no DRAM; A-results zeros; A-compare | 100×(planar−0)/planar | Yes |
| CONV1 capacity sweep | Abstract, IV-I, V-D, VIII | 2/4/8/16 MiB | Sensitivity input YAMLs and A-sens `localized_memory_capacity_MiB` | Direct fields | Yes |
| CONV1 sweep energies | V-D | 2,256.65/3,066.11/3,941.87/5,217.29 µJ | A-sens and sensitivity raw stats `Energy (uJ)` | Direct parse | Yes |
| CONV1 sweep reductions | Abstract, V-D, VII, VIII | 69.27/58.25/46.32/28.95% | A-sens | 100×(7,343.23−sweep)/7,343.23 | Yes |
| CONV1 sweep cycles | V-D | 732,050 at every point | A-sens and sensitivity raw stats | Direct parse | Yes |

## Circuit configuration and result claims

| Claim | Section(s) | Value | Raw source / line-file-output | Calculation | Verified? |
|---|---|---:|---|---|---|
| Simulator version | Abstract, I, IV-J, VIII | ngspice 42; package 42+ds-3build1 | SPICE `logs/tool_versions.txt`; raw simulator banner | Direct output | Yes |
| Device model identity | I, IV-J | `45nm_HP.pm`; HP 45-nm metal-gate/high-k/strained-Si; SHA-256 `c9ed…8410`; blob `160d7da…` | Committed model header, `sha256sum`, Git blob; provenance audit | Direct header/checksum | Yes |
| Device model electrical metadata | IV-J | VDD 1.0 V; BSIM4 level 54/version 4.0; tnom 27 °C | `45nm_HP.pm` header and model declarations; instantiated netlists | Direct fields | Yes |
| Driver/receiver dimensions | IV-J | driver NMOS/PMOS 4/8 µm; receiver 1/2 µm; all L=45 nm | Nominal netlists | Direct instance parameters | Yes |
| Input stimulus | IV-J | 1 V; 20-ps rise/fall; 1-ns period | Nominal netlists, pulse source | Direct parameters | Yes |
| Nominal link proxies | Abstract, I, IV-J, Table IV, VIII | vertical 40 fF; planar 160 fF; both 65 mΩ | Run manifest and nominal netlists | Direct parameter; 160 fF = 4×40 fF | Yes |
| Integration window and toggle normalization | IV-J | 1.05–2.05 ns; two transitions/cycle; divide by 2 | Nominal and sensitivity netlists, `.measure` expressions | Direct expressions | Yes |
| Nominal switching energy | Abstract, V-E, Table IV, VIII | planar 95.489; vertical 34.598 fJ/toggle | S-results and S-trace; nominal `ngspice_stdout_stderr.txt` `.measure` output | |integral| and unit conversion, then /2 | Yes |
| Switching-energy reduction | Abstract, I, V-E, Table IV, VIII | 63.77% | SPICE processed comparison | 100×(95.489−34.59825)/95.489 | Yes |
| Nominal rise/fall delays | V-F, Table IV | planar 29.693/25.042 ps; vertical 14.946/14.405 ps | S-results and nominal raw `.measure` output | Unit conversion and rounding | Yes |
| Nominal mean delays | Abstract, V-F, Table IV, VIII | planar 27.367; vertical 14.675 ps | S-results `mean_propagation_delay_ps` | (rise+fall)/2 | Yes |
| Mean-delay reduction | Abstract, I, V-F, Table IV, VIII | 46.38% | SPICE processed comparison | 100×(27.36712−14.675375)/27.36712 | Yes |
| Nominal capacitance reduction | Table IV | 75.00% | Run manifest | 100×(160−40)/160 | Yes |
| Capacitance sweep | Abstract, IV-K, V-E–V-F, VII | 5/20/40/80 fF; planar context 160 fF | Run manifest and sensitivity netlists | Direct parameters | Yes |
| Sweep switching energies | V-E | 17.008/24.512/34.598/54.912 fJ/toggle | S-results and per-case raw `.measure` output | Per-cycle energy/2, rounded | Yes |
| Sweep mean delays | V-F | 9.692/12.116/14.675/19.139 ps | S-results and per-case raw `.measure` output | (rise+fall)/2, rounded | Yes |

## Negative assertions checked

| Assertion | Evidence | Verified? |
|---|---|---|
| Architecture cycles and utilization do not improve | Paired values in A-results are identical; validator passes | Yes |
| Highest-level event count is unchanged; only external-DRAM interface events become zero | A-results and raw hierarchy inputs | Yes |
| Network/interconnect architecture energy is unavailable, not zero | A-trace marks metric `NA`; stats have no separate network-energy value | Yes |
| Link percentages are not inference-level percentages | Circuit testbench contains only driver/link/receiver; architecture cycles are unchanged | Yes |
| No quantitative thermal result exists | No thermal solver output is present in evidence branches | Yes |
| No sensing-accuracy-versus-temperature curve is supportable | Provenance audit finds no temperature-labeled dataset, sensor transfer model, predictions, ground truth, or accuracy metric | Yes |
