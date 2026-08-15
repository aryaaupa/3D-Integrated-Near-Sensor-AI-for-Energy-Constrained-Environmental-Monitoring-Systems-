# Response to Reviewers

**Manuscript:** “3D-Integrated Near-Sensor AI for Energy-Constrained Environmental Monitoring Systems”

We thank the Associate Editor and reviewers for the detailed technical guidance. The revised manuscript has been reconstructed around new, reproducible evidence rather than the previous analytical-only narrative. The architecture study now contains ten successful Timeloop/Accelergy model runs: planar and localized configurations for five convolution workloads. The study preserves the same compute array, precision, lower memory hierarchy, clock assumption, and per-workload mapping within each pair. A separate ngspice 42 experiment evaluates a representative CMOS communication path using the exact committed 45-nm PTM card. Raw inputs, outputs, scripts, processed CSVs, checksums, and validators are retained in the repository.

The principal architecture result is now an 8.36%-69.27% modeled energy-reduction range across five workloads. Timeloop cycles and utilization are unchanged within every pair. The expanded data also correct an earlier oversimplification: the scalar tensor-intensity indicator does not predict localization benefit. The revised discussion instead traces the variation to the fraction of planar energy associated with the substituted highest memory level.

## Reviewer 1

### Comment 1

**Reviewer comment:** The evaluation relies on an author-constructed analytical model and does not use established architecture, circuit, RTL, or silicon-evaluation tools.

**Response:** We replaced the analytical-only evaluation with two established simulation paths. Timeloop supplies mappings, cycles, utilization, computes, and memory actions. Accelergy combines those actions with component energy-reference tables, and the SRAM entries are generated through the Accelergy CACTI plug-in. The architecture study contains five planar/localized workload pairs. A separate ngspice 42 transient study evaluates an identical transistor-level driver/link/receiver path as capacitance changes. The paths are not co-simulated or numerically combined. The manuscript identifies these results as modeled/simulated quantities and does not claim RTL, post-layout, or fabricated-silicon validation.

**Location in revised manuscript:** Sections IV-A-IV-L; Figs. 2-7; Tables II-IV; Supplement S1-S13.

### Comment 2

**Reviewer comment:** The paper lacks explicit workloads, absolute values, and per-workload results.

**Response:** The revised study evaluates five configurations: AlexNet CONV1, AlexNet-derived dense CONV2, AlexNet CONV3, AlexNet-derived dense CONV4, and AlexNet-derived dense CONV5. Table I reports input/output dimensions, kernels, strides, MAC counts, tensor volumes, intensity indicators, and source YAML provenance. Table III reports absolute planar/localized energy, reduction, cycles, and utilization for every workload. Total-energy reductions are 69.27%, 27.14%, 8.36%, 35.36%, and 36.71%, respectively.

We use “AlexNet-derived dense” for CONV2, CONV4, and CONV5 because the evaluated YAML files connect every output channel to all listed input channels, whereas canonical AlexNet uses grouped connectivity for those layers.

**Location:** Sections IV-B and V-A-V-D; Figs. 4 and S1-S4; Tables I and III.

### Comment 3

**Reviewer comment:** The manuscript lacks comparison with published 3D and near-sensor systems.

**Response:** Related work now includes foundational 3D-integration studies, CamJ, and J3DAI. Table V positions their scope qualitatively. We do not compare percentage improvements across incompatible technologies, workloads, and evaluation boundaries. J3DAI is described as a specialized three-wafer sensor/accelerator platform; the present contribution is a controlled memory-substitution study plus a separate representative-link experiment.

**Location:** Sections II-B, II-C, VII-B; Table V.

### Comment 4

**Reviewer comment:** The figures are schematic and do not provide quantitative evidence.

**Response:** The main paper now contains four quantitative figures in addition to three compact technical schematics: five-workload total energy, localized-SRAM capacity sensitivity, link switching energy versus capacitance, and link delay versus capacitance. The supplement adds intensity-versus-reduction, energy per compute, component-energy breakdown, and external-DRAM-action figures. Every plot is generated from committed CSV data and is available as PDF, SVG, and high-resolution PNG.

**Location:** Figs. 4-7; Supplementary Figs. S1-S4; `figure_data/`; `scripts/generate_submission_figures.py`.

### Comment 5

**Reviewer comment:** The state-of-the-art discussion and reference list are insufficient and contain duplication.

**Response:** The related-work section and bibliography were rebuilt around 18 primary or official sources. Each citation has one defined claim and a publisher/official URL in the reference audit. The audit distinguishes the CACTI 6.0 methodology paper from the executed CACTI 7.0 code line, Zhao and Cao's PTM methodology from the exact public model-card source, and the ngspice 42 manual from newer documentation.

**Location:** Section II; References [1]-[18]; `07_REFERENCE_AUDIT_FINAL.md`.

### Comment 6

**Reviewer comment:** The proposed memory technology is unspecified.

**Response:** The evaluated localized memory is identified consistently as SRAM. The nominal component is a 2-MiB, 64-bit-wide CACTI-backed SRAM above the unchanged 128-KiB shared SRAM. The planar highest level is external LPDDR4. No NVM result is claimed.

**Location:** Sections III-B, IV-C, IV-D, IV-H; Fig. 2; Table II.

## Reviewer 2

### Comment 1

**Reviewer comment:** Please add and discuss Shen *et al.* on unified core-memory thermal management in 3D-stacked systems.

