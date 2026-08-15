# V. Results and Evaluation

## A. Workload-Level Energy Results

Table III and Fig. 4 report absolute layer energy. For CONV1, the planar configuration consumes 7,343.23 µJ and the localized configuration consumes 2,256.65 µJ. The deterministic reduction is 69.27%. Energy per Timeloop compute falls from 69.660 to 21.407 pJ, also a 69.27% reduction within rounding. For CONV2, total energy changes from 3,103.78 to 2,261.55 µJ, a 27.14% reduction, while energy per compute changes from 6.930 to 5.049 pJ.

[INSERT FIG. 4 HERE]

Caption: Fig. 4. Timeloop/Accelergy total energy for the planar and localized-memory configurations. Values are absolute layer energies; mappings and compute resources are fixed.

[INSERT FIG. 5 HERE]

Caption: Fig. 5. Energy per Timeloop compute. The large difference between CONV1 and CONV2 reflects workload dependence rather than a universal 3D scaling factor.

[INSERT TABLE III HERE]

Caption: TABLE III. Timeloop/Accelergy results.

The total-energy difference is not accompanied by a Timeloop cycle difference. CONV1 takes 732,050 cycles in both configurations, and CONV2 takes 3,110,400 cycles in both. Utilization is 0.8571 in all four runs. At the nominal 1-GHz assumption, those counts correspond to 732.05 and 3,110.40 µs, respectively, but these values contain no external-interface bandwidth penalty. The measured architectural effect is therefore energy reduction at unchanged modeled cycles.

## B. Workload Dependence

The contrast between 69.27% for CONV1 and 27.14% for CONV2 is more informative than a single average. CONV1 performs 105,415,200 MACs but touches large feature maps relative to its weight volume. Its tensor intensity indicator is 219.69 MACs per combined tensor element. CONV2 performs 447,897,600 MACs and has an indicator of 501.41. Thus, the external-memory term occupies a larger share of the planar CONV1 result, and substituting a lower-cost local memory produces a larger relative change.

The component values are consistent with that interpretation. CONV1 highest-level memory energy is 6,775.052 µJ in the planar run and 1,688.475 µJ in the localized run. Its lower SRAM/local-buffer energy (526.162 µJ) and compute energy (42.013 µJ) are identical between architectures. For CONV2, highest-level memory energy changes from 1,121.624 to 279.387 µJ, while lower SRAM/local-buffer energy remains 1,803.648 µJ and compute energy remains 178.510 µJ. The unchanged terms are a direct consequence of the fixed mapping and compute hierarchy.

These results do not establish that every memory-sensitive layer will save 69.27%, or that every compute-intensive layer will save 27.14%. They establish that, for two traceable layers under one controlled architecture, the benefit of highest-level localization depends strongly on workload behavior.

## C. Memory-Localization Analysis

For CONV1, Timeloop reports 105,569,787 highest-level reads and 290,400 highest-level writes in both architectures. For CONV2, it reports 17,338,752 reads and 186,624 writes in both. The fixed mapping therefore yields a 0% reduction in highest-level event count.

The physical destination of those events is different. The planar model contains LPDDR4, so its external-DRAM event totals are 105,860,187 for CONV1 and 17,525,376 for CONV2. The localized model contains no DRAM component, so external-DRAM events are zero and the corresponding activity terminates in stacked SRAM. This is a 100% reduction at the modeled external-DRAM interface, not a 100% reduction in total data movement. The wording “external traffic is eliminated in the localized hierarchy” is valid only with that interface explicitly named.

## D. Localized-Memory Capacity Sensitivity

Fig. 6 shows the CONV1 capacity sweep. Total energy is 2,256.65, 3,066.11, 3,941.87, and 5,217.29 µJ for 2, 4, 8, and 16 MiB, respectively. Relative to the same 7,343.23-µJ planar baseline, the reductions are 69.27%, 58.25%, 46.32%, and 28.95%. Cycles remain 732,050 at every point.

[INSERT FIG. 6 HERE]

Caption: Fig. 6. CONV1 localized-SRAM capacity sensitivity. Every tested capacity fits the layer tensors; increasing capacity raises CACTI-backed access cost and reduces the energy benefit under the fixed access pattern.

The trend demonstrates that “more local SRAM” is not a monotonic energy improvement. Since all capacities exceed the selected working set and the access count is fixed, the sweep exposes the array-cost side of the capacity tradeoff. A system that must retain multiple layers or concurrent streams may still require a larger SRAM, but that system-level capacity requirement is outside this layer experiment.

## E. Transistor-Level Link Energy

Table IV gives the nominal link results. The 160-fF planar bump-load proxy consumes 95.489 fJ/toggle, whereas the literature-backed 40-fF vertical proxy consumes 34.598 fJ/toggle. With identical devices and stimulus, this is a 63.77% switching-energy reduction. The result is conditional on the predictive 45-nm model and lumped testbench; it is not an extracted package or LPDDR4-I/O result.

[INSERT TABLE IV HERE]

Caption: TABLE IV. Nominal ngspice link results.

Across the vertical capacitance sweep, energy/toggle is 17.008, 24.512, 34.598, and 54.912 fJ at 5, 20, 40, and 80 fF, respectively. The monotonic trend in Fig. 7 supports the expected load dependence over the complete evaluated range.

[INSERT FIG. 7 HERE]

Caption: Fig. 7. ngspice supply energy per toggle versus lumped link capacitance. The 40-fF point is the nominal literature-backed vertical proxy; 160 fF is the disclosed conservative planar proxy.

## F. Transistor-Level Link Delay

Mean propagation delay is 27.367 ps for the 160-fF planar proxy and 14.675 ps for the 40-fF vertical proxy, a 46.38% reduction. The 5-, 20-, 40-, and 80-fF vertical sweep produces 9.692, 12.116, 14.675, and 19.139 ps, respectively (Fig. 8). The nominal rise/fall propagation delays are 29.693/25.042 ps for the planar proxy and 14.946/14.405 ps for the vertical proxy.

[INSERT FIG. 8 HERE]

Caption: Fig. 8. ngspice mean input-to-receiver propagation delay versus lumped link capacitance. The result characterizes one representative link, not inference latency.

## G. Cross-Level Interpretation

The architecture and circuit results support one bounded locality argument. At architecture level, replacing high-cost LPDDR4 actions with lower-cost SRAM actions reduces modeled energy, particularly for CONV1. At circuit level, reducing the load on an otherwise identical driver/receiver path reduces simulated switching energy and propagation delay. Neither result requires a claim that MAC throughput changed.

The two percentages must remain separate. Timeloop reports unchanged accelerator cycles because the external bandwidth is not constrained and the mapping is fixed. ngspice reports a 46.38% delay reduction for a single loaded communication path. The latter cannot be substituted for an inference-latency reduction without a bandwidth-aware system timing model. Similarly, link switching energy is not added to the Timeloop total because the energy boundary between the memory component and I/O circuitry is not resolved well enough to rule out double counting.
