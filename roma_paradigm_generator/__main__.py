"""Run with ``python -m roma_paradigm_generator``.

Absolute import, so PyInstaller can also use this file as the entry script.
"""

import sys

from roma_paradigm_generator.cli import main

if __name__ == "__main__":
    sys.exit(main())
