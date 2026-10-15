"""Regression test: today's output for many nouns and verbs must not change by accident.

The expected values were produced by the code itself, so they protect against
unintended changes; they are not a linguistic reference. When you change a rule
on purpose, regenerate the file and review the diff:

    python -m tests.test_golden
"""

import json
from pathlib import Path

import pytest

from roma_paradigm_generator.nouns import ANIMATE, INANIMATE, generate_noun_paradigms
from roma_paradigm_generator.verbs import conjugate

GOLDEN_FILE = Path(__file__).parent / "data" / "golden_paradigms.json"

NOUNS = (
    "mas kher sudcas trapišagos uraviben raklo voďi paňi učiťeľka rakľi pheň phral khosno piri "
    "khoskerdo lavutaris papus bašavno pharipen problemos kamiben kamňipen džuvľi manušňi džeňi "
    "sikhľarďi čhavo čhaj dad daj balval kham foros rom romňi gadžo čiriklo šero jakh vast"
).split()
GENDERS = ("masculine", "feminine", "other")
VERBS = (
    "dikhel", "kerel", "phenel", "kamel", "bašal", "asal", "pašľol", "čambel", "chuťel", "ušťel",
    "urel", "sikhadel", "bešel", "lel", "pačal", "ladžal pes", "ťidel", "bisterel", "mukel",
    "dživel", "rodel", "pijel", "sovel", "avel", "ačhol", "rovel", "darav", "dikhel pes",
    "pes dikhel", "kerel buťi", "pratel", "bal kerel", "lil ginel", "kerel lačho buťi",
)


def build_golden():
    nouns = {
        f"{word}|{gender}|{animacy}": generate_noun_paradigms(word, gender, animacy)
        for word in NOUNS
        for gender in GENDERS
        for animacy in (ANIMATE, INANIMATE)
    }
    verbs = {verb: conjugate(verb) for verb in VERBS}
    # JSON keys are strings, so convert the person numbers before comparing.
    return json.loads(json.dumps({"nouns": nouns, "verbs": verbs}, ensure_ascii=False))


@pytest.fixture(scope="module")
def golden():
    return json.loads(GOLDEN_FILE.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def current():
    return build_golden()


@pytest.mark.parametrize("section", ["nouns", "verbs"])
def test_matches_golden_file(golden, current, section):
    assert current[section].keys() == golden[section].keys()
    changed = [key for key in golden[section] if current[section][key] != golden[section][key]]
    assert not changed, f"Output changed for: {', '.join(changed)}"


if __name__ == "__main__":
    GOLDEN_FILE.write_text(json.dumps(build_golden(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Wrote {GOLDEN_FILE}")
