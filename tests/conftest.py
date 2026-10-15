from pathlib import Path

import pytest

from roma_paradigm_generator.dictionary import Dictionary

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def test_dictionary() -> Dictionary:
    return Dictionary.from_xml(DATA_DIR / "test_dictionary.xml")
