"""
Module: user_interface

This module defines a simple Tkinter-based user interface for the Roma Paradigm Generator.
It allows users to enter a word, search for its paradigms, and displays the results.

Functions:
- create_ui(): Create the main user interface with entry, search button, and result text.
- update_result_text(result_message): Update the result text widget with the provided message.
- perform_search(event, from_button, animacy): Perform a search based on user input and update the result text.

Usage:
This module is intended to be used as the main entry point for the Roma Paradigm Generator application.
"""

import tkinter as tk
from search_handler import search_word
from language_processor import generate_noun_paradigms, generate_obliquus

def create_ui():
    """
    Create the main user interface with an entry, search button, and result text.

    Returns:
    Tuple: root (Tkinter root window), search_entry (Tkinter entry widget),
           result_text (Tkinter text widget), animacy_var (Tkinter StringVar).
    """
    root = tk.Tk()
    root.title("Generator romskych paradigiem")
    root.geometry("800x900")

    # Input field and Search button in one line
    input_label = tk.Label(root, text="Which word do yo want to search?  Savo lav roden?  Aké slovo hľadáte?")
    input_label.pack()

    input_frame = tk.Frame(root)
    input_frame.pack()

    search_entry = tk.Entry(input_frame, width=50)
    search_entry.pack(side=tk.LEFT)

    search_button = tk.Button(input_frame, text="Search Hľadať Rodel", command=lambda: perform_search(from_button=False, animacy=animacy_var.get()))
    search_button.pack(side=tk.LEFT, padx=(10, 0))

    # Radiobuttons for animacy below the first line
    animacy_var = tk.StringVar(value="neživotné")  # Set default value
    animacy_frame = tk.Frame(root)
    animacy_frame.pack()

    tk.Radiobutton(animacy_frame, text="Animate / Životné / Džide", variable=animacy_var, value="životné").pack(side=tk.LEFT)
    tk.Radiobutton(animacy_frame, text="Inanimate / Neživotné / Nadžide", variable=animacy_var, value="neživotné").pack(side=tk.LEFT)

    # Result_text 
    result_text = tk.Text(root, height=70, width=70, wrap=tk.WORD, bg=root.cget("bg"), highlightthickness=0, bd=0, font=("Helvetica", 10))
    result_text.pack()

    # Set focus on the search entry
    search_entry.focus_set()

    # Bind both the button click and Enter/Return key
    root.bind('<Return>', lambda event=None: perform_search(event, from_button=False, animacy=animacy_var.get()))
    search_button.bind('<Button-1>', lambda event=None: perform_search(event, from_button=True, animacy=animacy_var.get()))

    return root, search_entry, result_text, animacy_var


def update_result_text(result_message):
    """
    Update the result text widget with the provided message.

    Parameters:
    - result_message (str): The message to be displayed in the result text widget.
    """
    result_text.config(state='normal')  # Enable the Text widget for editing
    result_text.delete("1.0", tk.END)  # Clear the existing text
    result_text.insert(tk.END, result_message)
    result_text.config(state='disabled')  # Disable the Text widget for editing


def perform_search(event=None, from_button=False, animacy="neživotné"):
    """
    Perform a search based on user input and update the result text.

    Parameters:
    - event: Tkinter event (default: None).
    - from_button (bool): Indicates if the search was triggered by a button click (default: False).
    - animacy (str): Animacy of the word ('životné' or 'neživotné').

    Note: This function is bound to both the 'Return' key and the search button click events.

    """
    search_term = search_entry.get()
    search_results = search_word(search_term)

    if "word" in search_results:
        word = search_results["word"]
        part_of_speech = search_results["part_of_speech"]

        if part_of_speech == "noun":
            gender = search_results["gender"]
            obliquus_singular, obliquus_plural, gender, noun_type = generate_obliquus(word, gender)
            paradigms = generate_noun_paradigms(word, obliquus_singular, obliquus_plural, gender, noun_type, animacy=animacy)

            # Clear previous result
            update_result_text("")
           
            # Display paradigms
            update_result_text("Singulár:")
            for case, form in paradigms["Singulár"].items():
                update_result_text(result_text.get("1.0", tk.END) + f"\n{case}: {form}")

            update_result_text(result_text.get("1.0", tk.END) + "\n\nPlurál:")
            for case, form in paradigms["Plurál"].items():
                update_result_text(result_text.get("1.0", tk.END) + f"\n{case}: {form}")
        
        elif part_of_speech == "verb":
            update_result_text(f"Ma ruš! Slovesá ešte nevieme.")
        
        else:
            update_result_text(f"Ma ruš! No paradigms for {word} available yet.")
    else:
        update_result_text(f"Result: {search_results}")


if __name__ == "__main__":
    root, search_entry, result_text, animacy_var = create_ui()
    root.mainloop()
