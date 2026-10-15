import csv
from pathlib import Path

import pytest

from roma_paradigm_generator.nouns import (
    CASES,
    PLURAL,
    SINGULAR,
    format_noun_paradigms,
    format_noun_table,
    generate_noun_paradigms,
    generate_obliquus,
)

DATA_DIR = Path(__file__).parent / "data"
CASE_COLUMNS = ("nom", "gen", "dat", "aku", "voc", "lok", "abl", "ins")


def read_cases(file_name):
    with open(DATA_DIR / file_name, newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


@pytest.mark.parametrize("row", read_cases("obliquus_cases.csv"), ids=lambda row: row["word"])
def test_generate_obliquus(row):
    assert generate_obliquus(row["word"], row["gender"]) == (
        row["expected_obl_sg"],
        row["expected_obl_pl"],
        row["expected_gender"],
        row["expected_noun_type"],
    )


@pytest.mark.parametrize("row", read_cases("noun_paradigm_cases.csv"), ids=lambda row: row["word"])
def test_generate_noun_paradigms(row):
    expected = {
        SINGULAR: {case: row[f"{column}_sg"] for case, column in zip(CASES, CASE_COLUMNS)},
        PLURAL: {case: row[f"{column}_pl"] for case, column in zip(CASES, CASE_COLUMNS)},
    }
    assert generate_noun_paradigms(row["word"], row["gender"], row["animacy"]) == expected


def test_paradigms_list_cases_in_display_order():
    paradigms = generate_noun_paradigms("kher", "masculine", "neživotné")
    assert tuple(paradigms[SINGULAR]) == CASES
    assert tuple(paradigms[PLURAL]) == CASES


def test_word_ending_overrides_dictionary_gender():
    # -as marks a xenoclitic masculine whatever the dictionary says.
    assert generate_obliquus("sudcas", "feminine").gender == "masculine"


def test_unclassifiable_noun_keeps_the_word_as_stem():
    assert generate_obliquus("but", "other") == ("but", "but", "other", "other")


def test_lavutaris_has_nominative_plural_in_a():
    assert generate_noun_paradigms("lavutaris", "masculine", "životné")[PLURAL]["nominatív"] == "lavutara"


def test_animacy_changes_accusative_singular():
    assert generate_noun_paradigms("phral", "masculine", "životné")[SINGULAR]["akuzatív"] == "phrales"
    assert generate_noun_paradigms("phral", "masculine", "neživotné")[SINGULAR]["akuzatív"] == "phral"


def test_format_noun_paradigms():
    assert format_noun_paradigms({"nominatív": "kher", "genitív": "khereskero"}) == (
        "nominatív: kher\n\ngenitív: khereskero\n\n"
    )


def test_format_noun_table_shows_both_numbers():
    text = format_noun_table(generate_noun_paradigms("kher", "masculine", "neživotné"))
    assert text.startswith("Singulár:\n\nnominatív: kher\n\n")
    assert "\n\nPlurál:\n\nnominatív: khera\n\n" in text
