import pytest

from roma_paradigm_generator.dictionary import Dictionary
from roma_paradigm_generator.generator import generate_paradigm_text
from roma_paradigm_generator.nouns import ANIMATE, INANIMATE


def test_noun_shows_declension(test_dictionary):
    text = generate_paradigm_text("kher", INANIMATE, test_dictionary)
    assert text.startswith("Singulár:\n\nnominatív: kher\n\n")


def test_animacy_is_passed_to_nouns(test_dictionary):
    animate = generate_paradigm_text("džuvľi", ANIMATE, test_dictionary)
    inanimate = generate_paradigm_text("džuvľi", INANIMATE, test_dictionary)
    assert "akuzatív: džuvľa" in animate
    assert "akuzatív: džuvľi" in inanimate


def test_verb_shows_conjugation(test_dictionary):
    text = generate_paradigm_text("čambel", INANIMATE, test_dictionary)
    assert text.startswith("Presentum\n")
    assert "čambav" in text


def test_reflexive_verb_phrase(test_dictionary):
    assert "dikhav man" in generate_paradigm_text("dikhel pes", INANIMATE, test_dictionary)


@pytest.mark.parametrize(
    "term, message",
    [
        ("", "Ma ruš! Please type a word first."),
        ("   ", "Ma ruš! Please type a word first."),
        ("Nope", "Ma ruš! We do not have 'nope' in our dictionary."),
        ("word", "Ma ruš! We do not have 'word' in our dictionary."),
        ("kalki", "Ma ruš! No paradigms for plural forms available."),
        ("grisoskeri zamiška", "Ma ruš! No paradigms for grisoskeri zamiška available."),
        ("bisloveso", "Ma ruš! No paradigms for bisloveso available."),
        ("bipos", "An error occurred: No valid posROM element found for 'bipos'."),
    ],
)
def test_messages(test_dictionary, term, message):
    assert generate_paradigm_text(term, INANIMATE, test_dictionary) == message


def test_uses_default_dictionary_when_none_given():
    assert generate_paradigm_text("phral").startswith("Singulár:")


def test_empty_dictionary():
    assert "do not have" in generate_paradigm_text("phral", INANIMATE, Dictionary([]))
