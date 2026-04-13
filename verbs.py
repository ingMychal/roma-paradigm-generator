from verbs_endings import endings_dict, tense_mapping
from search_handler import replace_special_characters
from exceptions import verb_imper_i
import re

# Compiled once at module level — avoids recompilation on every call
_RE_WORD_ENDING_L = re.compile(r'\b\w+l\b')
_RE_SINGLE_VERB = re.compile(r'^.+l$')
_RE_STANDALONE_PES = re.compile(r'\bpes\b')


def contains_valid_verb(input_string):
    """Return True if the input contains at least one word ending with 'l'."""
    return bool(_RE_WORD_ENDING_L.search(input_string))


def is_valid_verb(input_string):
    """Return True if the entire input is a single word ending with 'l'."""
    return bool(_RE_SINGLE_VERB.match(input_string))


def determine_conjugation_class(word):
    """
    Determine conjugation class of a verb based on its ending.
    Returns 1 (-al), 2 (-el), or 3 (-ol / fallback).
    """
    endings_to_conj_class = {"al": 1, "el": 2, "ol": 3}
    for ending, conj_class in endings_to_conj_class.items():
        if word.endswith(ending):
            return conj_class
    return 3  # use 3 as a fallback


def define_pres_root(word, conj_class):
    if conj_class == 1:
        return word[:-1]
    else:
        return word[:-2]


def define_perf_root(pres_root, conj_class):
    """
    Derive the perfect root from the present root.
    Raises NotImplementedError for class-2 roots with unrecognised final consonant.
    """
    if conj_class == 1:
        if not pres_root.endswith('a'):
            raise ValueError(
                f"Class-1 present root '{pres_root}' unexpectedly does not end in 'a'. "
                "Check the input verb."
            )
        return pres_root + "nď"

    elif conj_class == 2:
        last = pres_root[-1]
        if last in 'lnrv':
            return pres_root + "ď"
        elif last in 'čgjkhm':
            return pres_root + "ľ"
        elif last == 'd':
            return pres_root + "ň"
        elif last in 'sš':
            return pres_root + "ť"
        elif last == 'ť':
            return pres_root + "iľ"
        else:
            raise NotImplementedError(
                f"No perfect-root rule defined for class-2 root '{pres_root}' "
                f"ending in '{last}'. Add a rule to define_perf_root()."
            )

    else:  # conj_class == 3
        return pres_root + "iľ"


def find_word_ending_with_l(input_string):
    for word in input_string.split():
        if word.endswith("l"):
            return word.strip("()")  # Remove parentheses if present
    return None


def is_conditional(tense):
    return tense.startswith('cond_')


def generate_verb_paradigms(verb):
    conj_class = determine_conjugation_class(verb)
    pres_root = define_pres_root(verb, conj_class)
    perf_root = define_perf_root(pres_root, conj_class)

    tenses = ['pres', 'fut', 'impf', 'perf', 'cond_pres', 'cond_perf']
    persons = [1, 2, 3]
    numbers = ['sg', 'pl']
    forms = ['imper']

    paradigms = {}

    for tense in tenses:
        paradigms[tense] = {}
        base_tense = ''
        for person in persons:
            paradigms[tense][person] = {}

            for number in numbers:
                if is_conditional(tense):
                    base_tense = tense.split('_')[1]  # Get the base tense
                    try:
                        if tense == 'cond_pres':
                            base_tense = 'impf'  # Conditional present uses imperfect endings
                        ending = endings_dict[conj_class][base_tense][person][number]

                        # Handle cond_perf
                        if tense == 'cond_perf':
                            if person == 3:
                                if number == 'sg':
                                    ending = ending[:-1] + 'h' + 'as'  # Change "s" to "has"
                                elif number == 'pl':
                                    ending = ending + 'h' + 'as'  # Append "has"
                            else:
                                ending = ending + 'as'
                    except KeyError:
                        ending = ''  # Handle cases where the key is not present
                else:
                    ending = endings_dict[conj_class][tense][person][number]

                # Apply the rule for specific tenses and conj_class == 1
                if (tense in ['pres', 'fut', 'impf'] or base_tense == 'impf') and conj_class == 1:
                    modified_root = pres_root[:-1]
                    paradigm = f"{modified_root}{ending}"
                    paradigms[tense][person][number] = paradigm
                elif tense in ('perf', 'cond_perf'):
                    if person == 3 and number == 'pl':
                        perf_root_ending = perf_root[-1]
                        modified_perf_root_ending = replace_special_characters(perf_root_ending)
                        mod_perf_root = perf_root[:-1] + modified_perf_root_ending
                        paradigm = f"{mod_perf_root}{ending}"
                        paradigms[tense][person][number] = paradigm
                    else:
                        paradigm = f"{perf_root}{ending}"
                        paradigms[tense][person][number] = paradigm
                else:
                    paradigm = f"{pres_root}{ending}"
                    paradigms[tense][person][number] = paradigm

    # Generate imperative forms (only for 2nd person)
    for form in forms:
        paradigms[form] = {}
        for person in [2]:  # Only for 2nd person
            paradigms[form][person] = {}
            for number in numbers:
                if number == 'sg':
                    if conj_class == 3:
                        ending = 'uv!'
                    elif conj_class == 2:
                        if verb in verb_imper_i:
                            ending = 'i!'
                        elif verb.endswith('del'):
                            ending = 'e!'
                        else:
                            ending = '!'
                    else:
                        ending = '!'
                else:
                    if conj_class == 1:
                        ending = 'n!'
                    elif conj_class == 2:
                        ending = 'en!'
                    else:
                        ending = 'on!'

                paradigm = f"{pres_root}{ending}"
                paradigms[form][person][number] = paradigm

    return paradigms


