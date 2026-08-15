# 3D-Integrated Near-Sensor AI for Energy-Constrained Environmental Monitoring Systems

ARYA UPADHYAY, Member, IEEE

Department of Electrical and Computer Engineering, The University of Texas at Austin, Austin, TX 78712 USA

Corresponding author: Arya Upadhyay (e-mail: arya.upadhyay@utexas.edu).


# Abstract

Data movement can dominate the energy of edge artificial-intelligence accelerators, especially when sensor-derived activations and model parameters repeatedly traverse an external-memory interface. This paper presents a three-tier near-sensor architecture that vertically organizes sensing, localized memory, and compute. The principal architectural mechanism is evaluated with Timeloop and Accelergy using CACTI-backed memory characterization. Two AlexNet convolution layers are executed on the same 168-processing-element, 45-nm accelerator with identical arithmetic precision, mappings, lower memory hierarchy, and 1-GHz clock assumption. Replacing the modeled external LPDDR4 level with a 2-MiB localized SRAM reduces total energy from 7,343.23 to 2,256.65 µJ (69.27%) for activation/memory-intensive CONV1 and from 3,103.78 to 2,261.55 µJ (27.14%) for relatively compute-intensive CONV2. Timeloop cycles and utilization remain unchanged, so these results establish an energy-locality benefit rather than an inference-latency improvement. A 2–16-MiB CACTI-backed sweep shows that the reduction for CONV1 decreases from 69.27% to 28.95% as SRAM capacity and access cost increase. Complementary ngspice 42 transient simulation with the exact public 45-nm high-performance PTM card evaluates a representative link. Reducing the lumped load from a 160-fF planar proxy to a literature-backed 40-fF vertical proxy lowers switching energy from 95.489 to 34.598 fJ/toggle (63.77%) and mean propagation delay from 27.367 to 14.675 ps (46.38%). The link results are circuit-level quantities and are not combined with the architectural energy totals.

# Index Terms

Three-dimensional integration, edge artificial intelligence, near-sensor computing, memory hierarchy, data movement, Timeloop, Accelergy, CACTI, ngspice, thermal co-design.

# I. Introduction

Edge artificial-intelligence (AI) systems increasingly execute inference close to sensors to reduce dependence on continuous cloud connectivity and to support operation under tight energy budgets. The arithmetic itself is only part of the cost. Weights, input features, intermediate activations, and partial sums must be stored and transferred through a hierarchy whose higher levels can consume far more energy per access than a multiply-accumulate (MAC) operation [1], [2]. Spatial accelerators such as Eyeriss therefore devote substantial hardware and mapping effort to data reuse [3]. This concern is a modern instance of the memory wall: increases in compute throughput alone do not remove the bandwidth, latency, and energy costs imposed by the memory system [4].

Near-sensor workloads sharpen this problem. A sensor can continuously generate data even when inference is intermittent, and a conventional planar organization may place acquisition, external memory, and compute in separate dies or packages. The resulting high-level traffic may dominate system energy despite efficient local register files and on-chip SRAM. Three-dimensional (3D) integration offers a physical mechanism to increase locality: sensing, storage, and compute can occupy distinct tiers connected by dense inter-tier links rather than by a distant external-memory path [5], [6]. However, vertical integration is not an automatic or workload-independent efficiency multiplier. Its value depends on the tensor working set, reuse, mapping, storage capacity, and the fraction of energy associated with the memory level that is localized.

Existing work provides important but distinct reference points. CamJ models system-level energy for computational CMOS image sensors and explores 2D/3D sensing organizations [7]. J3DAI demonstrates a specialized three-wafer CMOS image sensor containing a DNN accelerator [8]. These works establish that in-sensor and vertically integrated AI are credible research directions. The question addressed here is narrower and controlled: **with workload, compute resources, precision, lower memory hierarchy, and mapping held fixed, how much does modeled energy change when the highest memory level is moved from external LPDDR4 to localized on-stack SRAM?** This formulation isolates memory placement instead of comparing unrelated accelerators.

We answer that question using established architecture tools and then test the associated electrical motivation independently. Timeloop characterizes mapping, cycles, utilization, and memory activity, while Accelergy combines those action counts with component energy estimates; SRAM action energies are produced through the Accelergy CACTI workflow [10]–[13]. Two convolution layers from the repository's AlexNet configuration [14] provide contrasting behavior. CONV1 has dimensions 227 × 227 × 3 to 55 × 55 × 96 with an 11 × 11 kernel and stride four; CONV2 has dimensions 31 × 31 × 96 to 27 × 27 × 256 with a 5 × 5 kernel and stride one. Their architecture-oriented intensity indicators are 219.69 and 501.41 MACs per combined weight/input/output tensor element, respectively. The indicator is used to distinguish the two selected layers and is not presented as a roofline operational intensity.

