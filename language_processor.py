from exceptions import masc_xeno, fem_oiko_i, masc_xeno_nom_pl_a

def generate_obliquus(word,gender):
    """
    Generate obliquus forms of a given word based on its gender and type.

    """
    obliquus_singular, obliquus_plural = word, word

    # Abstract
    if word.endswith(("ben", "pen", "ipen", "iben")):
        noun_type, gender = "oiko", "masculine"
        
        obliquus_singular = word[:-2] + word[-1] + "as"
        obliquus_plural =  obliquus_singular[:-2] + "en"
    # Xenoclitic masculine 
    elif word.endswith(("is", "as", "os", "us")) and word not in masc_xeno:
        obliquus_plural = word[:-2] + "en"
        noun_type, gender = "xeno", "masculine"

    # Xenoclitic feminine 
    elif word.endswith(("a")):
        obliquus_plural = word[:-1] + "en"
        noun_type, gender = "xeno", "feminine"
    
    # Oikoclitic feminine -i suff.
    elif word.endswith("i") and word not in fem_oiko_i:
        obliquus_singular, obliquus_plural = word[:-1] + "a", word[:-1] + "en"
        noun_type, gender = "oiko", "feminine"

    # Oikoclitic Masculine -o suff.
    elif word.endswith("o") or word in fem_oiko_i:
        obliquus_singular, obliquus_plural = word[:-1] + "es", word[:-1] + "en"
        noun_type, gender = "oiko", "masculine"

    # Oikoclitic Masculine -Ø suff.
    elif gender == "masculine" or word in masc_xeno:
        obliquus_singular, obliquus_plural = word + "es", word + "en"
        noun_type, gender = "oiko", "masculine"

     # Oikoclitic feminine -Ø suff.
    elif gender == "feminine":
        obliquus_singular, obliquus_plural = word + "a", word + "en"
        noun_type, gender = "oiko", "feminine"
    
    else:
        noun_type, gender = "other", "other"

    return obliquus_singular, obliquus_plural, gender, noun_type


def generate_noun_paradigms(word, obliquus_singular, obliquus_plural, gender, noun_type, animacy):
    """
    Generate noun paradigms (singular and plural forms) based on the word's properties.

    Parameters:
    - word (str): The base word for which paradigms are generated.
    - obliquus_singular (str): Obliquus singular form of the word.
    - obliquus_plural (str): Obliquus plural form of the word.
    - gender (str): Gender of the word ('masculine', 'feminine', or 'other').
    - noun_type (str): Noun type ('xeno', 'oiko', or 'other').
    - animacy (str): Animacy of the word ('životné' or 'neživotné').

    Returns:
    Dictionary: Paradigms for both singular and plural forms in different cases.
    """
    suffixes = {
        "nominatív": ["", ""],
        "genitív": ["kero", "gero"],
        "datív": ["ke", "ge"],
        "akuzatív": ["es", "a"] if gender == 'masculine' else ["a", "en"],
        "vokatív": ["eja", "ije"] if gender == 'masculine' else ["ije", "ale"],
        "lokál": ["te", "de"],
        "ablativ": ["tar", "dar"],
        "inštrumentál": ["ha", "ca"]
    }

    paradigms = {"Singulár": {}, "Plurál": {}}

    for case, (suffix_singular, suffix_plural) in suffixes.items():
        singular, plural = apply_case_rules(word, obliquus_singular, obliquus_plural, gender, noun_type, animacy, case, suffix_singular, suffix_plural)
        paradigms["Singulár"][case] = singular
        paradigms["Plurál"][case] = plural

    return paradigms


def apply_case_rules(word, obliquus_singular, obliquus_plural, gender, noun_type, animacy, case, suffix_singular, suffix_plural):
    if case == "nominatív":
        return nominative_case(word, gender, noun_type, obliquus_plural)
    elif case == "akuzatív":
        return accusative_case(word, obliquus_singular, obliquus_plural, suffix_singular, suffix_plural, gender, animacy, noun_type)
    elif case == "vokatív":
        return vocative_case(word,obliquus_singular,suffix_singular, obliquus_plural,suffix_plural, gender, animacy, noun_type)
    elif case == "inštrumentál":
        return instrumental_case(word, obliquus_singular,obliquus_plural, gender, noun_type, suffix_singular, suffix_plural)
    else:
        return obliquus_singular + suffix_singular, obliquus_plural + suffix_plural

