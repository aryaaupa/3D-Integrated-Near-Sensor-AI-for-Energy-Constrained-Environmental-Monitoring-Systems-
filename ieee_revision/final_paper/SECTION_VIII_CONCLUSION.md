# VIII. Conclusion

This paper evaluated a three-tier near-sensor sensor–memory–compute organization with an established, reproducible tool chain. Two AlexNet convolution layers were mapped to the same 168-PE, 45-nm accelerator. Timeloop characterized mapping, activity, cycles, and utilization; Accelergy and CACTI-backed models estimated component energy. Replacing external LPDDR4 with nominal 2-MiB localized SRAM reduced modeled total energy from 7,343.23 to 2,256.65 µJ (69.27%) for CONV1 and from 3,103.78 to 2,261.55 µJ (27.14%) for CONV2. Cycles were unchanged within each workload pair, making workload-dependent energy reduction—not inference speedup—the architecture-level result. A 2–16-MiB sensitivity study showed that the CONV1 reduction decreased from 69.27% to 28.95% as CACTI-characterized SRAM capacity increased.

Complementary ngspice 42 simulation with the exact public 45-nm HP PTM card showed that reducing a representative link load from a 160-fF planar proxy to a literature-backed 40-fF vertical proxy reduced switching energy by 63.77% and mean propagation delay by 46.38%. These are link-level values and are not combined with the Timeloop/Accelergy totals.

Future work should extend the evaluation to full networks and bandwidth-aware timing, use post-layout parasitic extraction and a physical 3D interconnect implementation, perform package-level thermal simulation, characterize a selected sensor across temperature with labeled data, and ultimately compare against fabricated silicon.

# Acknowledgment

The author thanks the anonymous reviewers for comments that motivated the tool-based evaluation, workload-level reporting, and clearer scope boundaries in this revision.
