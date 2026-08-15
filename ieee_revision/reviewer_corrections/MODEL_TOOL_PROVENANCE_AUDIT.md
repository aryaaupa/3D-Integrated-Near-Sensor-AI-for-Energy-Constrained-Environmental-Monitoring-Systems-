# Model and tool provenance audit

## Audit basis

This audit inspects the exact artifacts used by the successful simulations,
not filenames inferred from prose. The authoritative run is commit
`9dfd8e40ac959f1a66d024014859a340a15df101` on branch
`agent/spice-link-validation`.

## PTM model actually simulated

The committed source card is:

`ieee_revision/spice_validation/models/45nm_HP.pm`

The successful nominal vertical run contains the copied card at:

`ieee_revision/spice_validation/raw_outputs/vertical_40fF/model.pm`

Both paths resolve to Git blob
`160d7da3c5f3a6c0037332df5535dc07d62720ae`. The recorded SHA-256 is
`c9ed2e513523c57a76912a35b2860cb85e4aaa3402b69757d84efa9cc2fb8410`.
The file header is exactly:

```text
* PTM High Performance 45nm Metal Gate / High-K / Strained-Si
* nominal Vdd = 1.0V
```

The card declares NMOS and PMOS models with `level = 54`, compact-model
`version = 4.0`, and `tnom = 27`. The official University of Minnesota PTM
archive lists a 45-nm high-performance bulk-CMOS model and links the model
card. The same archive lists Zhao and Cao among the PTM references.

### Citation boundary

Zhao and Cao should be cited for the predictive-technology-model methodology
and bulk-CMOS model family. The exact card should separately be attributed to
the University of Minnesota PTM archive. The manuscript should not imply that
the paper itself embeds or uniquely identifies the exact bytes of
`45nm_HP.pm`.

Recommended IEEE reference:

W. Zhao and Y. Cao, “New generation of predictive technology model for
sub-45 nm early design exploration,” *IEEE Trans. Electron Devices*, vol. 53,
no. 11, pp. 2816–2823, Nov. 2006, doi:
10.1109/TED.2006.884077.

Exact-card source:

University of Minnesota, “Predictive Technology Model (PTM),” 45-nm HP bulk
CMOS model. [Online]. Available: https://mec.umn.edu/ptm

### Manuscript-safe wording

> Transient simulations used the high-performance 45-nm bulk-CMOS PTM model
> card distributed by the University of Minnesota PTM archive. The exact
> committed card is `45nm_HP.pm` (SHA-256: `c9ed2e...`); its header identifies
> a metal-gate/high-k/strained-Si model with nominal VDD = 1.0 V, and the card
> declares BSIM4 version 4.0 parameters with nominal temperature 27 °C. Zhao
> and Cao are cited for the underlying PTM methodology.

## ngspice version actually executed

`logs/bootstrap_ngspice.txt` records:

- `ngspice-42`;
- KLU direct linear solver enabled;
- build creation date `Sun Mar 31 20:15:14 UTC 2024`.

`logs/toolchain_provenance.txt` records the Ubuntu 24.04 package
`ngspice_42+ds-3build1_amd64.deb` and package SHA-256
`466c4c06418107ceaa9c9457065b3bb71a9d9dc5ec6fef186d7de9d5208ce8db`.

The version-matched documentation is the official *ngspice User's Manual,
Version 42*, preserved in the ngspice release-42 archive dated 27 December
2023. The current manual may be cited for general project documentation, but
the version-42 manual is the reproducibility reference for this run.

Recommended reference:

ngspice development team, *ngspice User's Manual*, Version 42, Dec. 27, 2023.
[Online]. Available:
https://sourceforge.net/projects/ngspice/files/ng-spice-rework/old-releases/42/ngspice-42-manual.pdf/download

Official documentation index:

https://ngspice.sourceforge.io/docs.html

### Manuscript-safe wording

> Circuit-level transient analysis was performed with ngspice 42 using the
> version-42 user manual. The exact Ubuntu package and checksum are preserved
> with the run evidence.

## CACTI code actually invoked

The architecture evidence records:

- Accelergy CACTI plug-in commit
  `291018b12cc9cd467168973fc47528670e1480ce`;
- HewlettPackard CACTI source commit
  `1ffd8dfb10303d306ecd8d215320aea07651e878`.

Accelergy logs explicitly identify `CactiSRAM` and record the 45-nm CACTI
calls, including `cache_size`, `block_size`, and `tech_node_um=0.045`. The
README at the pinned CACTI commit identifies the code line as Version 7.0,
derived from Version 6.5 and merged with CACTI-3DD. Therefore, the executed
code must not be called a CACTI 6.0 binary.

The MICRO 2007 paper remains a primary citation for the CACTI methodology:

N. Muralimanohar, R. Balasubramonian, and N. P. Jouppi, “Optimizing NUCA
organizations and wiring alternatives for large caches with CACTI 6.0,” in
*Proc. 40th Annu. IEEE/ACM Int. Symp. Microarchitecture (MICRO)*, 2007,
pp. 3–14, IEEE Xplore document 4408241.

### DOI warning

Publisher indexes are inconsistent. IEEE Xplore and the IEEE Computer Society
record currently display `10.1109/MICRO.2007.33` for document 4408241, while
the ACM Digital Library associates `10.1109/MICRO.2007.30` with this title and
uses `.33` for a different MICRO paper. Until the publisher metadata conflict
is resolved, the safest traceable manuscript reference is the IEEE Xplore
document URL and document number rather than presenting an unchecked DOI as
unambiguous:

https://ieeexplore.ieee.org/document/4408241/

Pinned implementation source:

https://github.com/HewlettPackard/cacti/commit/1ffd8dfb10303d306ecd8d215320aea07651e878

### Manuscript-safe wording

> SRAM action energies were generated through the Accelergy CACTI plug-in
> using the pinned HewlettPackard CACTI source snapshot
> `1ffd8dfb...`. The executed source identifies itself as the Version 7.0 line;
> the foundational CACTI 6.0 publication is cited for methodology rather than
> misidentifying the executable version.

## Result

The existing numerical results remain unchanged. This audit corrects only
tool/model identity and citation wording.
