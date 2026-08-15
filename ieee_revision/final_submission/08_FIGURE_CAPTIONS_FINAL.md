# Final Figure Captions and Placement

## Main figures

**Fig. 1.** Conceptual three-tier near-sensor architecture comprising a sensor/front-end tier, a localized-SRAM tier, and a compute tier. The compute tier contains the evaluated 128-KiB global buffer and 168-PE array. Vertical paths indicate conceptual inter-tier communication; physical geometry is not modeled.

Placement: Section III-A after the three-tier organization paragraph.

**Fig. 2.** Controlled planar and localized memory hierarchies. The lower hierarchy and 168-PE compute substrate are identical; the primary modeled change is the highest-level component, external LPDDR4 versus 2-MiB localized SRAM.

Placement: Section III-B after the fair-comparison description.

**Fig. 3.** Independent architecture- and circuit-level evaluation paths. Timeloop/Accelergy/CACTI generate architecture energy, while the PTM/ngspice testbench generates representative-link switching energy and delay. The paths are interpreted separately.

Placement: Section IV-A after the evaluation-boundary paragraph.

**Fig. 4.** Timeloop/Accelergy total energy across five convolution configurations. Pair annotations show deterministic planar-to-localized reductions. Mapping, precision, lower hierarchy, compute resources, cycles, and utilization are unchanged within each pair.

Placement: Section V-A. This is the principal quantitative architecture figure.

**Fig. 5.** CONV1 localized-SRAM capacity sensitivity. The dashed line is the planar LPDDR4 baseline. Every evaluated SRAM capacity fits the selected layer tensors; larger modeled arrays increase access cost under the fixed action pattern.

Placement: Section V-E.

**Fig. 6.** ngspice supply energy per toggle versus lumped link capacitance. The 40-fF point is the literature-referenced TSV case; 160 fF is the disclosed planar-link proxy derived as 4 x 40 fF.

Placement: Section V-F.

**Fig. 7.** ngspice mean propagation delay versus lumped link capacitance for the identical driver/receiver testbench. Link propagation delay is a circuit-path quantity and is not substituted for inference latency.

Placement: Section V-G.

## Supplementary figures

**Fig. S1.** Tensor-intensity indicator versus planar-to-localized energy reduction. Points are shown individually; no regression or trend line is fitted. Similar indicator values for CONV3, dense CONV4, and dense CONV5 produce reductions from 8.36% to 36.71%, so no universal intensity-energy relationship is inferred.

**Fig. S2.** Energy normalized by Timeloop computes for the five controlled workload pairs.

**Fig. S3.** Component-energy breakdown. Lower-buffer and compute energy are unchanged within each pair; the highest-level component produces the observed total-energy difference.

**Fig. S4.** Planar external-DRAM actions. The localized model records zero external-DRAM actions by construction because its highest-level component is SRAM. Logical highest-level action counts remain unchanged.
