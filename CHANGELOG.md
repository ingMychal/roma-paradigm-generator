# Changelog

## 1.0.0

### Changed

- The code is now a Python package, `roma_paradigm_generator`. Start it with `python -m roma_paradigm_generator` instead of `python user_interface.py`.
- The sample dictionary moved to `roma_paradigm_generator/data/SRO.sample.xml`. The full dictionary goes to `roma_paradigm_generator/data/SRO.xml`, which Git ignores.
- The dictionary is read once per run instead of on every search.
- The executable is named `RomaParadigmGenerator`.
- The ablative is labelled `ablatív`, with the accent like the other cases.
- Messages no longer start with "Result:".

### Added

- A command line: `python -m roma_paradigm_generator phral --animate` prints the paradigms.
- `pyproject.toml`, so the project installs with `pip install .` and gets a `roma-paradigm-generator` command.
- GitHub Actions CI: tests on Linux, macOS and Windows, a package install, and an executable build.
- Tests for verbs, the command line, the window, and a regression snapshot of the current output.

### Fixed

- Two of the tests always failed, so `build_script.py` never built anything.
- One click on the search button ran the search twice.
- Dragging the scrollbar did not scroll the results.
- A verb phrase starting with `pes`, such as `pes dikhel`, kept `pes` in every person instead of `man`, `tut`, `amen` ...
- Searching for a word that appears in the "not found" message, such as `word`, crashed the search.
- An empty search looked up an empty word; it now asks for a word.
- A dictionary entry with an empty lemma broke the search for every word listed after it.
- A verb whose dictionary form has no word ending in -l showed nothing; it now shows a message.
- On macOS the results font was not monospaced, so the verb tables lost their alignment.
- `requirements.txt` was saved as UTF-16, which some tools cannot read.
- `build_script.py` only worked when run from the repository folder, and used `pkg_resources`, which new setuptools versions removed.
- Running `nouns.py` directly crashed.
