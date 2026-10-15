"""Command-line entry point.

    python -m roma_paradigm_generator                 open the window
    python -m roma_paradigm_generator phral --animate  print the paradigms of 'phral'
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from . import __version__
from .dictionary import DictionaryError, load_dictionary
from .generator import generate_paradigm_text
from .nouns import ANIMATE, INANIMATE


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="roma-paradigm-generator",
        description="Generate East Slovak Romani noun and verb paradigms. "
        "Without a word, open the graphical interface.",
    )
    parser.add_argument("word", nargs="*", help="the word to look up, e.g. phral or 'dikhel pes'")
    parser.add_argument("--animate", action="store_true", help="decline a noun as animate (default: inanimate)")
    parser.add_argument("--dictionary", type=Path, help="path to an SRO XML file (default: the bundled one)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        dictionary = load_dictionary(args.dictionary)
    except DictionaryError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if not args.word:
        from .gui import run  # Imported here so the CLI works where Tk is not installed.

        run(dictionary)
        return 0

    # Romani letters (č, ľ, ň ...) must print on consoles whose default encoding lacks them.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(generate_paradigm_text(" ".join(args.word), ANIMATE if args.animate else INANIMATE, dictionary))
    return 0
