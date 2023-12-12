"""
This module provides functions to search for words in the xml file.

"""

from xml_parser import parse_xml_data

def clean_text(text):
    """Clean and normalize text, removing invisible characters."""
    cleaned_text = text.lower().replace('\n', '').replace('\t', '').replace('\r', '').replace('\u00a0', ' ')
    return cleaned_text.strip()  # Remove leading and trailing spaces

def replace_special_characters(word):
    """Replace special characters in a word."""
    translation_table = str.maketrans("čťľšžýáíéóúŕäôĺňď", "ctlszyaieouraolnd")
    return word.translate(translation_table)

def get_pos_category(pos_rom):
    """Determine part of speech category."""
    if "sloveso" in pos_rom:
        return "verb"
    elif "podstatné meno" in pos_rom:
        return "noun"
    else:
        return "other"
    
def get_gender_category(pos_rom):
    """Determine gender category."""
    if "ženský" in pos_rom:
        return "feminine"
    elif "mužský" in pos_rom:
        return "masculine"
    else:
        return "other"

def search_word(search_term):
    """Search for a word in the XML file and return information about it."""
    try:
        # Search for a word in the dictionary
        # First parse the XML
        root = parse_xml_data()
        search_term = clean_text(search_term)

        # Get the list of sense entries generated by xml_parser.py
        sense_entries = root.findall('.//Sense')

        # Iterate through the sense entries
        for sense_element in sense_entries:
            # Find the lemmaROM within the current Sense
            lemmaROM_elem = sense_element.find('./Definition/lemmaROM')
            if lemmaROM_elem is not None:
                lemma_rom = clean_text(lemmaROM_elem.text)

                # Compare search_term and lemma_rom
                if replace_special_characters(search_term) == replace_special_characters(lemma_rom):
                    posROM_elem = sense_element.find('./posROM')
                    if posROM_elem is not None and posROM_elem.text is not None:
                        pos_rom = clean_text(posROM_elem.text)
                        part_of_speech = get_pos_category(pos_rom)
                        gender = get_gender_category(pos_rom)

                        return {
                            "word": lemma_rom,
                            "part_of_speech": part_of_speech,
                            "gender": gender,
                        }
                    raise ValueError(f"No valid posROM element found for '{lemma_rom}'.")
                
        # If the word is not found, set an appropriate message and return
        return f"Ma ruš! We do not have '{search_term}' in our dictionary."


    except Exception as e:
        # Handle exceptions, log the error, and provide a meaningful message to the user
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    result = search_word('čambel')
    print(result)
