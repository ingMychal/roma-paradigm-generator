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
    '''Run tests using pytest. Aborts the executable build if tests fail.'''
    result = subprocess.run(
    ['pytest', 'test_generator.py'],
    capture_output=True,
    text=True,
    check=False
)
    # Check if any tests failed
    if result.returncode != 0:
        print("Tests failed. Aborting executable build.")
        print(result.stdout)
        sys.exit(1)

def build_executable():
    '''Build the executable using PyInstaller after running tests.'''
    run_tests()

    # Get the path to the directory containing this script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Set the working directory to the script's location
    os.chdir(script_directory)

    # Construct the path to the data file relative to the script's location
    data_path = os.path.join(script_directory, "data", "SRO.xml")

    # Construct the PyInstaller command
    pyinstaller_command = (
        f'pyinstaller --onefile --add-data "{data_path}{os.pathsep}data" user_interface.py'
    )

    # Run the PyInstaller command
    os.system(pyinstaller_command)

if __name__ == "__main__":
    build_executable()
