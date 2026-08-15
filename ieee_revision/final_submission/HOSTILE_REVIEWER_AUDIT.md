# Hostile-Reviewer Submission Audit

This audit challenges the hardened manuscript against the most likely technical objections. It is an internal submission-control document, not manuscript text.

| Risk | Hostile-reviewer challenge | Hardened treatment | Status |
|---|---|---|---|
| 3D overclaiming | Timeloop does not physically model tiers, TSVs, or a package. | Title, abstract, introduction, methodology, captions, discussion, and conclusion define the demonstrated result as a controlled LPDDR4-to-localized-SRAM study motivated by a proposed 3D organization. | PASS |
| SRAM-vs-DRAM confounding | The comparison changes memory technology as well as placement. | Sections III-B, IV-D, VII-A, and VII-D explicitly disclose that the proxy couples technology and placement and does not isolate a geometry-only 3D effect. | PASS |
| Workload naming | Canonical AlexNet CONV2/4/5 use grouped convolution. | Every manuscript-facing occurrence uses “AlexNet-derived dense CONV2,” “AlexNet-derived dense CONV4,” or “AlexNet-derived dense CONV5.” Tables and supplement disclose the connectivity difference. | PASS |
| Proxy capacitance | A 160-fF bump value was not measured by Batra et al. | The manuscript identifies 40 fF as the literature-referenced TSV case and 160 fF as a conservative deterministic planar-link proxy derived as 4 x 40 fF. Captions state that 160 fF is not a measured bump. | PASS |
| Circuit percentages | 63.77% and 46.38% could be misread as generic planar-versus-3D improvements. | Every circuit percentage is tied to the representative 160-fF proxy versus 40-fF TSV testbench cases. The text rejects generic hardware and inference-speed interpretations. | PASS |
| Latency language | Link propagation delay or cycles x 1 ns could be mistaken for end-to-end inference latency. | The manuscript uses “cycle-derived execution time” for architecture timing and “representative-path propagation delay” for ngspice. External bandwidth is unconstrained, and no inference-latency improvement is claimed. | PASS |
| Statistical overinterpretation | Five samples cannot establish a universal relationship. | The main text uses bounded language. Supplementary Fig. S1 labels all five points, fits no regression, and explicitly states that no statistical or workload-universal relationship is inferred. | PASS |
| Reproducibility | Tool versions, mappings, model provenance, or raw evidence may be unclear. | Tool commits, container digest, mapping-freeze protocol, PTM header/hash, ngspice package, formulas, traceability paths, and validators are documented in the manuscript and supplement. | PASS |
| Component mechanism | Total-energy reductions could be asserted without component evidence. | Main Fig. 5 is generated from committed component-energy columns and shows highest memory, unchanged lower buffers, and unchanged compute for all ten runs. Component sums are validated against total energy. | PASS |
| Figure-caption self-containment | Captions may omit the controlled variable or evidence boundary. | Captions specify workload scope, P/L meaning, fixed architecture/mapping, proxy definitions, and the distinction between circuit delay and inference latency. | PASS |
| Reference accuracy | CACTI/PTM/ngspice sources may be conflated. | References distinguish foundational CACTI 6.0 methodology, executed CACTI 7 code-line context, Zhao-Cao predictive-model methodology, the exact PTM archive, and the version-42 ngspice manual. | PASS WITH DISCLOSED BIBLIOGRAPHIC LIMITATION |
| Unsupported validation | The manuscript could imply silicon, physical extraction, thermal, or sensor-accuracy results. | These claims are explicitly excluded in the abstract, methodology, physical-design section, limitations, and conclusion. | PASS |

## Remaining defensible limitations

- The five workloads are individual convolution configurations, not full-network inference.
- The LPDDR4-to-SRAM comparison intentionally combines memory technology and placement.
- External-memory bandwidth does not constrain Timeloop cycles in these runs.
- Network energy is unavailable as a separate reported component.
- The link is a lumped representative testbench, not an extracted TSV/package path.
- No physical design, thermal field, fabricated-silicon, or sensing-accuracy experiment exists.
- Five samples support descriptive interpretation only.

