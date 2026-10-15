import pytest

from roma_paradigm_generator.verbs import (
    UNKNOWN_PERFECT_ROOT,
    conjugate,
    define_perf_root,
    define_pres_root,
    determine_conjugation_class,
    find_verb,
    format_verb_paradigms,
    generate_verb_paradigms,
    is_valid_verb,
    process_verb,
)


@pytest.mark.parametrize("verb, expected", [("bašal", 1), ("kerel", 2), ("pašľol", 3), ("lel", 2), ("darav", 3)])
def test_determine_conjugation_class(verb, expected):
    assert determine_conjugation_class(verb) == expected


@pytest.mark.parametrize(
    "verb, pres_root, perf_root",
    [
        ("bašal", "baša", "bašanď"),
        ("kerel", "ker", "kerď"),
        ("dikhel", "dikh", "dikhľ"),
        ("rodel", "rod", "rodň"),
        ("bešel", "beš", "bešť"),
        ("ušťel", "ušť", "ušťiľ"),
        ("pašľol", "pašľ", "pašľiľ"),
    ],
)
def test_roots(verb, pres_root, perf_root):
    conjugation_class = determine_conjugation_class(verb)
    assert define_pres_root(verb, conjugation_class) == pres_root
    assert define_perf_root(pres_root, conjugation_class) == perf_root


def test_unknown_perfect_root_is_marked():
    assert define_perf_root("pat", 2) == UNKNOWN_PERFECT_ROOT


@pytest.mark.parametrize(
    "verb, tense, person, number, expected",
    [
        ("kerel", "pres", 1, "sg", "kerav"),
        ("kerel", "pres", 3, "pl", "keren"),
        ("kerel", "fut", 2, "sg", "kereha"),
        ("kerel", "impf", 1, "pl", "kerahas"),
        ("kerel", "perf", 1, "sg", "kerďom"),
        ("kerel", "perf", 3, "pl", "kerde"),
        ("kerel", "cond_pres", 1, "sg", "keravas"),
        ("kerel", "cond_perf", 1, "sg", "kerďomas"),
        ("kerel", "cond_perf", 3, "sg", "kerďahas"),
        ("kerel", "cond_perf", 3, "pl", "kerdehas"),
        ("bašal", "pres", 1, "sg", "bašav"),
        ("bašal", "pres", 3, "sg", "bašal"),
        ("bašal", "cond_pres", 3, "pl", "bašanas"),
        ("bašal", "perf", 3, "pl", "bašande"),
        ("pašľol", "pres", 1, "sg", "pašľuvav"),
        ("pašľol", "perf", 1, "sg", "pašľiľom"),
        ("pašľol", "perf", 3, "pl", "pašľile"),
    ],
)
def test_conjugated_forms(verb, tense, person, number, expected):
    assert generate_verb_paradigms(verb)[tense][person][number] == expected


@pytest.mark.parametrize(
    "verb, singular, plural",
    [
        ("bašal", "baša!", "bašan!"),
        ("kerel", "ker!", "keren!"),
        ("sikhadel", "sikhade!", "sikhaden!"),
        ("urel", "uri!", "uren!"),
        ("pašľol", "pašľuv!", "pašľon!"),
    ],
)
def test_imperative(verb, singular, plural):
    assert generate_verb_paradigms(verb)["imper"] == {2: {"sg": singular, "pl": plural}}


def test_every_tense_has_all_persons_and_numbers():
    paradigms = generate_verb_paradigms("kerel")
    assert list(paradigms) == ["pres", "fut", "impf", "perf", "cond_pres", "cond_perf", "imper"]
    for tense, persons in paradigms.items():
        expected_persons = [2] if tense == "imper" else [1, 2, 3]
        assert list(persons) == expected_persons
        for numbers in persons.values():
            assert list(numbers) == ["sg", "pl"]


@pytest.mark.parametrize("text, expected", [("kerel", True), ("kerel buťi", False), ("dikhel pes", False), ("pes dikhel", False)])
def test_is_valid_verb_means_single_word(text, expected):
    assert is_valid_verb(text) is expected


@pytest.mark.parametrize("text, expected", [("kerel buťi", "kerel"), ("(dikhel) pes", "dikhel"), ("bari buťi", None)])
def test_find_verb(text, expected):
    assert find_verb(text) == expected


def test_phrase_keeps_other_words():
    paradigms = conjugate("kerel buťi")
    assert paradigms["pres"][1]["sg"] == "kerav buťi"
    assert paradigms["imper"][2]["sg"] == "ker buťi!"


@pytest.mark.parametrize(
    "text, first_singular, third_plural, imperative_plural",
    [
        ("dikhel pes", "dikhav man", "dikhen pen", "dikhen tumen!"),
        ("pes dikhel", "man dikhav", "pen dikhen", "tumen dikhen!"),
    ],
)
def test_reflexive_pes_follows_person(text, first_singular, third_plural, imperative_plural):
    paradigms = conjugate(text)
    assert paradigms["pres"][1]["sg"] == first_singular
    assert paradigms["pres"][3]["pl"] == third_plural
    assert paradigms["imper"][2]["pl"] == imperative_plural


def test_pes_inside_another_word_is_not_replaced():
    assert conjugate("kerel pesko")["pres"][1]["sg"] == "kerav pesko"


def test_text_without_verb():
    assert conjugate("bari buťi") is None
    assert process_verb("bari buťi") is None


def test_format_verb_paradigms_aligns_columns():
    text = format_verb_paradigms(generate_verb_paradigms("kerel"))
    assert text.startswith("Presentum\n")
    assert "Imperativus\n" in text
    present_rows = text.split("\n\n")[0].splitlines()[2:]
    assert [row.index("\t") for row in present_rows] == [present_rows[0].index("\t")] * 3


def test_phrase_ending_in_verb_conjugates_the_last_word():
    # 'bal' also ends in -l, but the verb is the last word.
    paradigms = conjugate("bal kerel")
    assert paradigms["pres"][1]["sg"] == "bal kerav"
    assert paradigms["imper"][2]["sg"] == "bal ker!"
    assert find_verb("bal kerel") == "kerel"


def test_only_the_verb_itself_is_replaced():
    assert conjugate("kerel kerel")["pres"][1]["sg"] == "kerel kerav"