def format_verb_paradigms(verb_paradigms):
    formatted_output = ""

    all_singular_forms = [
        forms.get('sg', '')
        for tense_value in verb_paradigms.values()
        for forms in tense_value.values()
    ]
    max_singular_length = max(len(f) for f in all_singular_forms) if all_singular_forms else 0

    for tense_key, tense_value in verb_paradigms.items():
        formatted_tense_name = tense_mapping.get(tense_key, tense_key)
        formatted_output += f"{formatted_tense_name}\n"

        max_plural_length = max(len(forms.get('pl', '')) for forms in tense_value.values())
        indentation = "    Singulár".ljust(max_singular_length + 6) + "Plurál" + "\n"
        formatted_output += indentation

        for person, forms in tense_value.items():
            person_str = f"{person}."
            singular_form = forms.get('sg', '').ljust(max_singular_length)
            plural_form = forms.get('pl', '').ljust(max_plural_length)

            formatted_output += f"{person_str.ljust(3)} {singular_form} \t{plural_form}\n"
        formatted_output += "\n"

    return formatted_output


def contains_standalone_pes(input_string):
    """Return True if the string contains 'pes' as a standalone word."""
    return bool(_RE_STANDALONE_PES.search(input_string))


def replace_pes_forms(paradigms):
    pes_forms = {
        1: {'sg': 'man', 'pl': 'amen'},
        2: {'sg': 'tut', 'pl': 'tumen'},
        3: {'sg': 'pes', 'pl': 'pen'}
    }

    for tense, tense_data in paradigms.items():
        for person, person_data in tense_data.items():
            for number, pes_string in person_data.items():
                updated_string = _RE_STANDALONE_PES.sub(
                    lambda match: pes_forms[person][number], pes_string
                )
                paradigms[tense][person][number] = updated_string

    return paradigms


def replace_neutral_with_forms(input_string, verb, paradigms):
    """
    Replace the neutral (infinitive) form of the verb in input_string with
    the appropriate conjugated form for each tense, person, and number.
    """
    modified_forms = {}

    for tense, persons in paradigms.items():
        modified_forms[tense] = {}

        for person, numbers in persons.items():
            modified_forms[tense][person] = {}

            for number, paradigm in numbers.items():
                if tense == 'imper':
                    modified_string = input_string.replace(verb, paradigm[:-1]) + '!'
                else:
                    modified_string = input_string.replace(verb, paradigm)

                modified_forms[tense][person][number] = modified_string

    return modified_forms


def process_verb(input_string):
    """
    Integrate all helper functions to generate paradigms for input_string.
    Returns formatted paradigm string, or None if no verb is detected.
    """
    if is_valid_verb(input_string):
        paradigms = generate_verb_paradigms(input_string)
        return format_verb_paradigms(paradigms)

    elif contains_valid_verb(input_string):
        verb = find_word_ending_with_l(input_string)
        paradigms = generate_verb_paradigms(verb)
        paradigms = replace_neutral_with_forms(input_string, verb, paradigms)
        if contains_standalone_pes(input_string):
            paradigms = replace_pes_forms(paradigms)
        return format_verb_paradigms(paradigms)

    return None


if __name__ == '__main__':
    input_string = 'dikhel'
    result = process_verb(input_string)
    print(result)
