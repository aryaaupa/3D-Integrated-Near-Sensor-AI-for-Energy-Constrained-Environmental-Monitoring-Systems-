# Provenance and Reviewer 2 correction pack

This directory records a targeted audit of the transistor-model, simulator,
and CACTI provenance used in the verified evaluation, together with the
disposition of Reviewer 2's request for sensing accuracy versus temperature.

No simulation result is created or changed here. The audit is based on the
published evidence at commit `9dfd8e40ac959f1a66d024014859a340a15df101`
and the architecture evidence inherited from commit
`4291da55dc45f433f6836ec0b39e96b04ccc2068`.

Files:

- `MODEL_TOOL_PROVENANCE_AUDIT.md`: exact PTM, ngspice, and CACTI identities,
  citations, and manuscript-safe wording.
- `REVIEWER_2_TEMPERATURE_RESPONSE.md`: evidence decision, reviewer response,
  replacement manuscript language, and unsupported statements to remove.
- `temperature_accuracy_evidence_audit.csv`: machine-readable record showing
  why no accuracy-versus-temperature curve was generated.

The absence of a curve is deliberate. The repository contains no
temperature-labeled sensing dataset or sensor/model predictions, and ngspice
link simulation cannot establish sensing accuracy.