The controlled Timeloop/Accelergy evaluation produces a deliberately nonuniform result. For CONV1, total modeled energy decreases from 7,343.23 to 2,256.65 µJ, a 69.27% reduction. For CONV2, it decreases from 3,103.78 to 2,261.55 µJ, a 27.14% reduction. The split is the primary scientific finding: highest-level localization helps both evaluated layers, but its relative benefit is much larger for the more memory-sensitive case. Timeloop reports 732,050 cycles for CONV1 and 3,110,400 cycles for CONV2 in both organizations, with utilization 0.8571. Because the experiment fixes the mapping and does not impose an external-bandwidth timing constraint, no architectural inference-latency improvement is claimed.

A second experiment addresses a separable circuit question. Short vertical connections can present lower electrical loading than package-level alternatives, but Timeloop does not transistor-simulate those links. We therefore use ngspice 42 with the exact public `45nm_HP.pm` card distributed by the University of Minnesota PTM archive [16]–[18]. An identical CMOS driver, receiver, fanout, supply, input slew, and series resistance is used for both link proxies; only the lumped capacitance changes. The nominal 40-fF vertical value comes from measured 45-nm stacked hardware [15], and 160 fF is a disclosed conservative planar proxy derived from the same source. The simulated link switching energy decreases by 63.77%, and mean link propagation delay decreases by 46.38%. These are link-level quantities, not whole-inference energy or latency improvements, and they are not arithmetically combined with the Timeloop/Accelergy percentages.

The contributions are as follows:

1. A three-tier sensor–localized-memory–compute organization that exposes memory placement and link loading as two separable evaluation questions.
2. A reproducible, controlled Timeloop/Accelergy evaluation with CACTI-backed SRAM characterization, fixed workload mappings, and identical compute assumptions.
3. A workload-dependent result: 69.27% modeled total-energy reduction for AlexNet CONV1 and 27.14% for CONV2, with absolute energy, cycles, utilization, and memory events reported per workload.
4. A 2–16-MiB localized-SRAM sensitivity study showing that larger capacity is not monotonically better in the modeled energy objective.
5. An independent transistor-level ngspice 42 link study using the exact 45-nm HP PTM card and literature-backed interconnect parameters.

The proposed architecture has not been fabricated and is not post-layout. Representative communication links are nevertheless evaluated at transistor level. Thermal behavior, sensor accuracy versus temperature, physical TSV coupling, and package heat removal remain outside the reported simulations and are treated explicitly as physical-design and validation requirements.

# II. Background and Related Work

## A. Data Movement in Edge-AI Accelerators

The cost of DNN inference is determined jointly by arithmetic, storage, and communication. Sze *et al.* survey how tensor dimensions, loop nests, dataflow, and memory hierarchy determine access frequency and energy [1]. Horowitz's energy comparison further motivates minimizing long-distance movement instead of treating MAC count as a complete efficiency proxy [2]. Eyeriss demonstrates the architectural response: a spatial array, local register files, a shared global buffer, and a row-stationary dataflow exploit reuse across weights, activations, and partial sums [3].

The memory wall provides a broader systems interpretation [4]. If compute throughput grows while memory service cost remains high, the system can be limited by data supply rather than arithmetic. In an edge device, this limitation appears not only as performance pressure but also as energy consumed at off-chip interfaces. The relevant design objective is therefore not simply to minimize the number of operations. It is to map a fixed workload so that expensive high-level accesses are avoided or replaced by lower-cost storage without inadvertently increasing other activity.

Timeloop and Accelergy make that reasoning explicit. Timeloop represents loop mappings across a spatial accelerator and reports performance and activity statistics [10]. Accelergy estimates energy from component actions and energy-reference-table entries [11]. These tools do not replace a physical implementation, but they allow an architecture comparison to be stated in reproducible configuration files rather than in an author-constructed spreadsheet. The present study adopts that role and preserves all raw maps, statistics, ERTs, ARTs, logs, and input YAML files.

## B. Three-Dimensional Integration and Near-Sensor Computing

Three-dimensional integration places active or passive functions on vertically connected tiers. Early analyses described the potential for reducing global interconnect length and combining system functions within a compact footprint [5]. Manufacturing studies later developed processes, design structures, and integration flows for stacked silicon [6]. For near-sensor computing, the important opportunity is heterogeneous locality: a sensor-compatible tier, a dense memory tier, and a digital compute tier need not use the same process, yet can communicate within one stack.

The architectural benefit is conditional. Vertical placement can lower the cost of reaching storage, but it does not itself change the convolution's MAC count. Nor does it guarantee fewer memory events when a fixed mapping is retained. In the present experiment, the same highest-level events occur in both organizations; their destination changes from external LPDDR4 to localized SRAM. This distinction separates **traffic elimination at a named external interface** from **elimination of total data movement**, the latter of which is not claimed.

## C. Existing 3D-Integrated AI Hardware

CamJ provides component-level modeling for computational CMOS image sensors and includes 2D-versus-3D architectural exploration [7]. Its sensor-aware scope complements the accelerator-centered analysis here. J3DAI is an especially relevant hardware reference because it implements a DNN accelerator in a three-wafer stacked CMOS-image-sensor platform [8]. Its top, middle, and bottom dies specialize the pixel, readout/system, and AI functions, respectively, and its evaluation focuses on the digital system and performance–power–area behavior.

