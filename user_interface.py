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

    # Input field and Search button in one line
    input_label = tk.Label(input_frame, 
                           text="Which word do yo want to search? | Savo lav roden? | Aké slovo hľadáte?",
                           font=("Helvetica", 11))
    input_label.grid(row=0, column=0)


    search_entry = tk.Entry(
        input_frame, 
        width=50)
    search_entry.grid(row=1, column=0)

    search_button = tk.Button(input_frame, 
                              text="Search | Hľadať | Rodel", 
                              bg='#4FBCFF',
                              command=lambda: perform_search(from_button=False, animacy=animacy_var.get()))
    search_button.grid(row=1, column=1)

    # Radiobuttons for animacy below the first line
    animacy_var = tk.StringVar(value="neživotné")  # Set default value
    animacy_frame = tk.Frame(root)
    animacy_frame.pack()

    tk.Radiobutton(animacy_frame, text="Animate | Životné | Džide", variable=animacy_var, value="životné").pack(side=tk.LEFT)
    tk.Radiobutton(animacy_frame, text="Inanimate | Neživotné | Nadžide", variable=animacy_var, value="neživotné").pack(side=tk.LEFT)

    
    # Result_text 
    result_text = tk.Text(root, 
                          height=70, 
                          width=70, 
                          yscrollcommand=scroll_y.set,  
                          wrap=tk.WORD,
                          bg=root.cget("bg"), 
                          highlightthickness=0, 
                          bd=0,pady=20,padx=20, 
                          font=("TkFixedFont", 18))
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

    """
    result_text.config(state='normal')  # Enable the Text widget for editing
    result_text.delete("1.0", tk.END)  # Clear the existing text
    result_text.insert(tk.END, result_message)
    result_text.config(state='disabled')  # Disable the Text widget for editing


def perform_search(event=None, from_button=False, animacy="neživotné"):
    """
    Perform a search based on user input and update the result text.

    """
    search_term = search_entry.get()
    search_results = search_word(search_term)

    if "word" in search_results:
        word = search_results["word"]
        part_of_speech = search_results["part_of_speech"]
        

        if part_of_speech == "množné":
            update_result_text("Ma ruš! No paradigms for plural forms available.")


        elif part_of_speech == "noun":
            gender = search_results["gender"]
            paradigms = generate_noun_paradigms(word, gender, animacy=animacy)
           
            update_result_text("")

            # Display paradigms
            formatted_paradigms = "Singulár:\n\n" + format_noun_paradigms(paradigms["Singulár"]) + "\n\nPlurál:\n\n" + format_noun_paradigms(paradigms["Plurál"])

            update_result_text(formatted_paradigms)
           
        
        elif part_of_speech == "verb":
            formatted_paradigms = process_verb(word)
            update_result_text("")
            update_result_text(formatted_paradigms)
        
        else:
            update_result_text(f"Ma ruš! No paradigms for {word} available.")
    
    else:
        update_result_text(f"Result: {search_results}")


if __name__ == "__main__":
    root, search_entry, result_text, animacy_var = create_ui()
    root.mainloop()