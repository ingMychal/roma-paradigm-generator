"""Build a standalone executable of the Roma Paradigm Generator with PyInstaller.

    python build_script.py

The tests run first; the build stops if any test fails. The executable bundles
the full dictionary (roma_paradigm_generator/data/SRO.xml) when it is present,
otherwise the sample. It lands in dist/ and only runs on the operating system
it was built on.
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from roma_paradigm_generator.dictionary import default_dictionary_path  # noqa: E402

APP_NAME = "RomaParadigmGenerator"
ENTRY_SCRIPT = ROOT / "roma_paradigm_generator" / "__main__.py"


def run(command):
    """Run a command from the repository root; exit with its code if it fails."""
    print("$", " ".join(str(part) for part in command), flush=True)
    result = subprocess.run(command, cwd=ROOT, check=False)
    if result.returncode != 0:
        sys.exit(result.returncode)


def run_tests():
    print("Running tests...")
    run([sys.executable, "-m", "pytest", "-q"])


def build_executable():
    run_tests()

    dictionary_file = default_dictionary_path()
    print(f"Bundling dictionary: {dictionary_file.relative_to(ROOT)}")

    run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--clean",
            "--onefile",
            "--name",
            APP_NAME,
            "--paths",
            str(ROOT),
            # Keep the file name, so the app finds it where it expects it.
            "--add-data",
            f"{dictionary_file}{os.pathsep}roma_paradigm_generator/data",
            str(ENTRY_SCRIPT),
        ]
    )
    executable = ROOT / "dist" / (APP_NAME + (".exe" if os.name == "nt" else ""))
    print(f"Built {executable}")


if __name__ == "__main__":
    build_executable()
