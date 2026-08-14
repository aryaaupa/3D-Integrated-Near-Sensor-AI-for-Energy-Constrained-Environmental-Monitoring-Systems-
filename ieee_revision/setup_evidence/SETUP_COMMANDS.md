# Exact setup and verification commands

These are the successful commands used in the reset workspace. Absolute paths
are retained so the evidence identifies the exact environment that produced it.

## Environment and Accelergy

```bash
ROOT=/workspace/scratch/ae4887560717
python3.12 -m venv "$ROOT/timeloop-env"
source "$ROOT/timeloop-env/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install cmake scons libconf numpy joblib ruamel.yaml PyYAML
python -m pip install "$ROOT/accelergy-timeloop-infrastructure/src/accelergy"
python -m pip install "$ROOT/accelergy-timeloop-infrastructure/src/accelergy-library-plugin"
python -m pip install "$ROOT/accelergy-timeloop-infrastructure/src/accelergy-table-based-plug-ins"
python -m pip install "$ROOT/accelergy-timeloop-infrastructure/src/accelergy-aladdin-plug-in"
```

## Barvinok and Timeloop (memory-safe)

The Debian development packages were downloaded and extracted into
`$ROOT/timeloop-build/sysroot`; their include and library directories were used
without rebuilding Boost, libconfig++, GMP, ncurses, NTL, or yaml-cpp.

```bash
BUILD="$ROOT/timeloop-build"
SYSROOT="$BUILD/sysroot"
PREFIX="$BUILD/prefix"
BAR="$BUILD/deps/barvinok-0.41.8"

cd "$BAR"
export CPPFLAGS="-I$SYSROOT/usr/include -I$SYSROOT/usr/include/x86_64-linux-gnu"
export CFLAGS="-fPIC"
export CXXFLAGS="-fPIC"
export LDFLAGS="-L$SYSROOT/usr/lib/x86_64-linux-gnu -Wl,-rpath,$SYSROOT/usr/lib/x86_64-linux-gnu"
export LD_LIBRARY_PATH="$SYSROOT/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PKG_CONFIG_PATH="$SYSROOT/usr/lib/x86_64-linux-gnu/pkgconfig"
./configure --prefix="$PREFIX" --with-ntl-prefix="$SYSROOT/usr" --with-isl=bundled
make -j1
make install

TIMELOOP="$ROOT/accelergy-timeloop-infrastructure/src/timeloop"
test -e "$TIMELOOP/src/pat" || ln -s ../pat-public/src/pat "$TIMELOOP/src/pat"
cd "$TIMELOOP"
source "$ROOT/timeloop-env/bin/activate"
export BOOSTDIR="$SYSROOT/usr"
export LIBCONFIGPATH="$SYSROOT/usr"
export YAMLCPPPATH="$SYSROOT/usr"
export NCURSESPATH="$SYSROOT/usr"
export BARVINOKPATH="$PREFIX"
export NTLPATH="$SYSROOT/usr"
export CPLUS_INCLUDE_PATH="$SYSROOT/usr/include:$SYSROOT/usr/include/x86_64-linux-gnu:$PREFIX/include"
export LIBRARY_PATH="$SYSROOT/usr/lib/x86_64-linux-gnu:$PREFIX/lib"
export LD_LIBRARY_PATH="$TIMELOOP/build:$SYSROOT/usr/lib/x86_64-linux-gnu:$PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
scons --accelergy -j1
```

## CACTI plugin

```bash
PLUGIN="$ROOT/accelergy-timeloop-infrastructure/src/accelergy-cacti-plug-in"
cd "$PLUGIN/cacti"
make -j1
cd "$PLUGIN"
PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_CACHE_DIR="$ROOT/pip-cache" \
  python -m pip install --no-deps --no-build-isolation "$PLUGIN"
```

The installed Aladdin plugin's two legacy width-normalization sites were fixed
to map `n_bits`, `precision`, or `max(width_a, width_b)` to `width`. This is the
same compatibility correction used by the recovered working setup.

## Fresh proof commands

```bash
source "$ROOT/timeloop-env/bin/activate"
accelergy -h
timeloop-model --help
timeloop-mapper --help
```

Raw output and exit statuses: `final_verification.txt`.

## Fresh official `intmac` run

```bash
EVIDENCE="$ROOT/timeloop-accelergy-exercises/ieee_revision/setup_evidence"
EXAMPLE="$ROOT/timeloop-accelergy-exercises/workspace/tutorial_exercises/01_accelergy_timeloop_2020_ispass/timeloop+accelergy/ref-output/intmac/parsed-processed-input.yaml"
source "$ROOT/timeloop-env/bin/activate"
cd "$EVIDENCE"
{
  printf 'FRESH_OFFICIAL_EXAMPLE_TIMESTAMP_UTC=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'COMMAND=timeloop-mapper %s\n\n' "$EXAMPLE"
} > official_example_raw_output.txt
timeloop-mapper "$EXAMPLE" >> official_example_raw_output.txt 2>&1
mapper_status=$?
printf '\nOFFICIAL_EXAMPLE_EXIT_STATUS=%s\n' "$mapper_status" >> official_example_raw_output.txt
test "$mapper_status" -eq 0
```

The run was then required to have nonempty stats, map, ERT, ART, and Accelergy
log files; the raw output was required to contain the final summary and exit-0
marker; and the Accelergy log was scanned for failure/error markers.
