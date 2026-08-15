#!/usr/bin/env bash
set -euo pipefail

tool_dir="${1:-/tmp/timeloop_spice_toolchain}"
mkdir -p "$tool_dir/root"

ngspice_url='https://archive.ubuntu.com/ubuntu/pool/universe/n/ngspice/ngspice_42+ds-3build1_amd64.deb'
ngspice_sha='466c4c06418107ceaa9c9457065b3bb71a9d9dc5ec6fef186d7de9d5208ce8db'
libxft_url='https://archive.ubuntu.com/ubuntu/pool/main/x/xft/libxft2_2.3.6-1build1_amd64.deb'
libxft_sha='b4f4f3255c0b8773b260c61cbe20ee7c63799cfc0e4e389fa58375dd480b093a'

fetch_verified() {
  local url="$1" output="$2" expected="$3"
  if [[ ! -f "$output" ]] || [[ "$(sha256sum "$output" | awk '{print $1}')" != "$expected" ]]; then
    curl -L --fail --retry 2 --max-time 120 -o "$output" "$url"
  fi
  printf '%s  %s\n' "$expected" "$output" | sha256sum -c -
}

fetch_verified "$ngspice_url" "$tool_dir/ngspice.deb" "$ngspice_sha"
fetch_verified "$libxft_url" "$tool_dir/libxft2.deb" "$libxft_sha"
dpkg-deb -x "$tool_dir/ngspice.deb" "$tool_dir/root"
dpkg-deb -x "$tool_dir/libxft2.deb" "$tool_dir/root"
LD_LIBRARY_PATH="$tool_dir/root/usr/lib/x86_64-linux-gnu" "$tool_dir/root/usr/bin/ngspice" --version