J3DAI and this work should not be placed in an artificial head-to-head percentage comparison. J3DAI is a specialized fabricated image-sensor system with its own accelerator, memories, software, and workloads. This study is a generalized controlled memory-localization experiment plus an independent representative-link simulation. It does not claim superiority to J3DAI. Instead, J3DAI demonstrates physical feasibility of the broader integration direction, while the present results isolate how one memory-hierarchy mechanism depends on workload and SRAM capacity.

## D. Thermal Management in 3D-Stacked Systems

Vertical integration also couples heat sources and raises power density. Shorter communication may reduce one energy term, yet interior tiers can have a poor path to a heat spreader, and local temperature depends on the spatial distribution and timing of activity. Shen *et al.* show why core and memory decisions must be coordinated in a 3D processor-memory stack [9]. Their extended thermal-simulation workflow jointly manages core dynamic voltage and frequency scaling (DVFS) and memory low-power modes, reflecting the fact that compute and memory are both performance- and thermally coupled.

That result constrains the interpretation of our energy study. A reduction in modeled memory energy cannot be translated directly into a peak-temperature or sensor-accuracy result. Tier placement, package thermal resistance, heat spreading, runtime regulation, and temperature-dependent sensor behavior require models and measurements not produced by Timeloop, Accelergy, CACTI, or the nominal-temperature link testbench. Section VI therefore treats thermal management as a necessary co-design activity rather than as a demonstrated benefit.

## E. Positioning of This Work

The present work sits between general architecture modeling and fabricated system demonstrations. Relative to a conceptual analytical model, it adds established tools, complete configuration and raw-output evidence, absolute per-workload values, a capacity sweep, and transistor-level link simulation. Relative to J3DAI or a post-layout design, it remains deliberately earlier stage: the stack is an architectural proxy, the link is a representative lumped testbench, and the sensor tier is not a selected transducer.

The study's two-level structure is therefore important. At architecture level, it asks how replacing a high-cost external memory with localized SRAM changes energy under a fixed mapping. At circuit level, it asks how a lower lumped link capacitance changes energy and delay for otherwise identical transistors. The evidence paths support a consistent locality argument, but their results retain separate denominators and modeling boundaries. Table V summarizes this positioning without forcing incompatible metrics into a single ranking.

[INSERT TABLE V HERE]

Caption: TABLE V. Qualitative positioning relative to representative accelerator, near-sensor, 3D-integration, and thermal-management work.

# III. System Architecture

## A. Overall 3D Stack Design

Fig. 1 shows the proposed organization. The sensor tier acquires and digitizes observations. A localized-memory tier retains the layer working set close to the accelerator. The compute tier contains the spatial PE array and its lower memory hierarchy. The logical direction of dataflow is sensor to memory to compute, with results returned to local storage or a system interface as required. The paper does not prescribe a particular bonding process, tier thickness, or sensor modality; those choices belong to a later physical implementation.

[INSERT FIG. 1 HERE]

Caption: Fig. 1. Three-tier near-sensor organization. The diagram is architectural; it does not specify TSV geometry, bonding pitch, or thermal boundaries.

The middle tier is called localized memory rather than nonvolatile memory because the evaluated nominal component is SRAM. This corrects the ambiguity in the earlier draft. Other memory technologies may be valuable in a heterogeneous stack, but their retention, write energy, endurance, process compatibility, and temperature sensitivity are not evaluated here and therefore are not part of the reported result.

## B. Dataflow and Memory Localization

The accelerator follows an Eyeriss-like spatial hierarchy: a shared global SRAM feeds per-PE input, weight, and partial-sum register files, which in turn feed MAC units [3]. The proposed mechanism does not alter that lower hierarchy. Instead, the layer data that would be served by external LPDDR4 in the planar organization is served by an on-stack SRAM. Thus, the architectural change occurs above the 128-KiB global buffer.

Localization is defined at a specific interface. For a fixed workload and mapping, Timeloop reports the same highest-level scalar reads and writes in the planar and localized cases. In the planar case, those events are LPDDR4 actions; in the localized case, they are stacked-SRAM actions. External DRAM traffic is therefore zero in the localized model, but the highest-level event count is not zero and is not reduced. The design repositions necessary data movement rather than erasing it.

## C. Planar Baseline

The architecture produces two separable evaluation questions. First, at architecture level, what energy change follows from terminating the same high-level events in local SRAM instead of external LPDDR4? Second, at circuit level, what energy and delay change follows when an otherwise identical communication path drives a lower lumped capacitance? The first question is evaluated with Timeloop/Accelergy and CACTI-backed memory models. The second is evaluated with ngspice. Fig. 2 shows how both paths retain independent raw evidence and meet only at bounded cross-level interpretation.

[INSERT FIG. 2 HERE]

