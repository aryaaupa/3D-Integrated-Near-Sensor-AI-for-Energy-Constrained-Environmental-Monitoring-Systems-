# Transistor-level communication-path validation

## Nominal result

ngspice transient simulation with the public 45 nm PTM BSIM4 model gives
**95.489 fJ/toggle** for the conservative
160 fF planar bump-load proxy and **34.598
fJ/toggle** for the measured 40 fF TSV load. The reduction is
**63.77%**. Mean
input-to-receiver propagation delay is **27.367
ps** and **14.675 ps**, respectively, a
**46.38%** reduction.

Both cases use the same 1 V, 45 nm transistor model, driver, receiver,
fanout-of-one load, 20 ps input slew, 1 ns test period, and 65 mΩ series
resistance. Only interconnect capacitance changes. The 40 fF and 65 mΩ nominal
vertical values come from measured 45 nm stacked hardware; 160 fF is a
conservative deterministic lower bound because the same paper reports the
40 fF TSV as less than one quarter of bump-bond capacitance.

## Capacitance sensitivity

Across the vertical-link sweep, the simulated values are:

| Capacitance | Energy/toggle | Mean delay |
|---:|---:|---:|
| 5 fF | 17.008 fJ | 9.692 ps |
| 20 fF | 24.512 fJ | 12.116 ps |
| 40 fF | 34.598 fJ | 14.675 ps |
| 80 fF | 54.912 fJ | 19.139 ps |


Energy increases monotonically across the complete 5–80 fF vertical-link
sensitivity range.

## Diagnostic bridge to Timeloop

The following values multiply raw Timeloop highest-level scalar events by the
reported 8-bit top-memory word width, a disclosed 0.5 bit-toggle probability,
and the SPICE energy per toggle:

- CONV1, planar: 40.434 µJ (0.551% of the corresponding Timeloop/Accelergy total).
- CONV1, 3D proxy: 14.650 µJ (0.649% of the corresponding Timeloop/Accelergy total).
- CONV2, planar: 6.694 µJ (0.216% of the corresponding Timeloop/Accelergy total).
- CONV2, 3D proxy: 2.425 µJ (0.107% of the corresponding Timeloop/Accelergy total).

These diagnostic link energies are **not added to or subtracted from** the
previous Timeloop/Accelergy totals because the boundary between memory-model
energy and I/O energy is not sufficiently resolved to rule out double
counting. Activity factors of 0.25, 0.5, and 1.0 are preserved in
`processed/system_bridge.csv`.

## Manuscript-ready paragraph

To corroborate the communication assumption at circuit level, we performed
ngspice transient simulations using the public 45 nm high-performance PTM
BSIM4 model. Identical CMOS driver, receiver, fanout, supply, input slew, and
series-resistance assumptions were used for both link cases; only the
interconnect capacitance was changed. A measured 40 fF TSV load from a 45 nm
wafer-stacked SOI-CMOS implementation was compared with a conservative 160 fF
bump-load proxy derived from the same publication. The simulated supply energy
decreased from 95.489 to
34.598 fJ per toggle, while mean
propagation delay decreased from 27.367 to
14.675 ps. These results validate the
direction and circuit-level plausibility of lower-capacitance vertical
communication; they do not constitute full-chip transistor simulation,
foundry signoff, extracted-layout analysis, or thermal validation.

## Limitation

This is a transistor-level link testbench using a predictive model, not a
foundry PDK or post-layout extraction. The planar case is a conservative bump
capacitance proxy, not a transistor-accurate LPDDR4 PHY. The simulation does
not model TSV coupling, inductance, ESD structures, package transmission lines,
process corners, temperature gradients, or the full accelerator.