**Response:** We added the requested ACM TECS study and discuss coordinated core DVFS and memory low-power control as a requirement for thermally coupled stacks. The cited work constrains future physical design; it is not presented as thermal output from our experiment.

**Location:** Sections II-D and VI; Reference [9].

### Comment 2

**Reviewer comment:** Concrete evaluated workloads and model details are needed.

**Response:** The manuscript now provides five workload definitions, exact connectivity terminology, MACs, tensor volumes, 14 x 12 array organization, 168 PEs, RF capacities, 128-KiB global SRAM, 2-MiB localized SRAM, bit widths, 45-nm architecture assumption, nominal 1-GHz clock, mapping-control procedure, tool commits, CACTI implementation commit, ngspice version/package, PTM header, model hash, supply, model version, and nominal temperature.

**Location:** Sections IV-B-IV-L; Tables I, II, IV; Supplement S1-S3 and S9-S12.

### Comment 3

**Reviewer comment:** Please characterize workload arithmetic intensity or memory sensitivity.

**Response:** We report a deterministic tensor-intensity indicator, MACs divided by the combined weight/input/output tensor-element count. The five-workload results show that this scalar is insufficient: CONV3, dense CONV4, and dense CONV5 have similar indicator values (147.40-151.70) but reductions of 8.36%-36.71%. We therefore avoid a trend fit or causal intensity claim. Component accounting provides the stronger explanation: planar highest-level memory contributes 11.06%, 47.10%, and 48.89% of total energy in these three cases, respectively. Across all five workloads, the replaceable planar-memory share ranges from 11.06% to 92.26% and directly accounts for the observed benefit under the controlled substitution.

**Location:** Sections IV-B, V-B, V-C; Table I; Figs. S1 and S3.

### Comment 4

**Reviewer comment:** Please provide sensing accuracy as a function of thermal behavior.

**Response:** We agree that temperature-dependent sensing accuracy is important for a deployable near-sensor system. It cannot be generated scientifically from the present framework. The repository contains no selected transducer, temperature-labeled sensor observations, calibrated temperature-dependent transfer function, fixed inference model, predictions, ground truth, or defined accuracy metric. Timeloop and Accelergy do not generate sensing predictions, and the PTM card's nominal 27 degrees C setting is not a sensor-accuracy experiment. We therefore did not fabricate or import a curve. Instead, the revised paper removes statements implying demonstrated thermal isolation or temperature-robust accuracy and specifies the experiment needed for future validation.

**Location:** Section VI; Section VII-D; Supplement S13.

### Comment 5

**Reviewer comment:** Please discuss J3DAI and clarify how the proposed work differs.

**Response:** J3DAI is now positioned as a specialized three-wafer CMOS-image-sensor/DNN-accelerator platform. This paper instead isolates external-to-local memory substitution on an unchanged accelerator and independently evaluates one capacitive link. We make no superiority claim or cross-platform percentage comparison.

**Location:** Sections II-C, VII-B; Table V; Reference [8].

## Reviewer 3

### Comment 1

**Reviewer comment:** The modeling framework and reproducibility details are unclear.

**Response:** The methodology now identifies each tool's role, source commits, workload provenance, frozen-mapping protocol, common architecture, controlled variable, energy equation, CACTI line, capacity sweep, netlist, PTM card/hash, ngspice package, measurement windows, delay thresholds, raw artifact classes, and validation procedure. A separate evidence manifest maps every deliverable to the authoritative branch and path.

**Location:** Section IV; Fig. 3; Supplement S1-S13; `evidence_manifest/`.

### Comment 2

**Reviewer comment:** Absolute values and a per-workload quantitative breakdown are missing.

**Response:** Table III and Fig. 4 now report absolute planar/localized energy for all five workloads. The supplement reports energy per compute, component energy, and external-DRAM actions. The lowest benefit, CONV3 at 8.36%, is retained and discussed because it demonstrates the boundary of the localization mechanism.

**Location:** Sections V-A-V-D; Table III; Figs. 4 and S2-S4.

### Comment 3

**Reviewer comment:** Quantitative comparisons and sensitivity evidence are insufficient.

**Response:** The main paper includes a four-point 2-16-MiB localized-SRAM capacity sweep and five-point link-capacitance sweeps for switching energy and delay. For CONV1, localized total energy increases from 2,256.65 uJ at 2 MiB to 5,217.29 uJ at 16 MiB, reducing the benefit from 69.27% to 28.95%. Link energy and mean delay are monotonic over 5-160 fF. All plotted points are parsed or deterministically copied from validated simulator outputs.

**Location:** Sections V-E-V-G; Figs. 5-7; Table IV.

### Comment 4

**Reviewer comment:** The manuscript is repetitive and mixes architecture, circuit, and thermal conclusions.

**Response:** The paper has been reconstructed into separate architecture, methodology, results, physical/thermal considerations, and cross-level discussion sections. Architecture energy/cycles, representative-link energy/delay, and future thermal/sensor validation are assigned distinct evidence boundaries. The architecture and circuit percentages are never multiplied or added.

**Location:** Sections III-VII; Fig. 3.

### Comment 5

**Reviewer comment:** Thermal claims require correction or quantitative support.

**Response:** Unsupported thermal-result language has been removed. Section VI treats tier ordering, heat removal, hotspot control, and coordinated power management as physical-design requirements. It states the additional package, power-map, boundary-condition, transducer, and labeled-data inputs required for future thermal and sensing validation.

**Location:** Sections VI, VII-D, and VIII.
