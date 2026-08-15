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

**Fig. 5.** Accelergy component-energy breakdown for all five controlled workload pairs. Within each workload, the left bar (P) is the external-LPDDR4 planar proxy and the right bar (L) is the 2-MiB localized-SRAM proxy. Timeloop action counts, lower buffers, compute resources, and mapping are unchanged; only the highest memory component changes. The figure quantifies an LPDDR4-to-SRAM substitution motivated by the proposed 3D organization, not a physical 3D-stack simulation.

Placement: Section V-C. This main-text figure supplies the component-level evidence for the central workload-dependent mechanism.

**Fig. 6.** AlexNet CONV1 localized-SRAM capacity sensitivity under the same fixed mapping, lower hierarchy, and 168-PE compute substrate. The dashed line is the 7,343.23-uJ external-LPDDR4 planar baseline. Every evaluated SRAM capacity fits the selected layer tensors; larger modeled arrays increase access energy under the unchanged action pattern, reducing the localization benefit from 69.27% at 2 MiB to 28.95% at 16 MiB.

Placement: Section V-E.

**Fig. 7.** ngspice supply energy per toggle for the identical 45-nm driver/receiver testbench over a 5-160-fF lumped-capacitance sweep. The 40-fF point is the literature-referenced TSV case; 160 fF is the conservative planar-link proxy derived as 4 x 40 fF, not a measured bump. The reported 63.77% reduction applies only to these two representative testbench loads.

Placement: Section V-F.

**Fig. 8.** ngspice mean propagation delay for the identical 45-nm driver/receiver testbench over a 5-160-fF lumped-capacitance sweep. The reported 46.38% reduction compares only the literature-referenced 40-fF TSV case with the conservative 160-fF planar-link proxy. It is a representative circuit-path quantity, not bandwidth-aware system or inference latency.

Placement: Section V-G.

## Supplementary figures

**Fig. S1.** Descriptive comparison of planar-to-localized total-energy reduction against (a) the planar highest-memory energy fraction and (b) the tensor-intensity indicator for the five evaluated workloads. All points are labeled, and no regression or trend line is fitted. Panel (a) shows that the exposed highest-memory fraction closely tracks the observed benefit within this controlled set; panel (b) shows that similar tensor-intensity values can yield substantially different reductions. No statistical or workload-universal relationship is inferred from five samples.

**Fig. S2.** Energy normalized by Timeloop computes for the five controlled workload pairs.

Component-energy breakdown moved to main-text Fig. 5 because it directly supports the central mechanism.

**Fig. S4.** Planar external-DRAM actions. The localized model records zero external-DRAM actions by construction because its highest-level component is SRAM. Logical highest-level action counts remain unchanged.
