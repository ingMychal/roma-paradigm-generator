import pytest

tk = pytest.importorskip("tkinter")

from roma_paradigm_generator import gui  # noqa: E402


@pytest.fixture
def app(test_dictionary):
    try:
        root = tk.Tk()
    except tk.TclError as exc:  # no display, e.g. on a CI server
        pytest.skip(f"Tk cannot open a window here: {exc}")
    root.withdraw()
    yield gui.ParadigmApp(root, test_dictionary)
    root.destroy()


def result(app):
    return app.result_text.get("1.0", "end-1c")


def test_search_shows_paradigms(app):
    app.search_entry.insert(0, "kher")
    app.search()
    assert result(app).startswith("Singulár:\n\nnominatív: kher")


def test_animacy_radio_button_is_used(app):
    app.search_entry.insert(0, "džuvľi")
    app.animacy.set("životné")
    app.search()
    assert "akuzatív: džuvľa" in result(app)


def test_result_area_is_read_only(app):
    app.show("hello")
    assert str(app.result_text.cget("state")) == "disabled"
    assert result(app) == "hello"


def test_button_click_searches_once(app, monkeypatch):
    calls = []
    monkeypatch.setattr(gui, "generate_paradigm_text", lambda *args: calls.append(args) or "x")
    button = next(
        widget
        for frame in app.root.winfo_children()
        for widget in frame.winfo_children()
        if isinstance(widget, tk.Button)
    )
    button.invoke()
    assert len(calls) == 1
    # A separate mouse binding on top of the button command ran every search twice.
    assert button.bind("<Button-1>") == ""
