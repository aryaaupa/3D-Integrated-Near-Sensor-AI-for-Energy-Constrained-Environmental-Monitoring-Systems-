# Final Claim Audit

Evidence priority used throughout: committed raw simulator output > deterministic processed output > manuscript table/figure > prose summary. Every claim below passes that hierarchy.

| Claim | Manuscript location | Value | Evidence file | Raw source | Calculation | Status |
|---|---|---|---|---|---|---|
| Evaluated PE count | Abstract; III; IV-C | 168 | planar/localized input YAML | flattened architecture | 14 x 12 | PASS |
| Array geometry | IV-C; Table II | 14 x 12 | architecture input YAML | flattened architecture | Direct | PASS |
| Input/weight precision | IV-C; Table II | 8 bit | architecture input YAML | flattened architecture | Direct | PASS |
| Partial-sum/output precision | IV-C; Table II | 16 bit | architecture input YAML | flattened architecture | Direct | PASS |
| Shared global SRAM | III; IV-C | 128 KiB | architecture input YAML | flattened architecture | 16,384 x 64 bit / 8 | PASS |
| Nominal localized SRAM | Abstract; III; IV-D | 2 MiB | localized input YAML | flattened architecture | 262,144 x 64 bit / 8 | PASS |
| Clock assumption | Abstract; IV-C | 1 GHz / 1 ns | architecture input YAML | flattened architecture | Reciprocal | PASS |
| CONV1 dimensions | IV-B; Table I | 227x227x3 to 55x55x96, 11x11, s4 | `workload_summary.csv` | problem YAML | Direct | PASS |
| Dense CONV2 dimensions | IV-B; Table I | 31x31x96 to 27x27x256, 5x5, s1 | `workload_summary.csv` | problem YAML | Direct | PASS |
| CONV3 dimensions | IV-B; Table I | 15x15x256 to 13x13x384, 3x3, s1 | `workload_summary.csv` | problem YAML | Direct | PASS |
| Dense CONV4 dimensions | IV-B; Table I | 15x15x384 to 13x13x384, 3x3, s1 | `workload_summary.csv` | problem YAML | Direct | PASS |
| Dense CONV5 dimensions | IV-B; Table I | 15x15x384 to 13x13x256, 3x3, s1 | `workload_summary.csv` | problem YAML | Direct | PASS |
| Workload MAC counts | IV-B; Table I | 105,415,200; 447,897,600; 149,520,384; 224,280,576; 149,520,384 | `results.csv`; `workload_summary.csv` | raw stats `Computes` | Direct/multiplied dimensions | PASS |
| Tensor-intensity indicators | IV-B; Table I | 219.69; 501.41; 148.45; 151.70; 147.40 | `workload_dependence.csv` | problem YAML | MACs/(W+I+O) | PASS |
| CONV1 energy | V-A; Table III | 7,343.23 -> 2,256.65 uJ | `results.csv` | paired raw stats | pJ / 1e6 | PASS |
| Dense CONV2 energy | V-A; Table III | 3,103.78 -> 2,261.55 uJ | `results.csv` | paired raw stats | pJ / 1e6 | PASS |
| CONV3 energy | V-A; Table III | 732.91 -> 671.67 uJ | `results.csv` | paired raw stats | pJ / 1e6 | PASS |
| Dense CONV4 energy | V-A; Table III | 2,364.95 -> 1,528.64 uJ | `results.csv` | paired raw stats | pJ / 1e6 | PASS |
| Dense CONV5 energy | V-A; Table III | 1,570.14 -> 993.78 uJ | `results.csv` | paired raw stats | pJ / 1e6 | PASS |
| Five energy reductions | Abstract; V-A; Table III | 69.27%; 27.14%; 8.36%; 35.36%; 36.71% | `comparison.csv` | paired raw stats | 100(Ep-El)/Ep | PASS |
| Headline reduction range | Abstract; I; VII; VIII | 8.36%-69.27% | `comparison.csv` | paired raw stats | min/max five reductions | PASS |
| CONV1 cycles/utilization | V-D; Table III | 732,050; 0.8571 both | `results.csv` | paired raw stats | Direct | PASS |
| Dense CONV2 cycles/utilization | V-D; Table III | 3,110,400; 0.8571 both | `results.csv` | paired raw stats | Direct | PASS |
| CONV3 cycles/utilization | V-D; Table III | 958,464; 0.9286 both | `results.csv` | paired raw stats | Direct | PASS |
| Dense CONV4 cycles/utilization | V-D; Table III | 1,437,696; 0.9286 both | `results.csv` | paired raw stats | Direct | PASS |
| Dense CONV5 cycles/utilization | V-D; Table III | 958,464; 0.9286 both | `results.csv` | paired raw stats | Direct | PASS |
| Cycle reduction | V-D | 0% for all five | `comparison.csv` | paired raw stats | 100(Cp-Cl)/Cp | PASS |
| Planar highest-memory shares | I; V-C | 92.26%; 36.14%; 11.06%; 47.10%; 48.89% | final `comparison.csv` | paired raw stats | 100Ehighest/Etotal | PASS |
| Logical highest-level actions unchanged | III-B; V-C | 0% reduction | architecture `comparison.csv` | raw stats/XML | paired equality | PASS |
| Localized external DRAM actions | V-C; S4 | 0 by construction | `results.csv` | localized raw stats | Direct classification | PASS |
| CONV1 capacity sweep energy | V-E | 2,256.65; 3,066.11; 3,941.87; 5,217.29 uJ | `sensitivity.csv` | four raw stats files | pJ / 1e6 | PASS |
| Capacity sweep reductions | V-E | 69.27%; 58.25%; 46.32%; 28.95% | `sensitivity.csv` | four raw stats files | 100(Eplanar-Elocal)/Eplanar | PASS |
| Capacity sweep cycles | V-E | 732,050 all points | `sensitivity.csv` | four raw stats files | Direct | PASS |
| PTM model hash | IV-K | c9ed2e...8410 | circuit checksums | exact model file | SHA-256 | PASS |
| PTM header/supply | IV-K | 45-nm HP; 1.0 V | model card | exact model file | Direct | PASS |
| PTM model version/tnom | IV-K | BSIM4 4.0; 27 C | model card | exact model file | Direct | PASS |
| ngspice version/package | IV-K | 42; 42+ds-3build1 | toolchain provenance | bootstrap log/package record | Direct | PASS |
| Nominal capacitances | IV-J; V-F/G | 40 fF and 160 fF | run manifest; assumptions | nominal input netlists | 160 = 4 x 40 | PASS |
| Nominal link resistance | IV-J; Table IV | 65 mOhm | run manifest | input netlists | Direct | PASS |
| Vertical energy/toggle | Abstract; V-F; Table IV | 34.598 fJ | `link_results.csv` | raw ngspice integral | abs(Q)V/2 | PASS |
| Planar energy/toggle | Abstract; V-F; Table IV | 95.489 fJ | `link_results.csv` | raw ngspice integral | abs(Q)V/2 | PASS |
| Representative 160-fF planar-link proxy versus literature-referenced 40-fF TSV case: energy reduction | Abstract; V-F; Table IV | 63.77% | `link_comparison.csv` | two raw outputs | 100(Ep-Ev)/Ep | PASS |
| Vertical rise/fall/mean delay | V-G; Table IV | 14.946/14.405/14.675 ps | `link_results.csv` | raw `.measure` output | mean=(rise+fall)/2 | PASS |
| Planar rise/fall/mean delay | V-G; Table IV | 29.693/25.042/27.367 ps | `link_results.csv` | raw `.measure` output | mean=(rise+fall)/2 | PASS |
| Representative 160-fF planar-link proxy versus literature-referenced 40-fF TSV case: mean-delay reduction | Abstract; V-G; Table IV | 46.38% | `link_comparison.csv` | two raw outputs | 100(Dp-Dv)/Dp | PASS |
| Link energy sweep | V-F; S11 | 17.008-95.489 fJ | `link_results.csv` | five raw outputs | Parsed | PASS |
| Link delay sweep | V-G; S11 | 9.692-27.367 ps | `link_results.csv` | five raw outputs | Parsed | PASS |
| No separate architecture network energy | IV-G; VII-D | NA, not zero | `results.csv`; traceability | raw stats inspection | Direct absence | PASS |
| No thermal simulation result | VI; VII-D | None reported | temperature evidence audit | repository inventory | Evidence absence audited | PASS |
| No sensing-accuracy-vs-temperature result | VI; VII-D | None generated | temperature evidence audit | repository inventory | Evidence absence audited | PASS |
| Architecture and circuit paths are independent | Abstract; IV-A; VII-A | No co-simulation | scripts/input boundaries | separate raw directories | Workflow inspection | PASS |

## Unsupported-language audit

The manuscript was searched for `speedup`, `higher utilization`, `thermal improvement`, `thermal uniformity`, `accuracy improvement`, `45-70%`, `60-80%`, `full network`, `silicon validation`, `post-layout`, and `reduced cycles`. Any occurrence is either a bounded denial/limitation or absent. No positive unsupported experimental claim remains.
