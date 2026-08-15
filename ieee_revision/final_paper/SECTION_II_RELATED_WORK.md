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
