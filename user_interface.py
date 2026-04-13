"""
This module defines a simple Tkinter-based user interface for the Roma Paradigm Generator.
It allows users to enter a word, search for its paradigms, and displays the results.

Usage:
This module is intended to be used as the main entry point for the Roma Paradigm Generator application.
"""

import tkinter as tk
from search_handler import search_word
from nouns import generate_noun_paradigms, format_noun_paradigms
from verbs import process_verb


def create_ui():
    """
    Create the main user interface with an entry, search button, and result text.
    """
    root = tk.Tk()
    root.title("Generator romskych paradigiem")
    root.geometry("800x900")

    scroll_y = tk.Scrollbar(root)
    scroll_y.pack(side="right", fill="y")

    input_frame = tk.Frame(root)
    input_frame.pack(pady=15)

    input_label = tk.Label(input_frame,
                           text="Which word do you want to search? | Savo lav roden? | Aké slovo hľadáte?",
                           font=("Helvetica", 11))
    input_label.grid(row=0, column=0)

    search_entry = tk.Entry(input_frame, width=50)
    search_entry.grid(row=1, column=0)

    # Animacy radio buttons
    animacy_var = tk.StringVar(value="neživotné")
    animacy_frame = tk.Frame(root)
    animacy_frame.pack()

    tk.Radiobutton(animacy_frame, text="Animate | Životné | Džide",
                   variable=animacy_var, value="životné").pack(side=tk.LEFT)
    tk.Radiobutton(animacy_frame, text="Inanimate | Neživotné | Nadžide",
                   variable=animacy_var, value="neživotné").pack(side=tk.LEFT)

    result_text = tk.Text(root,
                          height=70,
                          width=70,
                          yscrollcommand=scroll_y.set,
                          wrap=tk.WORD,
                          bg=root.cget("bg"),
                          highlightthickness=0,
                          bd=0, pady=20, padx=20,
                          font=("TkFixedFont", 18))
    result_text.pack()

    # Wire the scrollbar to the text widget
    scroll_y.config(command=result_text.yview)

    search_button = tk.Button(
        input_frame,
        text="Search | Hľadať | Rodel",
        bg='#4FBCFF',
        command=lambda: perform_search(
            search_entry=search_entry,
            result_text=result_text,
            animacy=animacy_var.get()
        )
    )
    search_button.grid(row=1, column=1)

    # Bind Enter key — only one binding, no duplicate on the button
    root.bind('<Return>', lambda event: perform_search(
        search_entry=search_entry,
        result_text=result_text,
        animacy=animacy_var.get()
    ))

    search_entry.focus_set()
    return root, search_entry, result_text, animacy_var


def update_result_text(result_text, result_message):
    """Update the result text widget with the provided message."""
    result_text.config(state='normal')
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, result_message)
    result_text.config(state='disabled')


def perform_search(search_entry, result_text, animacy="neživotné"):
    """
    Perform a search based on user input and update the result text.
    """
    search_term = search_entry.get().strip()
    if not search_term:
        update_result_text(result_text, "Ma ruš! Please enter a word to search.")
        return

    try:
        search_results = search_word(search_term)
    except Exception as e:
        update_result_text(result_text, f"An error occurred: {e}")
        return

    # search_word returns a dict on success, a plain string when not found
    if not isinstance(search_results, dict):
        update_result_text(result_text, f"Result: {search_results}")
        return

    word = search_results["word"]
    part_of_speech = search_results["part_of_speech"]

    if part_of_speech == "množné":
        update_result_text(result_text, "Ma ruš! No paradigms for plural forms available.")

    elif part_of_speech == "noun":
        gender = search_results["gender"]
        paradigms = generate_noun_paradigms(word, gender, animacy=animacy)
        formatted = (
            "Singulár:\n\n"
            + format_noun_paradigms(paradigms["Singulár"])
            + "\n\nPlurál:\n\n"
            + format_noun_paradigms(paradigms["Plurál"])
        )
        update_result_text(result_text, formatted)

    elif part_of_speech == "verb":
        formatted = process_verb(word)
        if formatted is None:
            update_result_text(result_text, f"Ma ruš! Could not generate paradigms for '{word}'.")
        else:
            update_result_text(result_text, formatted)

    else:
        update_result_text(result_text, f"Ma ruš! No paradigms for {word} available.")


if __name__ == "__main__":
    root, search_entry, result_text, animacy_var = create_ui()
    root.mainloop()
