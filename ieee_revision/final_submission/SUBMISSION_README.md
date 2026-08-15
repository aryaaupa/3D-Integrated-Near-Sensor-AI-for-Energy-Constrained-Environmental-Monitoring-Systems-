# JxCDC / IEEE Submission Package

This directory is the hardened submission source. Scientific values are unchanged from the validated five-workload Timeloop/Accelergy and ngspice evidence.

## Upload to the journal portal

1. `MANUSCRIPT_FINAL_CLEAN.md` - transfer this clean text into the required IEEE/JxCDC Word or LaTeX template.
2. `03_RESPONSE_TO_REVIEWERS_FINAL.md` - upload as the point-by-point response.
3. `MANUSCRIPT_FINAL_MARKED.md` - upload only if the portal requests a marked revision.
4. `04_SUPPLEMENTARY_MATERIAL.md` - upload if supplementary material is accepted.
5. Main figure PDFs from `figures/main/`:
   - `fig1_architecture.pdf`
   - `fig2_controlled_comparison.pdf`
   - `fig3_methodology.pdf`
   - `fig4_five_workload_energy.pdf`
   - `fig5_component_energy.pdf`
   - `fig6_capacity_sensitivity.pdf`
   - `fig7_link_energy.pdf`
   - `fig8_link_delay.pdf`
6. Supplementary figure PDFs, if the supplement is uploaded:
   - `figS1_mechanism_comparison.pdf`
   - `figS2_energy_per_compute.pdf`
   - `figS4_external_dram_actions.pdf`

## Do not upload as manuscript files unless requested

- `HOSTILE_REVIEWER_AUDIT.md`
- `05_CLAIM_AUDIT_FINAL.md`
- `07_REFERENCE_AUDIT_FINAL.md`
- `figure_data/`
- `scripts/`
- `evidence_manifest/`
- PNG/SVG figure copies when the portal accepts the PDF originals

## Final evidence boundary

The demonstrated architecture contribution is a controlled external-LPDDR4-to-localized-SRAM substitution motivated by a proposed 3D near-sensor organization. Timeloop does not physically model a 3D stack. The circuit percentages compare only a conservative 160-fF planar-link proxy with a literature-referenced 40-fF TSV case in an identical representative testbench.

