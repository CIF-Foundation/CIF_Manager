#!/usr/bin/env bash
# End-to-end build for the cif_lvcore_ipk LabVIEW RT package.
#
# Workflow:
#   1. Copy the checked-in IPK template into a staging directory
#   2. Overlay source files listed in cif_lvcore_ipk.build.json
#   3. Normalize text files to LF line endings for Linux/RT
#   4. Create the .ipk archive and move it to Installers/output/
#
# Usage:
#   bash Installers/build_cif_lvcore_ipk.sh
#
# On Windows, prefer Installers/build_cif_lvcore_ipk.bat which invokes this
# script through WSL.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/cif_lvcore_ipk.build.json"
APPLY_CONFIG="${SCRIPT_DIR}/apply_ipk_build_config.py"
BUILD_IPK="${SCRIPT_DIR}/build_ipk.sh"

if [[ ! -f "${CONFIG_FILE}" ]]; then
  echo "Error: Build config not found at ${CONFIG_FILE}" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required to apply ${CONFIG_FILE}" >&2
  exit 1
fi

# Read a top-level string value from the JSON build config.
read_config_value() {
  python3 - <<'PY' "${CONFIG_FILE}" "$1"
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    config = json.load(handle)

print(config[sys.argv[2]])
PY
}

IPK_TEMPLATE="${REPO_ROOT}/$(read_config_value ipk_template)"
STAGING_DIR="${REPO_ROOT}/$(read_config_value staging_directory)"
OUTPUT_DIR="${REPO_ROOT}/$(read_config_value output_directory)"

if [[ ! -d "${IPK_TEMPLATE}" ]]; then
  echo "Error: IPK template not found at ${IPK_TEMPLATE}" >&2
  exit 1
fi

# Stage a clean copy of the template so the source tree is never modified.
echo "Staging IPK template..."
rm -rf "$(dirname "${STAGING_DIR}")"
mkdir -p "${STAGING_DIR}"
cp -a "${IPK_TEMPLATE}/." "${STAGING_DIR}/"

# Copy canonical files from src/ into the staged package layout.
echo "Applying build config..."
python3 "${APPLY_CONFIG}" "${CONFIG_FILE}" "${REPO_ROOT}" "${STAGING_DIR}"

# Ensure shell scripts, Python, conf files, etc. use Linux line endings.
echo "Normalizing line endings to LF..."
python3 "${SCRIPT_DIR}/normalize_ipk_line_endings.py" "${STAGING_DIR}"

# Build the IPK from the staged tree.
echo "Building IPK..."
OUTPUT_PARENT="$(dirname "${STAGING_DIR}")"
IPK_PATH="$(
  bash "${BUILD_IPK}" "${STAGING_DIR}" "${OUTPUT_PARENT}"
)"

mkdir -p "${OUTPUT_DIR}"
FINAL_IPK="${OUTPUT_DIR}/$(basename "${IPK_PATH}")"
mv -f "${IPK_PATH}" "${FINAL_IPK}"

echo "Successfully created ${FINAL_IPK}"
