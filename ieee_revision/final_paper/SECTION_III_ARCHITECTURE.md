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
