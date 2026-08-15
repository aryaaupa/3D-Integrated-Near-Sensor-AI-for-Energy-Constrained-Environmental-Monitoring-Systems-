# Final submission checklist

## Manuscript completeness

- [x] Title, author line, affiliation, abstract, index terms, Sections I–VIII, and one bibliography are present; no acknowledgment section is included because no institutional or funding acknowledgment was supplied.
- [x] Abstract is 217 words, within the requested approximately 180–230-word range.
- [x] `COPY_PASTE_MANUSCRIPT.txt` is plain text with numbered citations, explicit figure/table insertion markers, captions, and no Markdown headings.
- [x] Tables I–V are present and use only evidence-backed or qualitative fields.
- [x] Reviewer-response letter addresses every supplied issue from Reviewers 1–3.

## Evidence and scientific scope

- [x] Architecture results originate from passing Timeloop/Accelergy runs at commit `4291da55dc45f433f6836ec0b39e96b04ccc2068`.
- [x] Circuit results originate from passing ngspice runs at commit `9dfd8e40ac959f1a66d024014859a340a15df101`.
- [x] Planar/localized pairs use identical workloads, mappings, compute array, precision, lower hierarchy, technology, and clock.
- [x] AlexNet CONV1 and dense CONV2 MAC counts match within each architecture pair.
- [x] Dense CONV2 is explicitly distinguished from canonical grouped AlexNet CONV2; the evaluated configuration connects every 5 × 5 filter to all 96 input channels.
- [x] All reported energy values are nonnegative; all reported utilization values lie in [0,1].
- [x] Highest-level event count (unchanged) is distinguished from external-DRAM interface events (zero in localized inputs).
- [x] Timeloop cycles are reported as unchanged; no architectural speedup is claimed.
- [x] Link delay is identified as a circuit-level result, not inference latency.
- [x] Link energy is not added to architecture energy, avoiding an unresolved double count.
- [x] No silicon, post-layout, extracted-package, or quantitative thermal claim is made.
- [x] No sensing-accuracy-versus-temperature curve is generated because required evidence is absent.

## Figures and tables

- [x] Figures 1–8 exist as PDF and PNG.
- [x] Quantitative figures read committed CSV inputs; plotted values are not manually retyped in the plotting code.
- [x] Every PDF was rendered to raster form and visually inspected for clipping, overlap, legibility, and correct labels.
- [x] Figure axes use absolute units and nonmisleading zero baselines where appropriate.
- [x] Figure captions state the relevant modeling boundary.

## Citations and provenance

- [x] Citations [1]–[18] are unique and appear in one IEEE bibliography.
- [x] Each citation is mapped to a supported claim and primary/official source in `reference_audit.md`.
- [x] Zhao and Cao are used for PTM methodology; the exact card is separately attributed to the University of Minnesota archive.
- [x] The cited ngspice manual matches the executed major version 42.
- [x] CACTI wording identifies the executed pinned source as the Version 7.0 line derived from 6.5; the manuscript does not claim that a CACTI 6.0 binary ran.
- [x] The conflicted CACTI 6.0 DOI is omitted rather than guessed.

## Claim and wording audit

- [x] Every experimental/configuration number is mapped to raw output or a deterministic calculation in `CLAIM_AUDIT.md`.
- [x] Legacy claims `45–70%`, `45-70%`, `1.6×`, `1.6x`, `2.5×`, `2.5x`, `60–80%`, and `60-80%` are absent.
- [x] Unsupported assertions of higher utilization, end-to-end speedup, generic 60–80% total-data-movement reduction, demonstrated thermal benefit, steady-state temperature reduction, or improved thermal uniformity are absent.
- [x] No TODO, placeholder request to the author, fabricated value, or invented simulation remains.
- [x] The main conclusion is workload-dependent memory-localization energy reduction, not a universal 3D multiplier.

## Reproduction files

- [x] `scripts/generate_all_figures.py` regenerates all figures from `figure_data/`.
- [x] `scripts/assemble_manuscript.py` regenerates the unified Markdown and copy-paste text from the modular manuscript files.
- [x] `TRACEABILITY.md` records evidence commits, raw paths, tool/model identifiers, figure inputs, and modeling boundaries.
- [x] `reference_audit.md` and `CLAIM_AUDIT.md` are included for editorial audit.

Status: ready for author-side placement into the IEEE JxCDC template and final formatting review. No additional experimental claim is needed for the submitted evidence scope.