def nominative_case(word, gender, noun_type, obliquus_plural):
    # sourcery skip: use-fstring-for-concatenation
    if noun_type == 'xeno' and gender == 'masculine':
        return word, word[:-2] + ("a" if word in masc_xeno_nom_pl_a else "i")
    elif noun_type == 'oiko' and gender == 'masculine':
        if word.endswith("o") or word in fem_oiko_i:
            return word, word[:-1] + ("e" if word.endswith("o") else "a")
        else:
            return word, word + "a"
    elif noun_type == 'xeno' and gender == 'feminine':
        return word, word[:-1] + "i"
    elif noun_type == 'oiko' and gender == 'feminine':
        return (word, word[:-1] + "a") if word.endswith("i") else (word, word + "a")
    else:
        return word, obliquus_plural 
def accusative_case(word, obliquus_singular,obliquus_plural, suffix_singular, suffix_plural, gender, animacy, noun_type):
    # sourcery skip: use-fstring-for-concatenation
    if noun_type == 'xeno':
        return word,obliquus_plural
    elif noun_type == 'oiko' and gender == 'masculine':
        if animacy == "životné":
            return obliquus_singular, obliquus_plural
        if word.endswith("o") or word in fem_oiko_i:
            return word, word[:-1] + ("e" if word.endswith("o") else "a")
        return word,  word + "a"
    elif noun_type == 'oiko' and gender == 'feminine':
        return (obliquus_singular if animacy == "životné" else word), obliquus_plural
    else:
        return obliquus_singular + suffix_singular, obliquus_plural + suffix_plural



def vocative_case(word,obliquus_singular,suffix_singular, obliquus_plural,suffix_plural, gender, animacy, noun_type):
    if noun_type == 'xeno' and gender == 'masculine':
        if animacy == "životné":
            return word[:-2] + "ona", word[:-2] + "ale"
        else:
            return word, obliquus_plural
    elif noun_type == 'oiko' and gender == 'masculine':
        if animacy == "životné":
            return word[:-1] + "eja" if word.endswith("o") else word + "eja", word[:-1] + "ale" if word.endswith("o") else word + "ale"
        if word.endswith("o"):
            return word, word[:-1] + "e"
        elif word in fem_oiko_i:
            return word, word[:-1] + "a"
        else:
            return word, word + "a"
    elif noun_type == 'xeno' and gender == 'feminine':
        if animacy == "životné":
            return word,  word[:-1] + "i"
        else:
            return word, obliquus_plural
    elif noun_type == 'oiko' and gender == 'feminine':
        if animacy != "životné":
            return word, obliquus_plural
        if word.endswith("i"):
            return word[:-1] + "ije", word[:-1] + "ale"   
        else:
            return word + "ije", word + "ale"
    else:
        return obliquus_singular + suffix_singular, obliquus_plural + suffix_plural


def instrumental_case(word, obliquus_singular,obliquus_plural, gender, noun_type, suffix_singular, suffix_plural):
    if noun_type == 'xeno' and gender == 'masculine':
        return word[:-1] + "ha", obliquus_plural + suffix_plural
    elif noun_type == 'oiko' and gender == 'masculine':
        return obliquus_singular[:-1] + suffix_singular, obliquus_plural + suffix_plural
    else:
        return obliquus_singular + suffix_singular, obliquus_plural + suffix_plural


if __name__ == '__main__':
            
    test = generate_obliquus("voďi","masculine")
    print(test)
    
    # # test2 = generate_noun_paradigms("uraviben", "uravibnas",	"uravibnen",	"masculine",	"oiko",	"neživotné")
    # # print(test2)
    
    # test3 = generate_noun_paradigms('mas','mases','masen','masculine','oiko','neživotné')
    # print(test3)
    