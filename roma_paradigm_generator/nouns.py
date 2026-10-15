"""Noun declension: build the singular and plural forms of all eight cases.

Romani nouns split into two declension types:

* oikoclitic ("oiko"): inherited words, e.g. kher, raklo, rakľi
* xenoclitic ("xeno"): later loanwords, e.g. sudcas, učiťeľka

Most case forms are the oblique stem plus a case suffix. The oblique stem is
built by ``generate_obliquus``; the nominative, accusative, vocative and
instrumental have their own rules.
"""

from __future__ import annotations

from typing import NamedTuple

from .dictionary import FEMININE, MASCULINE, OTHER
from .noun_exceptions import (
    MASCULINE_ENDING_IN_I,
    OIKOCLITIC_MASCULINE_LOOKALIKES,
    XENOCLITIC_NOMINATIVE_PLURAL_IN_A,
)

OIKOCLITIC = "oiko"
XENOCLITIC = "xeno"

ANIMATE = "životné"
INANIMATE = "neživotné"

SINGULAR = "Singulár"
PLURAL = "Plurál"

NOMINATIVE = "nominatív"
GENITIVE = "genitív"
DATIVE = "datív"
ACCUSATIVE = "akuzatív"
VOCATIVE = "vokatív"
LOCATIVE = "lokál"
ABLATIVE = "ablatív"
INSTRUMENTAL = "inštrumentál"

# (singular suffix, plural suffix) for the cases that are just stem + suffix.
OBLIQUE_CASE_SUFFIXES = {
    GENITIVE: ("kero", "gero"),
    DATIVE: ("ke", "ge"),
    LOCATIVE: ("te", "de"),
    ABLATIVE: ("tar", "dar"),
}

# Cases in display order.
CASES = (NOMINATIVE, GENITIVE, DATIVE, ACCUSATIVE, VOCATIVE, LOCATIVE, ABLATIVE, INSTRUMENTAL)


class Obliquus(NamedTuple):
    """The oblique stems of a noun and the declension class they imply."""

    singular: str
    plural: str
    gender: str
    noun_type: str


def generate_obliquus(word: str, gender: str) -> Obliquus:
    """Build the oblique stems of ``word`` and decide its gender and declension type.

    The word's ending overrides the dictionary gender where the ending is
    unambiguous; ``gender`` only decides words with a zero ending.
    """
    # Abstract nouns in -ben/-pen: uraviben -> uravibnas, uravibnen
    if word.endswith(("ben", "pen")):
        singular = word[:-2] + word[-1] + "as"
        return Obliquus(singular, singular[:-2] + "en", MASCULINE, OIKOCLITIC)

    # Xenoclitic masculine: sudcas -> sudcas, sudcen
    if word.endswith(("is", "as", "os", "us")) and word not in OIKOCLITIC_MASCULINE_LOOKALIKES:
        return Obliquus(word, word[:-2] + "en", MASCULINE, XENOCLITIC)

    # Xenoclitic feminine: učiťeľka -> učiťeľka, učiťeľken
    if word.endswith("a"):
        return Obliquus(word, word[:-1] + "en", FEMININE, XENOCLITIC)

    # Oikoclitic feminine in -i: rakľi -> rakľa, rakľen
    if word.endswith("i") and word not in MASCULINE_ENDING_IN_I:
        return Obliquus(word[:-1] + "a", word[:-1] + "en", FEMININE, OIKOCLITIC)

    # Oikoclitic masculine in -o (and the masculines in -i): raklo -> rakles, raklen
    if word.endswith("o") or word in MASCULINE_ENDING_IN_I:
        return Obliquus(word[:-1] + "es", word[:-1] + "en", MASCULINE, OIKOCLITIC)

    # Oikoclitic masculine with zero ending: kher -> kheres, kheren
    if gender == MASCULINE or word in OIKOCLITIC_MASCULINE_LOOKALIKES:
        return Obliquus(word + "es", word + "en", MASCULINE, OIKOCLITIC)

    # Oikoclitic feminine with zero ending: pheň -> pheňa, pheňen
    if gender == FEMININE:
        return Obliquus(word + "a", word + "en", FEMININE, OIKOCLITIC)

    return Obliquus(word, word, OTHER, OTHER)


def _oikoclitic_masculine_plural(word: str) -> str:
    """Nominative plural of an oikoclitic masculine: raklo -> rakle, voďi -> voďa, kher -> khera."""
    if word.endswith("o"):
        return word[:-1] + "e"
    if word in MASCULINE_ENDING_IN_I:
        return word[:-1] + "a"
    return word + "a"


