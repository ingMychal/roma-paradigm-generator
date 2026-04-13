"""
This module provides functions to search for words in the xml file.

"""

from xml_parser import parse_xml_data

# XML root is parsed once and cached here after the first search.
_xml_root_cache = None


def _get_xml_root():
    """Return the cached XML root, parsing the file on first call."""
    global _xml_root_cache
    if _xml_root_cache is None:
        _xml_root_cache = parse_xml_data()
    return _xml_root_cache


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
    if "množné" in pos_rom:
        return "množné"
    elif "sloveso" in pos_rom:
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
    """
    Search for a word in the XML file and return information about it.

    Returns a dict {"word": ..., "part_of_speech": ..., "gender": ...} on success,
    or a plain string message when the word is not found.

    Raises ValueError for malformed dictionary entries.
    Raises exceptions from xml_parser (FileNotFoundError, ValueError) on parse errors.
    """
    search_term = clean_text(search_term)
    if not search_term:
        return "Ma ruš! Please enter a word to search."

    root = _get_xml_root()

    for sense_element in root.findall('.//Sense'):
        lemmaROM_elem = sense_element.find('./Definition/lemmaROM')
        if lemmaROM_elem is None:
            continue

        lemma_rom = clean_text(lemmaROM_elem.text)

        if replace_special_characters(search_term) == replace_special_characters(lemma_rom):
            posROM_elem = sense_element.find('./posROM')
            if posROM_elem is None or posROM_elem.text is None:
                raise ValueError(f"No valid posROM element found for '{lemma_rom}'.")

            pos_rom = clean_text(posROM_elem.text)
            return {
                "word": lemma_rom,
                "part_of_speech": get_pos_category(pos_rom),
                "gender": get_gender_category(pos_rom),
            }

    return f"Ma ruš! We do not have '{search_term}' in our dictionary."


if __name__ == "__main__":
    result = search_word('čambel')
    print(result)
