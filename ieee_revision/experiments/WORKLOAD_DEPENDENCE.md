# Five-layer workload-dependence extension

The table and figure are generated from the five paired Timeloop/Accelergy runs. No regression or trend line is fitted.

| Layer | MACs/tensor element | Planar-to-localized energy reduction |
|---|---:|---:|
| CONV1 | 219.69 | 69.27% |
| CONV2 | 501.41 | 27.14% |
| CONV3 | 148.45 | 8.36% |
| CONV4 | 151.70 | 35.36% |
| CONV5 | 147.40 | 36.71% |

**Caption:** Workload dependence of the controlled memory-localization experiment. The x-axis is the deterministic architecture-oriented intensity indicator, defined as MAC count divided by the sum of weight, input-activation, and output-activation tensor elements. The y-axis is the planar-to-localized Timeloop/Accelergy total-energy reduction under a separately frozen planar mapping for each layer. Points are shown individually; no statistical relationship is fitted or claimed.

**Insertion:** Place in the Results section immediately after the per-workload energy comparison. It supports only the observation that the benefit varies across the five evaluated layer configurations; it does not establish a universal intensity-energy law.
