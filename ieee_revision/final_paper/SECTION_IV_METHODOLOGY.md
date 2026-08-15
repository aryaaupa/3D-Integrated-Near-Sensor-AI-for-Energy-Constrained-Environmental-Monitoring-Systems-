# IV. Methodology

## A. Evaluation Strategy

The evaluation uses two independent paths (Fig. 2). The architecture path quantifies workload mapping, activity, cycles, utilization, and component energy. The circuit path quantifies switching energy and propagation delay of a representative loaded CMOS communication path. Architectural percentages are computed only between Timeloop/Accelergy cases; circuit percentages are computed only between ngspice cases. No multiplication, addition, or substitution combines the two into a whole-system improvement.

All experiment artifacts are versioned. The architecture evidence is preserved at Git commit `4291da55dc45f433f6836ec0b39e96b04ccc2068`, and the SPICE evidence at `9dfd8e40ac959f1a66d024014859a340a15df101`. Each run has an input file, standard output/error capture, completion marker, processed CSV row, traceability row, and validator result. Timeloop/Accelergy runs additionally preserve maps, statistics, XML, ERT, ART, flattened architecture, and Accelergy logs. ngspice runs preserve the instantiated netlist, exact copied device model, simulator output, waveform, and checksums.

## B. Workload Selection and Characterization

We evaluate exactly two convolution workloads. The first is AlexNet CONV1 [14]. The second workload uses the spatial dimensions of AlexNet CONV2 but is modeled as a dense 5 × 5 convolution over all 96 input channels, consistent with the evaluated Timeloop workload configuration. We therefore call it the **AlexNet-derived dense CONV2 configuration** rather than canonical AlexNet CONV2. Table I gives both tensor definitions. For batch size one, the MAC count is

\[
N_{\mathrm{MAC}} = P Q K C R S,
\]

where \(P\) and \(Q\) are output height and width, \(K\) is the output-channel count, \(C\) is the input-channel count, and \(R\) and \(S\) are kernel height and width. This gives 105,415,200 MACs for AlexNet CONV1 and 447,897,600 for the dense CONV2 configuration.

An architecture-oriented intensity indicator is defined as

\[
I_{\mathrm{tensor}} = \frac{N_{\mathrm{MAC}}}{N_W + N_I + N_O},
\]

where \(N_W\), \(N_I\), and \(N_O\) are weight, input-activation, and output-activation element counts. The resulting values are 219.69 for AlexNet CONV1 and 501.41 for dense CONV2. CONV1 is therefore termed activation/memory-intensive relative to dense CONV2; dense CONV2 is termed relatively compute-intensive. This indicator does not include cache-line granularity or achieved bandwidth and is not a roofline operational intensity.

With 8-bit weights and inputs and 16-bit outputs, the complete tensor footprints are 770,235 bytes for CONV1 and 1,079,904 bytes for dense CONV2. The nominal 2-MiB localized SRAM is the smallest tested power-of-two capacity that exceeds both footprints. The experiment is layer-level, not a full-network execution or accuracy evaluation.

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

Reported architecture metrics are total energy, energy per Timeloop compute, cycles, utilization, highest-level reads and writes, external-DRAM events, and cycle-derived execution time calculated from the documented 1-ns period. For planar-to-localized total-energy reduction,

\[
\Delta E(w) = 100\frac{E_{\mathrm{planar}}(w)-E_{\mathrm{local}}(w)}{E_{\mathrm{planar}}(w)}.
\]

Energy per compute is total energy divided by Timeloop's total compute count. Utilization is accepted only in the closed interval [0,1]. The post-processing scripts reject negative energies, mismatched MAC counts, missing run markers, and inconsistent comparison formulas.

## I. Localized-Memory Capacity Sensitivity

For CONV1, localized SRAM capacity is swept over 2, 4, 8, and 16 MiB. The workload, mapping, access counts, compute hierarchy, 45-nm technology, and cycles remain fixed. Accelergy invokes CACTI separately for each capacity, allowing the larger array's action energy and leakage to influence total energy. This sweep evaluates sizing sensitivity; it does not model a capacity-miss transition because all tested capacities exceed the selected layer footprint.

## J. Transistor-Level Communication-Link Validation

Circuit simulation uses ngspice 42 from Ubuntu package `42+ds-3build1`, with the version-42 manual [18]. The exact device card is `45nm_HP.pm`, Git blob `160d7da3c5f3a6c0037332df5535dc07d62720ae`, SHA-256 `c9ed2e513523c57a76912a35b2860cb85e4aaa3402b69757d84efa9cc2fb8410`. Its header reads “PTM High Performance 45nm Metal Gate / High-K / Strained-Si” and states nominal \(V_{DD}=1.0\) V. The file declares `level=54`, compact-model `version=4.0`, and `tnom=27`. The exact card is attributed to the University of Minnesota PTM archive [17]; Zhao and Cao [16] are cited for the predictive-model methodology and model family rather than as the byte-level card source.

The testbench contains a CMOS output driver with 4-µm NMOS and 8-µm PMOS widths, a 1-µm/2-µm CMOS receiver, and an identical fanout-of-one load; all channel lengths are 45 nm. The input is a 1-V pulse with 20-ps rise/fall time and 1-ns period. Both nominal cases use 65 mΩ series resistance. Batra *et al.* report approximately 40 fF for the evaluated TSV structure and state that bump capacitance exceeds four times the TSV capacitance [15]. We therefore use 160 fF as a conservative planar-link load proxy for the controlled circuit comparison; it is not presented as a measured bump capacitance. The 65-mΩ series resistance is also taken from Batra *et al.* [15].

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

The vertical-link capacitance is swept over 5, 20, 40, and 80 fF while the model card, transistors, input, supply, temperature, resistance, integration window, and measurement thresholds remain unchanged. The sweep spans one eighth to twice the 40-fF TSV reference. The conservative 160-fF planar-link proxy is plotted on the same axes for context and is not labeled as a measured bump capacitance.

## L. Reproducibility and Traceability

Fig. 4–Fig. 8 are generated from committed CSV files by `scripts/generate_all_figures.py`; no plotted number is typed into the figure code. `CLAIM_AUDIT.md` maps every numerical manuscript claim to raw evidence or a deterministic formula. `TRACEABILITY.md` records the source branches, commits, tool/model identifiers, figure inputs, and validation boundaries. Raw architecture and circuit validators both report `FINAL_VALIDATION=PASS`. The temperature-evidence audit separately records that no temperature-labeled sensor dataset, sensor transfer model, predictions, ground truth, or accuracy metric exists. Consequently, no sensing-accuracy-versus-temperature curve is generated.
