# Manuscript tables

## TABLE I. Workload characterization

| Workload | Input feature map | Output feature map | Kernel | Stride | MACs | Weights | Input activations | Output activations | MACs per combined tensor element | Relative characterization |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| AlexNet CONV1 | 227 × 227 × 3 | 55 × 55 × 96 | 11 × 11 | 4 | 105,415,200 | 34,848 | 154,587 | 290,400 | 219.69 | Activation/memory-intensive of the pair |
| AlexNet CONV2 | 31 × 31 × 96 | 27 × 27 × 256 | 5 × 5 | 1 | 447,897,600 | 614,400 | 92,256 | 186,624 | 501.41 | Relatively compute-intensive |

The indicator is `MACs/(weights + input activations + output activations)` and is used only to compare these two layers; it is not a bandwidth-aware roofline operational intensity.

## TABLE II. Common accelerator and simulation parameters

| Parameter | Value | Comparison status |
|---|---:|---|
| Compute array | 14 × 12 = 168 PEs | Identical |
| Input and weight precision | 8 bit | Identical |
| Partial-sum/MAC-output precision | 16 bit | Identical |
| MAC | 8-bit multiplier, 16-bit adder | Identical |
| Per-PE input RF | 12 entries | Identical |
| Per-PE weight RF | 192 entries | Identical |
| Per-PE partial-sum RF | 16 entries | Identical |
| Shared global SRAM | 128 KiB | Identical |
| Architectural technology | 45 nm | Identical |
| Clock period | 1 ns (nominal 1 GHz) | Identical |
| Mapping | Planar mapping frozen and replayed | Identical per workload |
| Planar highest level | External LPDDR4, 64-bit access width | Controlled variable |
| Localized highest level | 2-MiB CACTI-backed SRAM, 64-bit access width | Controlled variable |

## TABLE III. Timeloop/Accelergy results

| Workload | Architecture | Total energy (µJ) | Energy/compute (pJ) | Cycles | Latency at 1 GHz (µs) | Utilization | Highest-level reads | Highest-level writes | External DRAM accesses |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| CONV1 | Planar | 7,343.23 | 69.660 | 732,050 | 732.05 | 0.8571 | 105,569,787 | 290,400 | 105,860,187 |
| CONV1 | Localized | 2,256.65 | 21.407 | 732,050 | 732.05 | 0.8571 | 105,569,787 | 290,400 | 0 |
| CONV2 | Planar | 3,103.78 | 6.930 | 3,110,400 | 3,110.40 | 0.8571 | 17,338,752 | 186,624 | 17,525,376 |
| CONV2 | Localized | 2,261.55 | 5.049 | 3,110,400 | 3,110.40 | 0.8571 | 17,338,752 | 186,624 | 0 |

## TABLE IV. Nominal ngspice link results

| Link case | Capacitance | Resistance | Energy/toggle | Rise delay | Fall delay | Mean delay |
|---|---:|---:|---:|---:|---:|---:|
| Planar bump-load proxy | 160 fF | 65 mΩ | 95.489 fJ | 29.693 ps | 25.042 ps | 27.367 ps |
| Vertical-link proxy | 40 fF | 65 mΩ | 34.598 fJ | 14.946 ps | 14.405 ps | 14.675 ps |
| Reduction | 75.00% capacitance | — | 63.77% | — | — | 46.38% |

## TABLE V. Prior-work positioning

| Work | Fabricated? | 3D integration? | Sensor integrated? | Evaluation type | Workload focus | Memory/interconnect focus | Thermal treatment |
|---|---|---|---|---|---|---|---|
| Eyeriss [3] | Yes | No | No | Fabricated accelerator | CNN layers/networks | Row-stationary on-chip reuse | Not the focus |
| CamJ [7] | Model validated against reported CIS chips | Supports 2D/3D exploration | Yes | System-level CIS energy modeling | In-sensor visual pipelines | Component-level sensing/compute organization | Power-density exploration |
| J3DAI [8] | Yes/specialized hardware platform | Three-wafer | CMOS image sensor | Digital PPA and workload demonstration | Classification and segmentation | Near-memory DNN subsystem | Physical tiering acknowledged |
| Shen *et al.* [9] | No | Processor-memory stack | No | Interval thermal simulation | PARSEC, SPLASH-2, and DNN workloads | Unified core/memory power regulation | Quantitative thermal management |
| This work | No | Architectural proxy plus link testbench | Conceptual sensor tier | Timeloop/Accelergy/CACTI plus ngspice | Two AlexNet convolution layers | Controlled external-to-local memory substitution and link capacitance | Qualitative design constraints only |

Percentages from prior work are not compared because platform, workload, modeling boundary, and reported metric differ.
