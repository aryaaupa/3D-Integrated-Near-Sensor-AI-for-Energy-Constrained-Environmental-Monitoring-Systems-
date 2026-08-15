# Assumptions and provenance

## Scope

The study isolates the circuit-level consequence of interconnect capacitance
for an otherwise identical CMOS driver/receiver path. It does not transistor-
simulate the 168-PE accelerator, SRAM arrays, LPDDR4 PHY, or sensor interface.

## Parameter table

| Parameter | Value | Classification | Source or rationale |
|---|---:|---|---|
| Simulator | ngspice 42 | Established circuit simulator | Ubuntu 24.04 package `42+ds-3build1`; package SHA-256 `466c4c06418107ceaa9c9457065b3bb71a9d9dc5ec6fef186d7de9d5208ce8db` |
| Device model | 45 nm HP PTM BSIM4 | Public predictive transistor model | University of Minnesota PTM archive, `45nm_HP.pm`; SHA-256 `c9ed2e513523c57a76912a35b2860cb85e4aaa3402b69757d84efa9cc2fb8410` |
| Supply | 1.0 V | Inherited from PTM model | Model header states nominal VDD = 1.0 V |
| Temperature | 27 °C | Inherited from PTM nominal model | Model `tnom=27`; testbench `temp=27` |
| Driver | NMOS 4 µm, PMOS 8 µm, L=45 nm | Deterministic testbench choice | Held identical in every run; 2:1 PMOS/NMOS width ratio |
| Receiver and FO1 load | NMOS 1 µm, PMOS 2 µm, L=45 nm | Deterministic testbench choice | Physical PTM transistors; identical in every run |
| Input | 20 ps rise/fall, 1 ns period | Deterministic testbench choice | Identical in every run; one rising and one falling toggle per measured period |
| Nominal TSV capacitance | 40 fF | Measured peer-reviewed hardware | Batra et al., 2014, 45 nm wafer-stacked SOI-CMOS EDRAM |
| Link resistance | 65 mΩ | Measured peer-reviewed hardware | Same paper reports 65 mΩ/link including TSV and local wire; applied identically to both cases |
| Planar bump capacitance proxy | 160 fF | Deterministic conservative lower bound | Same paper states 40 fF TSV capacitance is less than one quarter of bump-bond capacitance; exactly 4×40 fF avoids overstating the planar load |
| Vertical sensitivity | 5, 20, 40, 80 fF | Deterministic sensitivity values | Brackets the measured nominal value by 8× below and 2× above |
| System bridge activity | 0.25, 0.5, 1.0 | Explicit deterministic sensitivity | Not measured workload data; reported as scenarios and never merged into primary Timeloop energy |

## Literature

P. Batra et al., “Three-Dimensional Wafer Stacking Using Cu TSV Integrated
with 45 nm High Performance SOI-CMOS Embedded DRAM Technology,” *Journal of
Low Power Electronics and Applications*, vol. 4, no. 2, pp. 77–89, 2014,
DOI: [10.3390/jlpea4020077](https://doi.org/10.3390/jlpea4020077).

W. Zhao and Y. Cao, “New Generation of Predictive Technology Model for
Sub-45 nm Early Design Exploration,” *IEEE Transactions on Electron Devices*,
vol. 53, no. 11, pp. 2816–2823, 2006,
DOI: [10.1109/TED.2006.884077](https://doi.org/10.1109/TED.2006.884077).
The model card is distributed by the
[University of Minnesota PTM archive](https://mec.umn.edu/ptm).

## Interpretation boundary

The absolute SPICE numbers are conditional on this predictive model and
testbench. The defensible claim is that, for identical 45 nm CMOS circuitry,
the literature-backed lower vertical capacitance reduces simulated switching
energy and propagation delay. No claim is made about foundry signoff,
post-layout extraction, full LPDDR4 I/O energy, TSV coupling, thermal behavior,
or measured silicon from the proposed architecture.
