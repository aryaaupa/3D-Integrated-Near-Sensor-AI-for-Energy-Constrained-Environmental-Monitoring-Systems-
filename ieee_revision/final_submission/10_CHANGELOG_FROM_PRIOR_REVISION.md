# Changelog from Prior Revision

## Scientific reconstruction

- Replaced the two-workload architecture narrative with five validated planar/localized workload pairs.
- Added AlexNet CONV3 and AlexNet-derived dense CONV4 and dense CONV5.
- Corrected terminology so CONV2, CONV4, and CONV5 are not presented as canonical grouped AlexNet layers.
- Changed the headline architecture result from two isolated reductions to the verified 8.36%-69.27% range.
- Retained and discussed the 8.36% CONV3 result as evidence of workload dependence.
- Removed the implication that the scalar tensor-intensity indicator predicts localization benefit.
- Added component/activity analysis showing that planar highest-memory energy share directly explains the reduction under the controlled substitution.
- Clarified that highest-level logical action counts are unchanged and that zero localized external-DRAM actions arise from replacing the component with SRAM.

## Methodology and provenance

- Preserved the fixed-mapping, identical-compute fair-comparison protocol.
- Added exact five-workload YAML provenance and connectivity interpretation.
- Corrected CACTI language: the executed pinned source is the Version 7.0 line; the CACTI 6.0 paper is methodological background.
- Preserved the CACTI 6.0 publisher-DOI metadata warning rather than guessing between conflicting records.
- Added exact PTM card header, SHA-256, BSIM4 version, nominal supply, and nominal temperature.
- Separated Zhao/Cao predictive-model methodology from the University of Minnesota exact-card lineage.
- Matched the ngspice citation to the executed Version 42 manual and package.

## Figures and tables

- Rebuilt the main figure sequence as three scientific schematics plus four quantitative figures.
- Replaced the two-workload energy plot with a five-workload grouped bar chart.
- Moved energy-per-compute, intensity scatter, component breakdown, and external-DRAM activity to the supplement.
- Added vector SVG output and 600-dpi PNG output for every generated quantitative figure.
- Expanded Tables I and III to five workloads.

## Claim corrections

- Removed architectural speedup, increased-utilization, generic all-data-movement, demonstrated thermal-improvement, thermal-uniformity, and sensing-accuracy claims.
- Kept link propagation delay separate from cycle-derived execution time and inference latency.
- Kept architecture and circuit percentage reductions separate.
- Explicitly declined to fabricate sensing accuracy versus temperature.

## Submission organization

- Added a clean manuscript, readable marked manuscript, final reviewer response, structured supplement, final claim audit, final reference audit, captions, tables, evidence manifest, validation script, and upload checklist.
