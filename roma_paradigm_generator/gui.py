"""Tkinter window: type a word, pick the animacy, and read its paradigms."""

from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont
from typing import Optional

from .dictionary import Dictionary
from .generator import generate_paradigm_text
from .nouns import ANIMATE, INANIMATE

WINDOW_TITLE = "Generátor rómskych paradigiem"
PROMPT = "Which word do you want to search? | Savo lav roden? | Aké slovo hľadáte?"
SEARCH_LABEL = "Search | Hľadať | Rodel"
ANIMATE_LABEL = "Animate | Životné | Džide"
INANIMATE_LABEL = "Inanimate | Neživotné | Nadžide"


class ParadigmApp:
    """The main window. Build it with a Tk root, then call ``root.mainloop()``."""

    def __init__(self, root: tk.Tk, dictionary: Optional[Dictionary] = None):
        self.root = root
        self.dictionary = dictionary

        root.title(WINDOW_TITLE)
        root.geometry("800x900")

        input_frame = tk.Frame(root)
        input_frame.pack(pady=15)
        tk.Label(input_frame, text=PROMPT, font=("Helvetica", 11)).grid(row=0, column=0)

        self.search_entry = tk.Entry(input_frame, width=50)
        self.search_entry.grid(row=1, column=0)
        self.search_entry.focus_set()

        tk.Button(input_frame, text=SEARCH_LABEL, bg="#4FBCFF", command=self.search).grid(row=1, column=1)
        root.bind("<Return>", lambda _event: self.search())

        self.animacy = tk.StringVar(value=INANIMATE)
        animacy_frame = tk.Frame(root)
        animacy_frame.pack()
        for label, value in ((ANIMATE_LABEL, ANIMATE), (INANIMATE_LABEL, INANIMATE)):
            tk.Radiobutton(animacy_frame, text=label, variable=self.animacy, value=value).pack(side=tk.LEFT)

        # A monospaced font keeps the verb tables aligned.
        result_font = tkfont.nametofont("TkFixedFont").copy()
        result_font.configure(size=18)

        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side="right", fill="y")
        self.result_text = tk.Text(
            root,
            height=70,
            width=70,
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            bg=root.cget("bg"),
            highlightthickness=0,
            bd=0,
            pady=20,
            padx=20,
            font=result_font,
            state="disabled",
        )
        self.result_text.pack()
        scrollbar.config(command=self.result_text.yview)

    def show(self, message: str) -> None:
        """Replace the result area's text. The area stays read-only for the user."""
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.config(state="disabled")

    def search(self) -> None:
        self.show(generate_paradigm_text(self.search_entry.get(), self.animacy.get(), self.dictionary))


def run(dictionary: Optional[Dictionary] = None) -> None:
    """Open the window and block until it is closed."""
    root = tk.Tk()
    ParadigmApp(root, dictionary)
    root.mainloop()
