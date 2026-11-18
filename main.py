#!/usr/bin/env python3
"""Entry program for news-image-20261118 (standard library only).

Copies the finished front-page image (entry.png, shipped beside this
script in the repository) to the harness output directory as
entry.png. The copy is byte-for-byte, so repeated runs always write
identical bytes.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
