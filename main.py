"""Entry point for the make.fun news-image competition.

Writes the front page for Wednesday 18 November 2026 to /output/entry.png.
The picture is generated deterministically by make_image.py: no network,
no random input, so repeated runs produce byte-identical output.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from make_image import build_image


def main():
    output_dir = "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.png")
    build_image(path)
    print("Wrote", path)


if __name__ == "__main__":
    main()