Caption: Fig. 2. Two-level evaluation workflow. Architectural and circuit percentages are reported separately and are not combined into an invented whole-system result.

Fig. 3 contrasts the controlled hierarchies. The planar baseline comprises external LPDDR4, the 128-KiB global SRAM, PE-local register files, and the 168-unit MAC array. The localized organization replaces only LPDDR4 with a nominal 2-MiB CACTI-backed SRAM. Identical workload dimensions, precision, clock period, lower buffers, compute array, and loop mapping are used in both cases.

[INSERT FIG. 3 HERE]

Caption: Fig. 3. Controlled planar and localized-memory hierarchies. Only the highest memory component changes; the global SRAM, PE register files, MAC array, and mapping are identical.

# IV. Methodology

## A. Evaluation Strategy

The evaluation uses two independent paths (Fig. 2). The architecture path quantifies workload mapping, activity, cycles, utilization, and component energy. The circuit path quantifies switching energy and propagation delay of a representative loaded CMOS communication path. Architectural percentages are computed only between Timeloop/Accelergy cases; circuit percentages are computed only between ngspice cases. No multiplication, addition, or substitution combines the two into a whole-system improvement.

All experiment artifacts are versioned. The architecture evidence is preserved at Git commit `4291da55dc45f433f6836ec0b39e96b04ccc2068`, and the SPICE evidence at `9dfd8e40ac959f1a66d024014859a340a15df101`. Each run has an input file, standard output/error capture, completion marker, processed CSV row, traceability row, and validator result. Timeloop/Accelergy runs additionally preserve maps, statistics, XML, ERT, ART, flattened architecture, and Accelergy logs. ngspice runs preserve the instantiated netlist, exact copied device model, simulator output, waveform, and checksums.

## B. Workload Selection and Characterization

We evaluate exactly two convolution layers from the repository's established AlexNet configuration [14]. Table I gives their tensor dimensions. For batch size one, the MAC count is

\[
N_{\mathrm{MAC}} = P Q K C R S,
\]

where \(P\) and \(Q\) are output height and width, \(K\) is the output-channel count, \(C\) is the input-channel count, and \(R\) and \(S\) are kernel height and width. This gives 105,415,200 MACs for CONV1 and 447,897,600 for CONV2.

An architecture-oriented intensity indicator is defined as

\[
I_{\mathrm{tensor}} = \frac{N_{\mathrm{MAC}}}{N_W + N_I + N_O},
\]

where \(N_W\), \(N_I\), and \(N_O\) are weight, input-activation, and output-activation element counts. The resulting values are 219.69 for CONV1 and 501.41 for CONV2. CONV1 is therefore termed activation/memory-intensive relative to CONV2; CONV2 is termed relatively compute-intensive. This indicator does not include cache-line granularity or achieved bandwidth and is not a roofline operational intensity.

With 8-bit weights and inputs and 16-bit outputs, the complete tensor footprints are 770,235 bytes for CONV1 and 1,079,904 bytes for CONV2. The nominal 2-MiB localized SRAM is the smallest tested power-of-two capacity that exceeds both footprints. The experiment is layer-level, not a full-network execution or accuracy evaluation.

[INSERT TABLE I HERE]

Caption: TABLE I. Workload characterization.

## C. Accelerator Configuration

Both architectures use a 14 × 12 spatial array, or 168 PEs. Each PE contains an integer MAC modeled as an 8-bit multiplier and 16-bit adder, a 12-entry input RF, a 192-entry weight RF, and a 16-entry partial-sum RF. A 16,384 × 64-bit global buffer provides 128 KiB of shared SRAM. Inputs and weights are 8 bit; partial sums and MAC outputs are 16 bit. The architectural technology is 45 nm, and `global_cycle_seconds` is 1 ns, corresponding to a nominal 1-GHz clock. Table II lists the controlled parameters.

[INSERT TABLE II HERE]

Caption: TABLE II. Common accelerator and simulation parameters.

## D. Timeloop Mapping and Activity Analysis

Timeloop [10] maps the convolution loop nest onto the spatial and temporal resources. For each workload, a mapping search is first performed on the planar reference. The selected map is copied to a fixed-mapping workload file and replayed for both architectures. Loop factors, permutations, and datatype bypass directives are therefore identical within each workload pair.

Timeloop reports total computes, cycles, utilized instances, per-level scalar reads, scalar fills, scalar updates, and component activity. In the processed results, highest-level reads are the sum of scalar reads across dataspaces at LPDDR4 or stacked SRAM. Highest-level writes are scalar fills plus scalar updates at that level. External-DRAM events equal those highest-level events only in the planar hierarchy; they are zero when no DRAM component exists in the localized input. The validator normalizes only the highest-level component name and requires the remaining problem, mapping, compute, cycle, and utilization fields to match.

## E. Accelergy and CACTI Energy Characterization

Accelergy [11] forms an energy-reference table and combines component action counts with per-action energies. For workload \(w\), total architecture energy is

