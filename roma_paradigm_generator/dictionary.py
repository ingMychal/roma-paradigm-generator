"""Look up words in the SRO dictionary (the XML export behind romskyslovnik.online).

The full dictionary is not owned by this project and is never committed. Put it at
``roma_paradigm_generator/data/SRO.xml`` to use it; otherwise the bundled sample
``SRO.sample.xml`` is used.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional, Union

DATA_DIR = Path(__file__).resolve().parent / "data"
FULL_DICTIONARY_PATH = DATA_DIR / "SRO.xml"
SAMPLE_DICTIONARY_PATH = DATA_DIR / "SRO.sample.xml"

# Parts of speech
NOUN = "noun"
VERB = "verb"
PLURAL = "plural"  # a lemma that only exists in the plural
OTHER = "other"

# Genders
MASCULINE = "masculine"
FEMININE = "feminine"

_DIACRITICS_TABLE = str.maketrans("čťľšžýáíéóúŕäôĺňď", "ctlszyaieouraolnd")


class DictionaryError(Exception):
    """The dictionary file is missing, unreadable, or has an entry we cannot use."""


@dataclass(frozen=True)
class WordEntry:
    """What the dictionary says about one Romani word."""

    word: str
    part_of_speech: str
    gender: str


def clean_text(text: str) -> str:
    """Lowercase and remove line breaks, tabs and surrounding whitespace."""
    for char in ("\n", "\t", "\r"):
        text = text.replace(char, "")
    return text.replace(" ", " ").lower().strip()


def strip_diacritics(word: str) -> str:
    """Replace Slovak/Romani letters with diacritics by their plain counterparts."""
    return word.translate(_DIACRITICS_TABLE)


def get_pos_category(pos_rom: str) -> str:
    """Map a dictionary part-of-speech label, e.g. '(sloveso)', to NOUN, VERB, PLURAL or OTHER."""
    if "množné" in pos_rom:
        return PLURAL
    if "sloveso" in pos_rom:
        return VERB
    if "podstatné meno" in pos_rom:
        return NOUN
    return OTHER


def get_gender_category(pos_rom: str) -> str:
    """Map a dictionary part-of-speech label to MASCULINE, FEMININE or OTHER."""
    if "ženský" in pos_rom:
        return FEMININE
    if "mužský" in pos_rom:
        return MASCULINE
    return OTHER


def default_dictionary_path() -> Path:
    """The full dictionary when it is present, else the bundled sample."""
    return FULL_DICTIONARY_PATH if FULL_DICTIONARY_PATH.exists() else SAMPLE_DICTIONARY_PATH


class Dictionary:
    """An in-memory index of the Romani lemmas in an SRO XML file.

    Lookups ignore case, surrounding whitespace and diacritics, so 'dzuvli'
    finds 'džuvľi'. When several senses share a lemma, the first one wins.
    """

    def __init__(self, senses: list[tuple[str, Optional[str]]]):
        # Maps the lookup key to (lemma, part-of-speech label). The label is None
        # when the dictionary entry has none.
        self._index: dict[str, tuple[str, Optional[str]]] = {}
        for lemma, pos_rom in senses:
            self._index.setdefault(strip_diacritics(lemma), (lemma, pos_rom))

    @classmethod
    def from_xml(cls, path: Union[str, Path]) -> "Dictionary":
        """Parse an SRO XML file."""
        try:
            root = ET.parse(path).getroot()
        except FileNotFoundError as exc:
            raise DictionaryError(f"Dictionary file not found at: {path}") from exc
        except (ET.ParseError, OSError) as exc:
            raise DictionaryError(f"Error reading dictionary file at {path}: {exc}") from exc

        senses = []
        for sense in root.iter("Sense"):
            lemma_element = sense.find("./Definition/lemmaROM")
            if lemma_element is None or not lemma_element.text:
                continue
            pos_element = sense.find("./posROM")
            pos_rom = pos_element.text if pos_element is not None else None
            senses.append((clean_text(lemma_element.text), None if pos_rom is None else clean_text(pos_rom)))
        return cls(senses)

    def __len__(self) -> int:
        return len(self._index)

    def lookup(self, search_term: str) -> Optional[WordEntry]:
        """Return the entry for ``search_term``, or None when the word is unknown.

        Raises DictionaryError when the word exists but has no part-of-speech label.
        """
        key = strip_diacritics(clean_text(search_term))
        if key not in self._index:
            return None
        lemma, pos_rom = self._index[key]
        if pos_rom is None:
            raise DictionaryError(f"No valid posROM element found for '{lemma}'.")
        return WordEntry(lemma, get_pos_category(pos_rom), get_gender_category(pos_rom))


@lru_cache(maxsize=None)
def load_dictionary(path: Optional[Union[str, Path]] = None) -> Dictionary:
    """Load and cache a dictionary; with no path, use ``default_dictionary_path()``."""
    return Dictionary.from_xml(path if path is not None else default_dictionary_path())
