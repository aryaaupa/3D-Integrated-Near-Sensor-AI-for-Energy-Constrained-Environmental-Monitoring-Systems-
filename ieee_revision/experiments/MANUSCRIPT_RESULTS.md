# Manuscript-ready Timeloop/Accelergy results

## Workloads

Exactly two repository-native AlexNet convolution layers were evaluated:

- **AlexNet CONV1 (activation/memory-intensive):** input 227×227×3, output 55×55×96, kernel 11×11, stride 4×4, and 105,415,200 MACs. Tensor volumes are 34,848 weights, 154,587 input activations, and 290,400 output activations.
- **AlexNet CONV2 (relatively compute-intensive):** input 31×31×96, output 27×27×256, kernel 5×5, stride 1×1, and 447,897,600 MACs. Tensor volumes are 614,400 weights, 92,256 input activations, and 186,624 output activations.

## Absolute results

For **AlexNet CONV1**, Timeloop/Accelergy evaluation shows 7,343.23 µJ for the planar case and 2,256.65 µJ for the 3D proxy, a 69.27% reduction. Energy per compute changes from 69.660 to 21.407 pJ/compute. Both cases require 732,050 cycles (732.05 µs at 1 GHz) with utilization 0.8571. The fixed mapping produces 105,860,187 highest-level events in the planar case and 105,860,187 in the 3D proxy (0.00% event-count reduction); the proxy redirects these events to stacked SRAM, so modeled external-DRAM accesses fall by 100.00%.

For **AlexNet CONV2**, Timeloop/Accelergy evaluation shows 3,103.78 µJ for the planar case and 2,261.55 µJ for the 3D proxy, a 27.14% reduction. Energy per compute changes from 6.930 to 5.049 pJ/compute. Both cases require 3,110,400 cycles (3,110.40 µs at 1 GHz) with utilization 0.8571. The fixed mapping produces 17,525,376 highest-level events in the planar case and 17,525,376 in the 3D proxy (0.00% event-count reduction); the proxy redirects these events to stacked SRAM, so modeled external-DRAM accesses fall by 100.00%.

## Sensitivity

For AlexNet CONV1, varying localized SRAM capacity from 2 to 16 MiB while holding mapping and cycles fixed yields total-energy reductions of 28.95% to 69.27% relative to the planar baseline. The benefit therefore remains positive throughout the tested CACTI-backed range, although it decreases as modeled SRAM capacity and access energy increase.

## Major limitation

The integrated configuration is an architectural proxy, not a physical 3D implementation. Timeloop does not model TSV geometry, bonding, thermals, stress, or transistor-level behavior in this study. No separately reported interconnect/network energy is available, so that metric is `NA`. The 3D result isolates the modeled energy effect of replacing external LPDDR4 with localized CACTI-backed SRAM under an otherwise identical fixed mapping; it must not be described as measured silicon performance.

## IEEE methodology paragraph

Timeloop was used for mapping and for cycle, utilization, and memory-access characterization, while Accelergy with CACTI-backed component models was used for component-level energy estimation. The planar and 3D-proxy cases used identical convolution dimensions, MAC counts, 168-PE compute array, arithmetic precision, fixed loop mapping, 1-GHz clock assumption, and lower memory hierarchy. The 3D configuration was represented architecturally by redirecting high-cost external-memory traffic to localized on-stack SRAM, thereby modeling increased data locality and lower-cost local communication. This study does not claim transistor-level, physical-TSV, or thermal simulation.