\[
E_{\mathrm{total}}(w) = \sum_i \sum_a N_{i,a}(w)\,\epsilon_{i,a},
\]

where \(i\) identifies a component, \(a\) identifies an action, \(N_{i,a}\) is the Timeloop/Accelergy action count, and \(\epsilon_{i,a}\) is the corresponding ERT energy.

The planar highest level is a 64-bit-access LPDDR4 component. Its generated ERT assigns 512 pJ to read, write, and update vector actions. The nominal localized highest level is a 2-MiB, 64-bit-wide `smartbuffer_SRAM`. Its generated ERT assigns 127.645 pJ per read, 110.308 pJ per write/update, and 0.0525126 pJ leakage per cycle. The global SRAM is also CACTI-backed; PE RF and integer-MAC compound models are inherited from the official example.

SRAM characterization was obtained through the Accelergy CACTI plug-in at commit `291018b12cc9cd467168973fc47528670e1480ce` using HewlettPackard CACTI source commit `1ffd8dfb10303d306ecd8d215320aea07651e878`. The checked source identifies the implementation as the CACTI Version 7.0 line derived from 6.5 and merged with CACTI-3DD. We therefore cite both the foundational CACTI 6.0 methodology [12] and the CACTI 7 publication [13], but do not state that a “CACTI 6.0 binary” was executed.

## F. Planar and Localized-Memory Configurations

The planar path is external LPDDR4 → global SRAM → PE-local RFs → MAC. The localized path is 2-MiB stacked SRAM → the same global SRAM → the same PE-local RFs → the same MAC. No explicit TSV energy constant is inserted into the architecture model. Communication effects at this level are represented through the selected memory components and their action energies; a separately resolved network-energy metric is unavailable and is reported as `NA`, not zero.

The top-level bandwidth is unspecified in both configurations, following the reference input. This choice intentionally prevents bandwidth throttling from altering the cycles and isolates memory-technology energy. It also means that the reported 1-GHz cycle-derived times are not a bandwidth-aware end-to-end latency prediction.

## G. Controlled Fair-Comparison Protocol

For a workload pair, fairness requires equality of convolution dimensions, total MACs, PE count, PE array shape, arithmetic precision, RF capacities, global-buffer capacity, compute component, technology, clock, and fixed mapping. The validator confirms those invariants, identical cycles, and identical utilization. Only the highest-level memory name, class, capacity, and associated ERT actions differ.

This protocol deliberately excludes mapping co-optimization for the localized case. Such optimization could be useful in a future design, but would confound memory placement with a dataflow change. The present comparison therefore estimates the marginal modeled energy consequence of substituting the highest memory level.

## H. Evaluation Metrics

Reported architecture metrics are total energy, energy per Timeloop compute, cycles, utilization, highest-level reads and writes, external-DRAM events, and nominal latency calculated from the documented 1-ns period. For planar-to-localized total-energy reduction,

\[
\Delta E(w) = 100\frac{E_{\mathrm{planar}}(w)-E_{\mathrm{local}}(w)}{E_{\mathrm{planar}}(w)}.
\]

Energy per compute is total energy divided by Timeloop's total compute count. Utilization is accepted only in the closed interval [0,1]. The post-processing scripts reject negative energies, mismatched MAC counts, missing run markers, and inconsistent comparison formulas.

## I. Localized-Memory Capacity Sensitivity

For CONV1, localized SRAM capacity is swept over 2, 4, 8, and 16 MiB. The workload, mapping, access counts, compute hierarchy, 45-nm technology, and cycles remain fixed. Accelergy invokes CACTI separately for each capacity, allowing the larger array's action energy and leakage to influence total energy. This sweep evaluates sizing sensitivity; it does not model a capacity-miss transition because all tested capacities exceed the selected layer footprint.

## J. Transistor-Level Communication-Link Validation

Circuit simulation uses ngspice 42 from Ubuntu package `42+ds-3build1`, with the version-42 manual [18]. The exact device card is `45nm_HP.pm`, Git blob `160d7da3c5f3a6c0037332df5535dc07d62720ae`, SHA-256 `c9ed2e513523c57a76912a35b2860cb85e4aaa3402b69757d84efa9cc2fb8410`. Its header reads “PTM High Performance 45nm Metal Gate / High-K / Strained-Si” and states nominal \(V_{DD}=1.0\) V. The file declares `level=54`, compact-model `version=4.0`, and `tnom=27`. The exact card is attributed to the University of Minnesota PTM archive [17]; Zhao and Cao [16] are cited for the predictive-model methodology and model family rather than as the byte-level card source.

The testbench contains a CMOS output driver with 4-µm NMOS and 8-µm PMOS widths, a 1-µm/2-µm CMOS receiver, and an identical fanout-of-one load; all channel lengths are 45 nm. The input is a 1-V pulse with 20-ps rise/fall time and 1-ns period. Both nominal cases use 65 mΩ series resistance. The measured 40-fF vertical capacitance and 65-mΩ resistance come from Batra *et al.* [15]. That work reports the 40-fF TSV capacitance as less than one quarter of bump-bond capacitance; the planar proxy is therefore set to exactly 160 fF, a conservative deterministic lower bound, rather than an arbitrary fit.

