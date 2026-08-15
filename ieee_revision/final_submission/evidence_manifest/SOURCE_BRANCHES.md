# Authoritative Evidence Branches

| Evidence class | Branch / commit | Authoritative paths |
|---|---|---|
| Verified Timeloop/Accelergy setup | base `56de0a106d1448b738e697dcd47bd300b6f9eaf8` | `ieee_revision/setup_evidence/` |
| Original controlled architecture experiment | `agent/ieee-planar-vs-3d` / `4291da55dc45f433f6836ec0b39e96b04ccc2068` | `ieee_revision/experiments/` |
| Five-workload extension | `agent/full-ieee-r1-manuscript` / `19147f97226d38c2e7011f0ed085928d674658fb` | extended workloads, raw outputs, processed CSVs, validation |
| Scientific figure update | `agent/full-ieee-r1-manuscript` / `118301c73a8764d38371e4b817fca80a8a3a07e9` | final-paper figures and five-workload CSV |
| ngspice link validation | `agent/spice-link-validation` / `9dfd8e40ac959f1a66d024014859a340a15df101` | `ieee_revision/spice_validation/` |
| Model/tool/Reviewer-2 audit | `agent/provenance-reviewer2-corrections` / `f0f9cf9c3c1a2b9af2a1051e783d191d4f1614cc` | `ieee_revision/reviewer_corrections/` |

Evidence conflicts are resolved as raw output > deterministic processed output > manuscript/table > prose summary.
