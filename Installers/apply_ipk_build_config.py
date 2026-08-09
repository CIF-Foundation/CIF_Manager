#!/usr/bin/env python3
"""Apply cif_core_ipk.build.json copy mappings into a staged IPK tree.

Each copy entry maps one source file or directory from the repository into
the staged IPK package layout. Entries that contain only "_comment" are ignored.

Usage:
    apply_ipk_build_config.py <config.json> <repo_root> <ipk_root>
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


def load_config(config_path: Path) -> dict:
    """Load the JSON build configuration file."""
    with config_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def is_copy_entry(entry: dict) -> bool:
    """Return True when an entry defines a source/destination copy operation."""
    return "source" in entry and "destination" in entry


def apply_copies(repo_root: Path, ipk_root: Path, copies: list[dict]) -> None:
    """Copy each configured source file or directory into the staged IPK tree."""
    copy_index = 0
    for entry in copies:
        if not is_copy_entry(entry):
            continue

        copy_index += 1
        source = repo_root / entry["source"]
        destination = ipk_root / entry["destination"]

        if not source.exists():
            raise FileNotFoundError(
                f"Copy item {copy_index}: source not found: {entry['source']}"
            )

        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            # Directory copies replace the entire destination directory.
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

        print(f"Copied {entry['source']} -> {entry['destination']}")


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "Usage: apply_ipk_build_config.py <config.json> <repo_root> <ipk_root>",
            file=sys.stderr,
        )
        return 1

    config_path = Path(sys.argv[1]).resolve()
    repo_root = Path(sys.argv[2]).resolve()
    ipk_root = Path(sys.argv[3]).resolve()

    config = load_config(config_path)
    copies = config.get("copies")
    if not copies:
        raise ValueError(f"No copies defined in {config_path}")

    apply_copies(repo_root, ipk_root, copies)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
