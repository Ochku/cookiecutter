#!/usr/bin/env python3
"""Generate conda-lock files for reproducible environments."""

import subprocess  # nosec B404
import sys


def generate_lock_file():
    """Generate conda-lock files for all platforms."""
    try:
        subprocess.run(
            [
                "conda-lock",
                "lock",
                "--platform",
                "win-64",
                "--file",
                "environment.yml",
            ],
            check=True,
        )  # nosec B603 B607

        print("Successfully generated conda-lock.yml")

        # Create platform-specific lock files
        subprocess.run(
            ["conda-lock", "render", "-k", "env", "conda-lock.yml"], check=True
        )  # nosec B603 B607

        print("Successfully generated platform-specific lock files")

    except subprocess.CalledProcessError as e:
        print(f"Error generating lock files: {e}")
        sys.exit(1)


if __name__ == "__main__":
    generate_lock_file()
