"""Entrypoint for the News Image 22 Nov entry: publish the artwork."""

import os
import shutil
import sys
from pathlib import Path


def main() -> None:
    # The artwork sits beside this script, wherever it was unpacked.
    artwork = Path(__file__).resolve().parent / "entry.png"
    if not artwork.is_file():
        # A missing source means an incomplete bundle, so fail loudly
        # instead of leaving an empty output folder behind.
        print(f"error: bundled artwork not found at {artwork}", file=sys.stderr)
        raise SystemExit(1)
    # The grader may redirect the output folder through the env var.
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    # copyfile moves raw bytes only, so the image arrives unchanged.
    shutil.copyfile(artwork, out_dir / "entry.png")


if __name__ == "__main__":
    main()
