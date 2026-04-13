"""
This script automates the process of building the executable for the Roma Paradigm Generator.

Functions:
- run_tests(): Run tests using pytest. Aborts the executable build if tests fail.
- build_executable(): Build the executable using PyInstaller after running tests.

Usage:
Run this script directly to build the executable:
    $ python build_script.py
"""

import os
import sys
import subprocess


def run_tests():
    """Run tests using pytest. Aborts the executable build if tests fail."""
    result = subprocess.run(
        ['pytest', 'test_generator.py'],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print("Tests failed. Aborting executable build.")
        print(result.stdout)
        sys.exit(1)


def build_executable():
    """Build the executable using PyInstaller after running tests."""
    run_tests()

    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_directory)

    data_path = os.path.join(script_directory, "data", "SRO.xml")

    result = subprocess.run(
        [
            'pyinstaller',
            '--onefile',
            '--add-data', f'{data_path}{os.pathsep}data',
            'user_interface.py',
        ],
        check=False,
    )

    if result.returncode != 0:
        print("PyInstaller build failed.")
        sys.exit(1)

    print("Build successful. Executable is in the dist/ directory.")


if __name__ == "__main__":
    build_executable()
