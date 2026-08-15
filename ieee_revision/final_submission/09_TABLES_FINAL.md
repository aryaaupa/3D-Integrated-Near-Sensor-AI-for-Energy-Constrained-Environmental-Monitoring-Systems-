# Final Publication Tables

## TABLE I. Five-workload characterization

| Workload | Input | Output | Kernel / stride | MACs | Weights | Input act. | Output act. | Intensity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AlexNet CONV1 | 227 x 227 x 3 | 55 x 55 x 96 | 11 x 11 / 4 | 105,415,200 | 34,848 | 154,587 | 290,400 | 219.69 |
| AlexNet-derived dense CONV2 | 31 x 31 x 96 | 27 x 27 x 256 | 5 x 5 / 1 | 447,897,600 | 614,400 | 92,256 | 186,624 | 501.41 |
| AlexNet CONV3 | 15 x 15 x 256 | 13 x 13 x 384 | 3 x 3 / 1 | 149,520,384 | 884,736 | 57,600 | 64,896 | 148.45 |
| AlexNet-derived dense CONV4 | 15 x 15 x 384 | 13 x 13 x 384 | 3 x 3 / 1 | 224,280,576 | 1,327,104 | 86,400 | 64,896 | 151.70 |
| AlexNet-derived dense CONV5 | 15 x 15 x 384 | 13 x 13 x 256 | 3 x 3 / 1 | 149,520,384 | 884,736 | 86,400 | 43,264 | 147.40 |

Intensity is MACs divided by the combined weight/input/output tensor-element count. It is not a roofline operational intensity.

## TABLE II. Common architecture and controlled variable

| Parameter | Value | Status |
|---|---:|---|
| Compute array | 14 x 12 = 168 PEs | Identical |
| Input / weight precision | 8 bit | Identical |
| Partial-sum / output precision | 16 bit | Identical |
| MAC | 8-bit multiplier, 16-bit adder | Identical |
| Per-PE input RF | 12 entries | Identical |
| Per-PE weight RF | 192 entries | Identical |
| Per-PE partial-sum RF | 16 entries | Identical |
| Shared global SRAM | 128 KiB | Identical |
| Technology / period | 45 nm / 1 ns | Identical |
| Mapping | Planar mapping frozen and replayed | Identical per workload |
| Planar highest level | LPDDR4, 64-bit access width | Controlled variable |
| Localized highest level | 2-MiB SRAM, 64-bit access width | Controlled variable |

## TABLE III. Five-workload Timeloop/Accelergy results

| Workload | Intensity | Planar energy (uJ) | Localized energy (uJ) | Reduction | Cycles planar / localized | Utilization planar / localized |
|---|---:|---:|---:|---:|---:|---:|
| AlexNet CONV1 | 219.69 | 7,343.23 | 2,256.65 | 69.27% | 732,050 / 732,050 | 0.8571 / 0.8571 |
| AlexNet-derived dense CONV2 | 501.41 | 3,103.78 | 2,261.55 | 27.14% | 3,110,400 / 3,110,400 | 0.8571 / 0.8571 |
| AlexNet CONV3 | 148.45 | 732.91 | 671.67 | 8.36% | 958,464 / 958,464 | 0.9286 / 0.9286 |
| AlexNet-derived dense CONV4 | 151.70 | 2,364.95 | 1,528.64 | 35.36% | 1,437,696 / 1,437,696 | 0.9286 / 0.9286 |
| AlexNet-derived dense CONV5 | 147.40 | 1,570.14 | 993.78 | 36.71% | 958,464 / 958,464 | 0.9286 / 0.9286 |

## TABLE IV. Nominal representative-link results

| Case | Capacitance | Resistance | Energy/toggle | Rise delay | Fall delay | Mean delay |
|---|---:|---:|---:|---:|---:|---:|
| Conservative planar-link proxy | 160 fF | 65 mOhm | 95.489 fJ | 29.693 ps | 25.042 ps | 27.367 ps |
| TSV reference | 40 fF | 65 mOhm | 34.598 fJ | 14.946 ps | 14.405 ps | 14.675 ps |
| Relative reduction | 75.00% capacitance | - | 63.77% | - | - | 46.38% |

## TABLE V. Qualitative prior-work positioning

| Work | Hardware status | Evaluation scope | Memory / communication focus | Thermal treatment |
|---|---|---|---|---|
| Eyeriss [3] | Fabricated 2D accelerator | CNN accelerator | Row-stationary local reuse | Not primary focus |
| CamJ [7] | Model validated against reported CIS chips | In-sensor system energy | 2D/3D sensing-compute exploration | Power-density exploration |
| J3DAI [8] | Specialized three-wafer platform | CMOS sensor and DNN accelerator | Near-memory DNN subsystem | Physical tiering acknowledged |
| Shen *et al.* [9] | Simulation study | 3D processor-memory thermal management | Unified core/memory power control | Quantitative thermal study |
| This work | Architecture proxy plus circuit testbench | Five convolution configurations | Controlled LPDDR4-to-SRAM substitution; separate capacitive-link sweep | Design constraints only |

No cross-paper percentage comparison is made because technology, workload, modeling boundary, and reported metric differ.
