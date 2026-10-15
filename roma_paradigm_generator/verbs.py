"""Verb conjugation: build the forms of all tenses for a verb or a verb phrase.

Verbs are entered in the 3rd person singular present (the dictionary form),
e.g. kerel, bašal, pašľol. The ending -al / -el / -ol decides the conjugation
class (1 / 2 / 3).

A phrase that contains such a verb, e.g. 'dikhel pes' or 'kerel buťi', is
conjugated by replacing the verb in it; a reflexive 'pes' is replaced by the
matching pronoun (man, tut, pes, amen, tumen, pen).
"""

from __future__ import annotations

import re
from typing import Optional

from .dictionary import strip_diacritics
from .verb_endings import ENDINGS, TENSE_NAMES

TENSES = ("pres", "fut", "impf", "perf", "cond_pres", "cond_perf")
PERSONS = (1, 2, 3)
NUMBERS = ("sg", "pl")
IMPERATIVE = "imper"

# Shown instead of a perfect stem when no rule covers the verb.
UNKNOWN_PERFECT_ROOT = "xxx"

# Class 2 verbs whose imperative singular ends in -i.
IMPERATIVE_SINGULAR_IN_I = frozenset({"chuťel", "ušťel", "urel"})

REFLEXIVE_PRONOUNS = {
    1: {"sg": "man", "pl": "amen"},
    2: {"sg": "tut", "pl": "tumen"},
    3: {"sg": "pes", "pl": "pen"},
}

_VERB_PATTERN = re.compile(r"\b\w+l\b")
_PES_PATTERN = re.compile(r"\bpes\b")

# {tense: {person: {number: form}}}
Paradigms = dict[str, dict[int, dict[str, str]]]


def is_valid_verb(text: str) -> bool:
    """True when ``text`` is a single word ending in -l."""
    return bool(re.fullmatch(r"\S+l", text))


def _find_verb_match(text: str) -> Optional[re.Match]:
    """The verb of a phrase: its last word when that ends in -l, else its first word ending in -l."""
    matches = list(_VERB_PATTERN.finditer(text))
    if not matches:
        return None
    if matches[-1].end() == len(text.rstrip()):
        return matches[-1]
    return matches[0]


def find_verb(text: str) -> Optional[str]:
    """The word of ``text`` that is conjugated (see ``_find_verb_match``), or None."""
    match = _find_verb_match(text)
    return match.group() if match else None


def contains_valid_verb(text: str) -> bool:
    """True when some word in ``text`` ends in -l."""
    return find_verb(text) is not None


def determine_conjugation_class(verb: str) -> int:
    """1 for -al, 2 for -el, 3 for -ol and anything else."""
    for ending, conjugation_class in (("al", 1), ("el", 2), ("ol", 3)):
        if verb.endswith(ending):
            return conjugation_class
    return 3


def define_pres_root(verb: str, conjugation_class: int) -> str:
    """Present stem: bašal -> baša, kerel -> ker, pašľol -> pašľ."""
    return verb[:-1] if conjugation_class == 1 else verb[:-2]


def define_perf_root(pres_root: str, conjugation_class: int) -> str:
    """Perfect stem: baša -> bašanď, ker -> kerď, dikh -> dikhľ, pašľ -> pašľiľ."""
    if conjugation_class == 1:
        return pres_root + "nď"
    if conjugation_class == 2:
        last = pres_root[-1:]
        if last and last in "lnrv":
            return pres_root + "ď"
        if last and last in "čgjkhm":
            return pres_root + "ľ"
        if last == "d":
            return pres_root + "ň"
        if last and last in "sš":
            return pres_root + "ť"
        if last == "ť":
            return pres_root + "iľ"
        return UNKNOWN_PERFECT_ROOT
    return pres_root + "iľ"


def is_conditional(tense: str) -> bool:
    return tense.startswith("cond_")


def _ending(conjugation_class: int, tense: str, person: int, number: str) -> str:
    endings = ENDINGS[conjugation_class]
    if tense == "cond_pres":
        # The present conditional has the same form as the imperfect.
        return endings["impf"][person][number]
    if tense == "cond_perf":
        # The past conditional is the perfect plus -as (-has in the 3rd person).
        ending = endings["perf"][person][number]
        if person == 3:
            return ending[:-1] + "has" if number == "sg" else ending + "has"
        return ending + "as"
    return endings[tense][person][number]


