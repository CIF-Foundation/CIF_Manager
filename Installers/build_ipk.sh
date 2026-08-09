#!/usr/bin/env bash
# Create a cif-lvcore .ipk archive from a staged IPK directory.
#
# An IPK is an ar archive containing:
#   debian-binary
#   control.tar.gz  (metadata and install scripts)
#   data.tar.gz     (files to install on the target)
#
# Usage:
#   bash build_ipk.sh <ipk_directory> [output_directory]
#
# The final IPK path is printed to stdout. Status messages go to stderr so
# callers can safely capture only the output filename.
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <ipk_directory> [output_directory]" >&2
  exit 1
fi

IPK_DIR="$(cd "$1" && pwd)"
OUTPUT_DIR="${2:-$(dirname "${IPK_DIR}")}"

if [[ ! -f "${IPK_DIR}/control/control" ]]; then
  echo "Error: control file not found at ${IPK_DIR}/control/control" >&2
  exit 1
fi

# Package version comes from the opkg/ipk control file.
PKG_VERSION="$(grep "^Version:" "${IPK_DIR}/control/control" | cut -d' ' -f2)"
if [[ -z "${PKG_VERSION}" ]]; then
  echo "Error: Could not find version in ${IPK_DIR}/control/control" >&2
  exit 1
fi

pushd "${IPK_DIR}" >/dev/null

# Use numeric owner/group 0 so files extract consistently on RT targets.
tar --numeric-owner --group=0 --owner=0 -czf data.tar.gz -C data .
tar --numeric-owner --group=0 --owner=0 -czf control.tar.gz -C control .

IPK_FILENAME="${OUTPUT_DIR}/cif-lvcore.${PKG_VERSION}.ipk"
tar --numeric-owner --group=0 --owner=0 -cf "${IPK_FILENAME}" ./debian-binary ./data.tar.gz ./control.tar.gz

rm -f data.tar.gz control.tar.gz
popd >/dev/null

echo "Successfully created ${IPK_FILENAME}" >&2
printf '%s\n' "${IPK_FILENAME}"