The supply energy for one steady-state 1-ns cycle is

\[
E_{\mathrm{cycle}} = \left|\int_{1.05\,\mathrm{ns}}^{2.05\,\mathrm{ns}} V_{DD} I_{DD}(t)\,dt\right|.
\]

One cycle contains a rising and falling data toggle, so \(E_{\mathrm{toggle}}=E_{\mathrm{cycle}}/2\). Propagation delays are measured from the second 0.5-\(V_{DD}\) crossing at the input to the corresponding 0.5-\(V_{DD}\) crossing at the receiver output. Mean propagation delay is

\[
t_{pd}=\frac{t_{pLH}+t_{pHL}}{2}.
\]

These definitions measure a driver/link/receiver path. They do not measure an LPDDR4 PHY, a complete vertical network, or inference latency.

## K. Interconnect-Capacitance Sensitivity

The vertical-link capacitance is swept over 5, 20, 40, and 80 fF while the model card, transistors, input, supply, temperature, resistance, integration window, and measurement thresholds remain unchanged. The sweep spans one eighth to twice the measured nominal 40-fF value. The planar 160-fF proxy is plotted on the same axes for context but is not relabeled as a measured bump capacitance.

## L. Reproducibility and Traceability

Fig. 4–Fig. 8 are generated from committed CSV files by `scripts/generate_all_figures.py`; no plotted number is typed into the figure code. `CLAIM_AUDIT.md` maps every numerical manuscript claim to raw evidence or a deterministic formula. `TRACEABILITY.md` records the source branches, commits, tool/model identifiers, figure inputs, and validation boundaries. Raw architecture and circuit validators both report `FINAL_VALIDATION=PASS`. The temperature-evidence audit separately records that no temperature-labeled sensor dataset, sensor transfer model, predictions, ground truth, or accuracy metric exists. Consequently, no sensing-accuracy-versus-temperature curve is generated.

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

# VI. Physical-Design and Thermal Considerations

The modeled energy reductions do not resolve the physical design of a 3D stack. Vertical integration increases functional density and thermally couples tiers. Depending on tier ordering and package construction, heat generated in the compute tier can pass through memory or sensor structures before reaching a heat spreader. Local hot spots, memory retention and leakage, inter-tier stress, and sensor response can therefore constrain a design even when total communication energy is reduced [5], [6], [9].

Tier placement should be selected with a thermal-resistance network or finite-element package model rather than by presuming that the memory tier is intrinsically insulating. Compute placement near an efficient heat-removal path, thermal vias or dedicated heat-spreading structures, and package-level co-design are plausible options. Their effectiveness depends on materials, bond geometry, die thickness, activity maps, ambient boundary conditions, and cooling assumptions that are absent from the present architecture model.

Runtime control is also relevant. Shen *et al.* demonstrate that core DVFS and memory low-power modes are coupled in 3D processor-memory systems and should be managed jointly [9]. An edge-AI implementation could additionally use thermal-aware scheduling, duty cycling, sensor-aware acquisition throttling, or layer placement to shape activity. These are design mechanisms, not results of the reported simulations. The present Timeloop/Accelergy runs provide energy and activity estimates that could seed a future thermal model, but no temperature field is computed here.

Sensor behavior creates a separate validation obligation. Temperature can affect dark current, offset, noise, responsivity, calibration, and the downstream distribution seen by an inference model. The present evaluation does not quantify sensing accuracy as a function of temperature. Such a result requires a specified transducer, calibrated temperature-dependent sensor measurements or a validated transfer model, labeled inference data, frozen preprocessing and model parameters, raw predictions, and a stated accuracy metric. None of those inputs exists in the repository. A nominal `.temp=27` ngspice device simulation cannot produce sensing accuracy.

Accordingly, no sensing-accuracy-versus-temperature curve is reported. This is a scope boundary rather than an inferred negative result. A future study should expose the selected sensor and complete inference pipeline to controlled temperatures, use the same labeled samples at every point, report repeat counts and uncertainty, and distinguish sensor drift from circuit timing, memory, and model errors.

# VII. Discussion

The first insight is that memory placement can substantially change modeled energy even when the required computation and event count do not change. For each workload, the planar and localized cases execute identical MAC counts, loop mappings, lower-buffer activity, cycles, and utilization. The energy difference arises because the same highest-level actions use different component costs. This is a direct demonstration of why an access count alone is not an energy result: placement and memory technology determine the energy assigned to each action.

Second, the benefit is strongly workload dependent. CONV1 and CONV2 do not support a universal “approximately 70%” claim. Their reductions differ by more than forty percentage points, consistent with the much higher planar highest-level contribution in CONV1. A manuscript or design process that reports only an average would hide this central result. Workload selection and layer-by-layer characterization are therefore necessary when considering memory localization.