def _imperative_ending(verb: str, conjugation_class: int, number: str) -> str:
    if number == "pl":
        return {1: "n!", 2: "en!"}.get(conjugation_class, "on!")
    if conjugation_class == 3:
        return "uv!"
    if conjugation_class == 2:
        if verb.endswith("del"):
            return "e!"
        if verb in IMPERATIVE_SINGULAR_IN_I:
            return "i!"
    return "!"


def generate_verb_paradigms(verb: str) -> Paradigms:
    """Conjugate a single verb in all tenses, plus the imperative (2nd person only)."""
    conjugation_class = determine_conjugation_class(verb)
    pres_root = define_pres_root(verb, conjugation_class)
    perf_root = define_perf_root(pres_root, conjugation_class)
    # Class 1 drops the stem's final -a before the present-type endings, which start with -a.
    present_type_root = pres_root[:-1] if conjugation_class == 1 else pres_root

    paradigms: Paradigms = {}
    for tense in TENSES:
        paradigms[tense] = {}
        for person in PERSONS:
            paradigms[tense][person] = {}
            for number in NUMBERS:
                if tense in ("perf", "cond_perf"):
                    root = perf_root
                    if person == 3 and number == "pl":
                        # Before the 3rd person plural -e the stem drops its softening mark: kerďom, but kerde.
                        root = perf_root[:-1] + strip_diacritics(perf_root[-1:])
                else:
                    root = present_type_root
                paradigms[tense][person][number] = root + _ending(conjugation_class, tense, person, number)

    paradigms[IMPERATIVE] = {
        2: {number: pres_root + _imperative_ending(verb, conjugation_class, number) for number in NUMBERS}
    }
    return paradigms


def format_verb_paradigms(paradigms: Paradigms) -> str:
    """Render the paradigms as one aligned singular/plural table per tense."""
    singular_width = max(len(forms.get("sg", "")) for tense in paradigms.values() for forms in tense.values())
    output = ""
    for tense, persons in paradigms.items():
        plural_width = max(len(forms.get("pl", "")) for forms in persons.values())
        output += f"{TENSE_NAMES.get(tense, tense)}\n"
        output += "    Singulár".ljust(singular_width + 6) + "Plurál\n"
        for person, forms in persons.items():
            singular = forms.get("sg", "").ljust(singular_width)
            plural = forms.get("pl", "").ljust(plural_width)
            output += f"{f'{person}.'.ljust(3)} {singular} \t{plural}\n"
        output += "\n"
    return output


def contains_standalone_pes(text: str) -> bool:
    return bool(_PES_PATTERN.search(text))


def replace_pes_forms(paradigms: Paradigms) -> Paradigms:
    """Replace the reflexive 'pes' in every form by the pronoun of that person and number."""
    return {
        tense: {
            person: {
                number: _PES_PATTERN.sub(REFLEXIVE_PRONOUNS[person][number], phrase)
                for number, phrase in numbers.items()
            }
            for person, numbers in persons.items()
        }
        for tense, persons in paradigms.items()
    }


def replace_neutral_with_forms(text: str, verb_span: tuple[int, int], paradigms: Paradigms) -> Paradigms:
    """Put each conjugated form into the phrase ``text`` at ``verb_span`` (start, end).

    The imperative's '!' moves to the end of the phrase: 'kerel buťi' -> 'ker buťi!'.
    """
    start, end = verb_span
    before, after = text[:start], text[end:]
    phrases: Paradigms = {}
    for tense, persons in paradigms.items():
        phrases[tense] = {}
        for person, numbers in persons.items():
            phrases[tense][person] = {}
            for number, form in numbers.items():
                if tense == IMPERATIVE:
                    phrase = before + form[:-1] + after + "!"
                else:
                    phrase = before + form + after
                phrases[tense][person][number] = phrase
    return phrases


def conjugate(text: str) -> Optional[Paradigms]:
    """Conjugate a verb or a phrase containing one; None when ``text`` has no verb."""
    text = text.strip()
    if is_valid_verb(text):
        return generate_verb_paradigms(text)
    match = _find_verb_match(text)
    if match is None:
        return None
    paradigms = replace_neutral_with_forms(text, match.span(), generate_verb_paradigms(match.group()))
    if contains_standalone_pes(text):
        paradigms = replace_pes_forms(paradigms)
    return paradigms


def process_verb(text: str) -> Optional[str]:
    """Conjugate ``text`` and render it as tables; None when ``text`` has no verb."""
    paradigms = conjugate(text)
    return format_verb_paradigms(paradigms) if paradigms is not None else None
