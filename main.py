#!/usr/bin/env python3
"""Copy the pre-drawn news image to the grader output directory.

Deterministic: the same bytes are written on every run. No network,
no reading outside this repository.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "news-26-nov-2026.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    # Sanity check: the output must be byte-identical to the source.
    assert os.path.getsize(dst) == os.path.getsize(SRC)


if __name__ == "__main__":
    main()
