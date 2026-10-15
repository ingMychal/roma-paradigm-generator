import pytest

from roma_paradigm_generator import dictionary
from roma_paradigm_generator.dictionary import (
    Dictionary,
    DictionaryError,
    WordEntry,
    clean_text,
    get_gender_category,
    get_pos_category,
    load_dictionary,
    strip_diacritics,
)


def test_clean_text_lowercases_and_removes_whitespace_characters():
    assert clean_text("  \t This iS a Te\tst String. \r \n") == "this is a test string."


def test_strip_diacritics():
    assert strip_diacritics("čťľšžýáíéóúŕäôĺňď") == "ctlszyaieouraolnd"


@pytest.mark.parametrize(
    "pos_rom, expected",
    [
        ("(sloveso, regionálny výraz)", "verb"),
        ("(podstatné meno, mužský rod, zdrobnenina)", "noun"),
        ("(podstatné meno, množné číslo)", "plural"),
        ("(prídavné meno, mužský rod)", "other"),
    ],
)
def test_get_pos_category(pos_rom, expected):
    assert get_pos_category(pos_rom) == expected


@pytest.mark.parametrize(
    "pos_rom, expected",
    [
        ("(podstatné meno, ženský rod)", "feminine"),
        ("(podstatné meno, mužský rod, zdrobnenina)", "masculine"),
        ("(príslovka)", "other"),
    ],
)
def test_get_gender_category(pos_rom, expected):
    assert get_gender_category(pos_rom) == expected


@pytest.mark.parametrize(
    "term, expected",
    [
        ("kher", WordEntry("kher", "noun", "masculine")),
        ("čambel", WordEntry("čambel", "verb", "other")),
        ("žila", WordEntry("žila", "noun", "feminine")),
        (
            "arminakeri zumin / jarminakeri zumin",
            WordEntry("arminakeri zumin / jarminakeri zumin", "other", "feminine"),
        ),
        ("grisoskeri zamiška", WordEntry("grisoskeri zamiška", "other", "other")),
        ("kalki", WordEntry("kalki", "plural", "other")),
    ],
)
def test_lookup_known_words(test_dictionary, term, expected):
    assert test_dictionary.lookup(term) == expected


@pytest.mark.parametrize("term", ["DŽUVĽI", "  džuvľi \n", "dzuvli"])
def test_lookup_ignores_case_whitespace_and_diacritics(test_dictionary, term):
    assert test_dictionary.lookup(term).word == "džuvľi"


def test_lookup_unknown_word_returns_none(test_dictionary):
    assert test_dictionary.lookup("nope") is None


def test_lookup_empty_term_matches_nothing(test_dictionary):
    # The fixture has a sense with an empty lemma; it must not match an empty search.
    assert test_dictionary.lookup("") is None


def test_first_sense_wins_when_lemma_repeats(test_dictionary):
    assert test_dictionary.lookup("kher").part_of_speech == "noun"


def test_lookup_word_without_part_of_speech_raises(test_dictionary):
    with pytest.raises(DictionaryError, match="bipos"):
        test_dictionary.lookup("bipos")


def test_missing_file_raises_dictionary_error(tmp_path):
    with pytest.raises(DictionaryError, match="not found"):
        Dictionary.from_xml(tmp_path / "missing.xml")


def test_malformed_file_raises_dictionary_error(tmp_path):
    broken = tmp_path / "broken.xml"
    broken.write_text("<root><Sense>", encoding="utf-8")
    with pytest.raises(DictionaryError, match="Error reading"):
        Dictionary.from_xml(broken)


def test_default_path_prefers_full_dictionary(tmp_path, monkeypatch):
    full = tmp_path / "SRO.xml"
    sample = tmp_path / "SRO.sample.xml"
    monkeypatch.setattr(dictionary, "FULL_DICTIONARY_PATH", full)
    monkeypatch.setattr(dictionary, "SAMPLE_DICTIONARY_PATH", sample)

    assert dictionary.default_dictionary_path() == sample
    full.write_text("<root/>", encoding="utf-8")
    assert dictionary.default_dictionary_path() == full


def test_bundled_sample_dictionary_loads():
    sample = load_dictionary(dictionary.SAMPLE_DICTIONARY_PATH)
    assert len(sample) > 0
    assert sample.lookup("phral") == WordEntry("phral", "noun", "masculine")
