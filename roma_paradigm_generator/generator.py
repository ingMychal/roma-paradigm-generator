"""Turn a search term into the text the app shows: look it up, then decline or conjugate it.

This module has no user-interface code, so the GUI and the command line share it.
"""

from __future__ import annotations

from typing import Optional

from .dictionary import NOUN, PLURAL, VERB, Dictionary, DictionaryError, clean_text, load_dictionary
from .nouns import INANIMATE, format_noun_table, generate_noun_paradigms
from .verbs import process_verb


def generate_paradigm_text(
    search_term: str,
    animacy: str = INANIMATE,
    dictionary: Optional[Dictionary] = None,
) -> str:
    """Return the paradigm tables for ``search_term``, or a message saying why there are none.

    ``animacy`` only matters for nouns. With no ``dictionary``, the default one is loaded.
    """
    term = clean_text(search_term)
    if not term:
        return "Ma ruš! Please type a word first."

    try:
        entry = (dictionary if dictionary is not None else load_dictionary()).lookup(term)
    except DictionaryError as exc:
        return f"An error occurred: {exc}"

    if entry is None:
        return f"Ma ruš! We do not have '{term}' in our dictionary."
    if entry.part_of_speech == PLURAL:
        return "Ma ruš! No paradigms for plural forms available."
    if entry.part_of_speech == NOUN:
        return format_noun_table(generate_noun_paradigms(entry.word, entry.gender, animacy))
    if entry.part_of_speech == VERB:
        verb_tables = process_verb(entry.word)
        if verb_tables is not None:
            return verb_tables
    return f"Ma ruš! No paradigms for {entry.word} available."
