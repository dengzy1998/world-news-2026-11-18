"""Copy the pre-rendered front page to the grader output directory.

The image is drawn at authoring time and committed as entry.png; this
program only copies it byte-for-byte, using the Python standard library
alone so it runs in any minimal Python image.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)

    destination = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source, destination)


if __name__ == "__main__":
    main()
