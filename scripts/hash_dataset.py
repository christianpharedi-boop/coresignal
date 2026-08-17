#!/usr/bin/env python3
"""Compute a SHA-256 hash and byte size for an acquired dataset."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_file():
        raise SystemExit(f"ERROR: file not found: {path}")

    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)

    print(f"file: {path}")
    print(f"sha256: {digest.hexdigest()}")
    print(f"byte_size: {size}")

if __name__ == "__main__":
    main()
