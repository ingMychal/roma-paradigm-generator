import pytest

from roma_paradigm_generator import cli, gui
from roma_paradigm_generator.__main__ import main as module_main

from .conftest import DATA_DIR

TEST_DICTIONARY = str(DATA_DIR / "test_dictionary.xml")


def test_prints_paradigms(capsys):
    assert cli.main(["kher", "--dictionary", TEST_DICTIONARY]) == 0
    assert capsys.readouterr().out.startswith("Singulár:\n\nnominatív: kher")


def test_joins_several_words_into_one_term(capsys):
    assert cli.main(["dikhel", "pes", "--dictionary", TEST_DICTIONARY]) == 0
    assert "dikhav man" in capsys.readouterr().out


def test_animate_flag(capsys):
    cli.main(["džuvľi", "--animate", "--dictionary", TEST_DICTIONARY])
    assert "akuzatív: džuvľa" in capsys.readouterr().out


def test_unknown_word_still_exits_zero(capsys):
    assert cli.main(["nope", "--dictionary", TEST_DICTIONARY]) == 0
    assert "do not have 'nope'" in capsys.readouterr().out


def test_missing_dictionary_exits_with_error(tmp_path, capsys):
    assert cli.main(["kher", "--dictionary", str(tmp_path / "missing.xml")]) == 2
    assert "not found" in capsys.readouterr().err


def test_without_word_opens_gui(monkeypatch):
    opened = []
    monkeypatch.setattr(gui, "run", opened.append)
    assert cli.main(["--dictionary", TEST_DICTIONARY]) == 0
    assert len(opened) == 1


def test_version(capsys):
    with pytest.raises(SystemExit) as exit_info:
        cli.main(["--version"])
    assert exit_info.value.code == 0
    assert "roma-paradigm-generator" in capsys.readouterr().out


def test_module_entry_point_is_cli_main():
    assert module_main is cli.main