Third, localized capacity is not a monotonic “more is always better” variable. In the 2–16-MiB sweep, every point fits the selected CONV1 tensors, so extra capacity does not avoid an additional modeled transfer. Instead, the larger CACTI-characterized array costs more per action, and the energy reduction decreases. A complete system will trade this access-energy penalty against full-network working-set retention, area, yield, routing, and concurrency. The layer result identifies the tradeoff but does not select a network-optimal capacity.

Fourth, the ngspice experiment independently supports the electrical motivation for shorter or lower-load communication. Under identical devices and stimulus, the literature-backed 40-fF vertical proxy has lower switching energy and propagation delay than the 160-fF planar proxy, and the vertical sweep is monotonic over 5–80 fF. The testbench is intentionally small enough to audit. It does not include pad drivers, ESD, clocking, equalization, coupling, inductance, or extracted package wiring, so its absolute values should not be generalized to a commercial external-memory interface.

Fifth, link delay and inference latency are different metrics. A 46.38% reduction in one link's propagation delay does not imply a 46.38% network speedup, nor does it conflict with unchanged Timeloop cycles. Any system-level latency claim would require modeling memory-controller scheduling, interface bandwidth, stalls, link serialization, protocol overhead, and the accelerator's critical path. The present evidence supports lower link delay and lower architecture energy, separately.

J3DAI [8] provides a useful practical comparison. It demonstrates a specialized three-wafer CMOS-image-sensor and DNN-accelerator platform. This work does not claim that a generalized model is superior to that fabricated system. Its contribution is complementary: fixed-compute experiments reveal how much one memory-localization mechanism can matter for two workloads, while the link testbench checks the direction of one electrical assumption. CamJ [7] similarly highlights the need for sensor-aware system modeling beyond an accelerator-only boundary.

Several limitations bound the conclusions. Only two AlexNet layers are evaluated; no full network, sensor acquisition chain, NVM, accuracy, area, cost, yield, or thermal field is modeled. The architecture proxy replaces LPDDR4 with SRAM but does not physically simulate TSVs or hybrid bonds. External bandwidth is unconstrained, so architectural timing does not capture memory stalls. CACTI-backed memory values and PTM circuit values are predictive/model-based rather than foundry signoff. The planar capacitance is a deterministic conservative proxy, not a measured value from the proposed system. These limitations do not invalidate the reported calculations, but they prevent claims about fabricated silicon, thermal robustness, or end-to-end speedup.

The broader implication is that practical 3D edge AI is a cross-layer co-design problem. Workload tensor behavior determines reuse opportunity; mapping determines activity; memory capacity determines both locality and access cost; interconnect geometry determines electrical loading; and tier/package design determines temperature. The two-level evaluation used here exposes those dependencies while keeping each claim within the modeling level that produced it.

# VIII. Conclusion

This paper evaluated a three-tier near-sensor sensor–memory–compute organization with an established, reproducible tool chain. Two AlexNet convolution layers were mapped to the same 168-PE, 45-nm accelerator. Timeloop characterized mapping, activity, cycles, and utilization; Accelergy and CACTI-backed models estimated component energy. Replacing external LPDDR4 with nominal 2-MiB localized SRAM reduced modeled total energy from 7,343.23 to 2,256.65 µJ (69.27%) for CONV1 and from 3,103.78 to 2,261.55 µJ (27.14%) for CONV2. Cycles were unchanged within each workload pair, making workload-dependent energy reduction—not inference speedup—the architecture-level result. A 2–16-MiB sensitivity study showed that the CONV1 reduction decreased from 69.27% to 28.95% as CACTI-characterized SRAM capacity increased.

Complementary ngspice 42 simulation with the exact public 45-nm HP PTM card showed that reducing a representative link load from a 160-fF planar proxy to a literature-backed 40-fF vertical proxy reduced switching energy by 63.77% and mean propagation delay by 46.38%. These are link-level values and are not combined with the Timeloop/Accelergy totals.

Future work should extend the evaluation to full networks and bandwidth-aware timing, use post-layout parasitic extraction and a physical 3D interconnect implementation, perform package-level thermal simulation, characterize a selected sensor across temperature with labeled data, and ultimately compare against fabricated silicon.

# Acknowledgment

The author thanks the anonymous reviewers for comments that motivated the tool-based evaluation, workload-level reporting, and clearer scope boundaries in this revision.

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

# References

[1] V. Sze, Y.-H. Chen, T.-J. Yang, and J. S. Emer, “Efficient processing of deep neural networks: A tutorial and survey,” *Proc. IEEE*, vol. 105, no. 12, pp. 2295–2329, Dec. 2017, doi: 10.1109/JPROC.2017.2761740.

[2] M. Horowitz, “1.1 Computing's energy problem (and what we can do about it),” in *2014 IEEE Int. Solid-State Circuits Conf. Dig. Tech. Papers (ISSCC)*, San Francisco, CA, USA, 2014, pp. 10–14, doi: 10.1109/ISSCC.2014.6757323.

