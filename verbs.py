from verbs_endings import endings_dict, tense_mapping
from search_handler import replace_special_characters
import re

def contains_valid_verb(input_string):
    # Use regular expression to check if the input contains a word ending with "l"
    return bool(re.search(r'\b\w+l\b', input_string))


def is_valid_verb(input_string):
    # Use regular expression to check if the input is a single word ending with "l"
    return bool(re.match(r'^.+l$', input_string))


def determine_conjugation_class(word):
    """
    Determine conjugation class of a verb based on its ending.
    """
    
    endings_to_conj_class = {"al": 1, "el": 2, "ol": 3}

    for ending, conj_class in endings_to_conj_class.items():
        if word.endswith(ending):
            return conj_class
    return 3 #use 3 as a fallback


def define_pres_root(word, conj_class):
    if conj_class == 1:
        pres_root = word[:-1]
        return pres_root
    else:
        pres_root = word[:-2]
        return pres_root 

  
def define_perf_root(pres_root, conj_class):
    if conj_class == 1:
        if pres_root.endswith('a'):
            return pres_root + "nď"
        
    elif conj_class == 2:
        if pres_root[-1] in 'lnrv':
            return pres_root + "d"
        elif pres_root[-1] in 'čgjkhm':
            return pres_root + "l"
        elif pres_root[-1] in 'd':
            return pres_root + "ň"
        elif pres_root[-1] in 'sš':
            return pres_root + "ť"
        elif pres_root[-1] in 'ť':
            return pres_root + "iľ"
        else:
            return "xxx"
    else:
        return pres_root + "iľ"
    

def find_word_ending_with_l(input_string):
    words = input_string.split()
    
    for word in words:
        if word.endswith("l"):
            return word.strip("()")  # Remove parentheses if present
    
    return None


def is_conditional(tense):
    if tense.startswith('cond_'):
        return True
    return False
    

def generate_verb_paradigms(verb):

    conj_class = determine_conjugation_class(verb)
    pres_root = define_pres_root(verb,conj_class)
    perf_root = define_perf_root(pres_root,conj_class)
    
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
                # Check if it's a conditional tense
                if is_conditional(tense):
                    base_tense = tense.split('_')[1]  # Get the base tense
                    try:
                        if tense == 'cond_pres':
                            base_tense = 'impf'  # Set base_tense to 'impf' for conj_class == 1
                        ending = endings_dict[conj_class][base_tense][person][number]

                        # Handle cond_perf 
                        if tense == 'cond_perf':
                            if person == 3:
                                if number == 'sg': # and en:
                                    ending = ending[:-1] + 'h' + 'as'  # Change "s" to "h"
                                elif number == 'pl':
                                    ending = ending + 'h' + 'as'  # Add "h" to the end
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
                        if verb.endswith('del'):
                            ending = "e!"
                        elif verb in ('chuťel', 'ušťel','urel'):
                            ending = 'i!'
                        else:
                            ending = "!"
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

    all_singular_forms = [forms.get('sg', '') for tense_value in verb_paradigms.values() for forms in tense_value.values()]
    max_singular_length = max(len(singular_form) for singular_form in all_singular_forms)
    # print(max_singular_length)

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
    # Use regular expression to find 'pes' as a standalone word
    pattern = r'\bpes\b'
    match = re.search(pattern, input_string)

    # If 'pes' is found as a standalone word, return True; otherwise, return False
    return bool(match)


def replace_pes_forms(paradigms):
    # Define pes_forms within the function
    pes_forms = {
        1: {'sg': 'man', 'pl': 'amen'},
        2: {'sg': 'tut', 'pl': 'tumen'},
        3: {'sg': 'pes', 'pl': 'pen'}
    }

    # Iterate through each tense, person, and number in the paradigms dictionary
    for tense, tense_data in paradigms.items():
        for person, person_data in tense_data.items():
            for number, pes_string in person_data.items():
                # Use regular expression to find standalone instances of 'pes'
                updated_string = re.sub(r'\bpes\b', lambda match: pes_forms[person][number], pes_string)
                paradigms[tense][person][number] = updated_string

    return paradigms


def replace_neutral_with_forms(input_string, verb, paradigms):

    '''
    function that replaces neutral form of verb in input_string with appropriate verb form 
    for given tense, person and number
    '''
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
    '''
    Function that integrates all helper functions to generate paradigms for input_string
    '''
    if is_valid_verb(input_string):
                paradigms = generate_verb_paradigms(input_string)
                formatted_paradigms = format_verb_paradigms(paradigms)
                return formatted_paradigms
    elif contains_valid_verb(input_string):
                verb = find_word_ending_with_l(input_string)
                paradigms = generate_verb_paradigms(verb)
                paradigms = replace_neutral_with_forms(input_string, verb, paradigms)
                if contains_standalone_pes(input_string):
                    paradigms = replace_pes_forms(paradigms)
                formatted_paradigms = format_verb_paradigms(paradigms)
                return formatted_paradigms
    

if __name__ == '__main__':
        
            input_string = 'visarel pes'
            result = process_verb(input_string)
            print(result)