# Reproducibility and traceability

## Evidence baselines

| Evidence | Git ref | Authoritative path | Validation record |
|---|---|---|---|
| Tool setup | `56de0a106d1448b738e697dcd47bd300b6f9eaf8` | `ieee_revision/setup_evidence/` | `final_verification.txt`, official-example raw output |
| Architecture experiment | `agent/ieee-planar-vs-3d` at `4291da55dc45f433f6836ec0b39e96b04ccc2068` | `ieee_revision/experiments/` | `logs/final_validation.txt` reports `FINAL_VALIDATION=PASS` |
| Circuit experiment | `agent/spice-link-validation` at `9dfd8e40ac959f1a66d024014859a340a15df101` | `ieee_revision/spice_validation/` | `logs/final_validation.txt` reports `FINAL_VALIDATION=PASS` |
| Provenance corrections | `agent/provenance-reviewer2-corrections` at `f0f9cf9c3c1a2b9af2a1051e783d191d4f1614cc` | `ieee_revision/reviewer_corrections/` | model, manual, CACTI, literature, and temperature-evidence audits |

The manuscript files in this directory do not replace raw evidence. They cite and summarize the immutable evidence commits above.

## Architecture evidence path

For each workload/architecture pair, the raw directory is:

`ieee_revision/experiments/raw_outputs/<workload>/<architecture>/`

It preserves the effective input YAML, fixed map, Timeloop statistics, XML, mapper/model standard output and error, ERT, ART, flattened architecture, Accelergy log, and run-completion marker. The parser output is `ieee_revision/experiments/processed/results.csv`; metric-to-source mappings are in `ieee_revision/experiments/processed/traceability.csv`; deterministic percentage calculations are in `ieee_revision/experiments/processed/comparison.csv`; the four-point capacity sweep is in `ieee_revision/experiments/processed/sensitivity.csv`.

Within each workload pair, the validator confirms identical problem dimensions, total computes, fixed mapping, 14 × 12 compute array, 168 PEs, bit widths, PE-local RFs, 128-KiB global SRAM, 45-nm assumption, 1-ns period, cycles, and utilization. The controlled change is the highest memory level: external LPDDR4 versus localized CACTI-backed SRAM.

Source versions preserved by the architecture evidence are Timeloop `32370826b3e280497c89f887acc1ee28e83fd3cf`, Accelergy `6911d156bd18ec45a3b25006f0eae284e9bc80a8`, Accelergy CACTI plug-in `291018b12cc9cd467168973fc47528670e1480ce`, and HewlettPackard CACTI `1ffd8dfb10303d306ecd8d215320aea07651e878`.

## Circuit evidence path

The nominal and sweep cases are stored under:

`ieee_revision/spice_validation/raw_outputs/<case>/`

Each directory preserves the instantiated netlist, `ngspice_stdout_stderr.txt`, waveform output, completion marker, copied model card, and checksums. Run parameters are in `ieee_revision/spice_validation/logs/run_manifest.csv`. Parsed measurements are in `ieee_revision/spice_validation/processed/link_results.csv`; metric-to-output mappings are in `ieee_revision/spice_validation/processed/traceability.csv`; nominal percentage calculations are in the processed comparison file.

The simulator is ngspice 42, Ubuntu package `42+ds-3build1`. The exact card is `45nm_HP.pm`, Git blob `160d7da3c5f3a6c0037332df5535dc07d62720ae`, SHA-256 `c9ed2e513523c57a76912a35b2860cb85e4aaa3402b69757d84efa9cc2fb8410`. Its header identifies “PTM High Performance 45nm Metal Gate / High-K / Strained-Si”; the model declares BSIM4 level 54, version 4.0, `tnom=27`, and nominal 1.0-V supply. The committed model and the copy used by each passing run are byte-identical.

## Manuscript figures

| Figure | Input file | Generation |
|---:|---|---|
| 1 | `figure_data/figure1_architecture_nodes.csv` | `scripts/generate_all_figures.py` |
| 2 | `figure_data/figure2_workflow_nodes.csv` | `scripts/generate_all_figures.py` |
| 3 | `figure_data/figure3_hierarchy.csv` | `scripts/generate_all_figures.py` |
| 4–5 | `figure_data/architecture_results.csv` | Values copied from the verified architecture `results.csv`; plotted by script |
| 6 | `figure_data/capacity_sensitivity.csv` | Values copied from the verified architecture `sensitivity.csv`; plotted by script |
| 7–8 | `figure_data/spice_link_results.csv` | Values copied from the verified circuit `link_results.csv`; plotted by script |

All figure outputs are available as vector PDF and inspection PNG. No result value is hard-coded in the plotting routine; the routine reads the CSV files.

## Evidence boundaries

- Timeloop/Accelergy: architecture-level activity, energy, cycles, and utilization under the specified inputs. It does not physically simulate TSVs, package wiring, or thermal fields.
- ngspice: one transistor-level driver/link/receiver path at the specified PTM-card conditions. It does not predict whole-inference latency or energy.
- CACTI: predictive memory characterization through the pinned CACTI 7.0 code line; it is not silicon measurement.
- Temperature and sensing accuracy: no temperature-labeled sensor data, calibrated transfer model, predictions, ground truth, or accuracy metric is present. No accuracy-versus-temperature curve is supported or generated.