def _nominative(word: str, obl: Obliquus) -> tuple[str, str]:
    if obl.noun_type == XENOCLITIC and obl.gender == MASCULINE:
        return word, word[:-2] + ("a" if word in XENOCLITIC_NOMINATIVE_PLURAL_IN_A else "i")
    if obl.noun_type == OIKOCLITIC and obl.gender == MASCULINE:
        return word, _oikoclitic_masculine_plural(word)
    if obl.noun_type == XENOCLITIC and obl.gender == FEMININE:
        return word, word[:-1] + "i"
    if obl.noun_type == OIKOCLITIC and obl.gender == FEMININE:
        return word, (word[:-1] if word.endswith("i") else word) + "a"
    return word, obl.plural


def _accusative(word: str, obl: Obliquus, animate: bool) -> tuple[str, str]:
    """Animate nouns take the oblique form; inanimate ones look like the nominative."""
    if obl.noun_type == XENOCLITIC:
        return word, obl.plural
    if obl.noun_type == OIKOCLITIC and obl.gender == MASCULINE:
        if animate:
            return obl.singular, obl.plural
        return word, _oikoclitic_masculine_plural(word)
    if obl.noun_type == OIKOCLITIC and obl.gender == FEMININE:
        return (obl.singular if animate else word), obl.plural
    return obl.singular + "a", obl.plural + "en"


def _vocative(word: str, obl: Obliquus, animate: bool) -> tuple[str, str]:
    if obl.noun_type == XENOCLITIC and obl.gender == MASCULINE:
        if animate:
            return word[:-2] + "ona", word[:-2] + "ale"
        return word, obl.plural
    if obl.noun_type == OIKOCLITIC and obl.gender == MASCULINE:
        if animate:
            stem = word[:-1] if word.endswith("o") else word
            return stem + "eja", stem + "ale"
        return word, _oikoclitic_masculine_plural(word)
    if obl.noun_type == XENOCLITIC and obl.gender == FEMININE:
        if animate:
            return word, word[:-1] + "i"
        return word, obl.plural
    if obl.noun_type == OIKOCLITIC and obl.gender == FEMININE:
        if not animate:
            return word, obl.plural
        stem = word[:-1] if word.endswith("i") else word
        return stem + "ije", stem + "ale"
    return obl.singular + "ije", obl.plural + "ale"


def _instrumental(word: str, obl: Obliquus) -> tuple[str, str]:
    plural = obl.plural + "ca"
    if obl.noun_type == XENOCLITIC and obl.gender == MASCULINE:
        return word[:-1] + "ha", plural
    if obl.noun_type == OIKOCLITIC and obl.gender == MASCULINE:
        return obl.singular[:-1] + "ha", plural
    return obl.singular + "ha", plural


def generate_noun_paradigms(word: str, gender: str, animacy: str) -> dict[str, dict[str, str]]:
    """Decline ``word``.

    ``gender`` is MASCULINE, FEMININE or OTHER (from the dictionary); ``animacy``
    is ANIMATE or INANIMATE. Returns ``{SINGULAR: {case: form}, PLURAL: {case: form}}``
    with the cases in display order.
    """
    obl = generate_obliquus(word, gender)
    animate = animacy == ANIMATE

    forms = {
        NOMINATIVE: _nominative(word, obl),
        ACCUSATIVE: _accusative(word, obl, animate),
        VOCATIVE: _vocative(word, obl, animate),
        INSTRUMENTAL: _instrumental(word, obl),
    }
    for case, (singular_suffix, plural_suffix) in OBLIQUE_CASE_SUFFIXES.items():
        forms[case] = (obl.singular + singular_suffix, obl.plural + plural_suffix)

    return {
        SINGULAR: {case: forms[case][0] for case in CASES},
        PLURAL: {case: forms[case][1] for case in CASES},
    }


def format_noun_paradigms(forms: dict[str, str]) -> str:
    """Render one number's forms as 'case: form' lines separated by blank lines."""
    return "".join(f"{case}: {form}\n\n" for case, form in forms.items())


def format_noun_table(paradigms: dict[str, dict[str, str]]) -> str:
    """Render both numbers of a declension, as shown in the app."""
    return (
        f"{SINGULAR}:\n\n"
        + format_noun_paradigms(paradigms[SINGULAR])
        + f"\n\n{PLURAL}:\n\n"
        + format_noun_paradigms(paradigms[PLURAL])
    )
