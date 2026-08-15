# Timeloop + Accelergy setup status

Fresh verification completed successfully on 2026-08-14 UTC.

## Installed tools

- Accelergy from commit `6911d15686ee7efdceba7d95605102df4472ae3a`
- Timeloop from commit `32370826fdf1aa3c8deb0c93e6b2a2fc7cf053aa`
- Python virtual environment: `/workspace/scratch/ae4887560717/timeloop-env`
- Accelergy executable: `/workspace/scratch/ae4887560717/timeloop-env/bin/accelergy`
- Timeloop model launcher: `/workspace/scratch/ae4887560717/timeloop-env/bin/timeloop-model`
- Timeloop mapper launcher: `/workspace/scratch/ae4887560717/timeloop-env/bin/timeloop-mapper`
- Compiled Timeloop binaries: `/workspace/scratch/ae4887560717/accelergy-timeloop-infrastructure/src/timeloop/build/`

Timeloop and Barvinok were compiled with one build job (`-j1`). Barvinok was
built with position-independent code because Timeloop links it into a shared
library. The launchers supply the local runtime-library paths and provide
conventional `-h`/`--help` behavior for this pinned Timeloop revision.

## Proof commands

All returned exit status 0 in the fresh run:

```bash
source /workspace/scratch/ae4887560717/timeloop-env/bin/activate
accelergy -h
timeloop-model --help
timeloop-mapper --help
```

The unedited command output and exit statuses are in `final_verification.txt`.

## Official example

The official preprocessed `intmac` input at
`workspace/tutorial_exercises/01_accelergy_timeloop_2020_ispass/timeloop+accelergy/ref-output/intmac/parsed-processed-input.yaml`
completed with mapper exit status 0.

Fresh result summary:

```text
Utilization = 1.00 | pJ/Compute = 4.840 | Cycles = 5505024
```

The complete raw stdout/stderr is `official_example_raw_output.txt`. All
generated ERT, ART, architecture, map, XML, statistics, and Accelergy log files
are stored beside this status file in `ieee_revision/setup_evidence/`.