[3] Y.-H. Chen, T. Krishna, J. S. Emer, and V. Sze, “Eyeriss: An energy-efficient reconfigurable accelerator for deep convolutional neural networks,” *IEEE J. Solid-State Circuits*, vol. 52, no. 1, pp. 127–138, Jan. 2017, doi: 10.1109/JSSC.2016.2616357.

[4] W. A. Wulf and S. A. McKee, “Hitting the memory wall: Implications of the obvious,” *ACM SIGARCH Comput. Archit. News*, vol. 23, no. 1, pp. 20–24, Mar. 1995, doi: 10.1145/216585.216588.

[5] K. Banerjee, S. J. Souri, P. Kapur, and K. C. Saraswat, “3-D ICs: A novel chip design for improving deep-submicrometer interconnect performance and systems-on-chip integration,” *Proc. IEEE*, vol. 89, no. 5, pp. 602–633, May 2001.

[6] J. U. Knickerbocker *et al.*, “Three-dimensional silicon integration,” *IBM J. Res. Develop.*, vol. 52, no. 6, pp. 553–569, Nov. 2008.

[7] T. Ma, Y. Feng, X. Zhang, and Y. Zhu, “CamJ: Enabling system-level energy modeling and architectural exploration for in-sensor visual computing,” in *Proc. 50th Annu. Int. Symp. Comput. Archit. (ISCA)*, Orlando, FL, USA, 2023, Art. no. 29, pp. 1–14, doi: 10.1145/3579371.3589064.

[8] B. Tain *et al.*, “J3DAI: A tiny DNN-based edge AI accelerator for 3D-stacked CMOS image sensor,” in *Proc. IEEE/ACM Int. Symp. Low Power Electron. Design (ISLPED)*, Reykjavík, Iceland, 2025, pp. 1–7.

[9] Y. Shen, L. Schreuders, A. Pathania, and A. D. Pimentel, “Thermal management for 3D-stacked systems via unified core-memory power regulation,” *ACM Trans. Embedded Comput. Syst.*, vol. 22, no. 5s, Art. no. 120, pp. 1–26, Sep. 2023, doi: 10.1145/3608040.

[10] A. Parashar *et al.*, “Timeloop: A systematic approach to DNN accelerator evaluation,” in *Proc. IEEE Int. Symp. Perform. Anal. Syst. Softw. (ISPASS)*, Madison, WI, USA, 2019, pp. 304–315, doi: 10.1109/ISPASS.2019.00042.

[11] Y. N. Wu, J. S. Emer, and V. Sze, “Accelergy: An architecture-level energy estimation methodology for accelerator designs,” in *Proc. IEEE/ACM Int. Conf. Comput.-Aided Design (ICCAD)*, Westminster, CO, USA, 2019, pp. 1–8, doi: 10.1109/ICCAD45719.2019.8942149.

[12] N. Muralimanohar, R. Balasubramonian, and N. P. Jouppi, “Optimizing NUCA organizations and wiring alternatives for large caches with CACTI 6.0,” in *Proc. 40th Annu. IEEE/ACM Int. Symp. Microarchitecture (MICRO)*, Chicago, IL, USA, 2007, pp. 3–14, IEEE Xplore document 4408241.

[13] R. Balasubramonian, A. B. Kahng, N. Muralimanohar, A. Shafiee, and V. Srinivas, “CACTI 7: New tools for interconnect exploration in innovative off-chip memories,” *ACM Trans. Archit. Code Optim.*, vol. 14, no. 2, Art. no. 14, pp. 1–25, Jun. 2017, doi: 10.1145/3085572.

[14] A. Krizhevsky, I. Sutskever, and G. E. Hinton, “ImageNet classification with deep convolutional neural networks,” in *Advances in Neural Information Processing Systems 25*, 2012, pp. 1097–1105.

[15] P. Batra *et al.*, “Three-dimensional wafer stacking using Cu TSV integrated with 45 nm high performance SOI-CMOS embedded DRAM technology,” *J. Low Power Electron. Appl.*, vol. 4, no. 2, pp. 77–89, May 2014, doi: 10.3390/jlpea4020077.

[16] W. Zhao and Y. Cao, “New generation of predictive technology model for sub-45 nm early design exploration,” *IEEE Trans. Electron Devices*, vol. 53, no. 11, pp. 2816–2823, Nov. 2006, doi: 10.1109/TED.2006.884077.

[17] University of Minnesota, “Predictive Technology Model (PTM),” 45-nm high-performance bulk-CMOS model. [Online]. Available: https://mec.umn.edu/ptm. Accessed: Aug. 14, 2026.

[18] ngspice development team, *ngspice User's Manual*, Version 42, Dec. 27, 2023. [Online]. Available: https://sourceforge.net/projects/ngspice/files/ng-spice-rework/old-releases/42/ngspice-42-manual.pdf/download. Accessed: Aug. 14, 2026.
