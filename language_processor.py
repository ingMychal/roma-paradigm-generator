"""
This module provides functions for language processing.

Functions:
- generate_obliquus(word, gender): Generate obliquus forms of a given word based on its gender and type.
- generate_noun_paradigms(word, obliquus_singular, obliquus_plural, gender, noun_type, animacy):
    Generate noun paradigms (singular and plural forms) based on the word's properties.

"""

from exceptions import masc_xeno, fem_oiko_i, masc_xeno_nom_pl_a

def generate_obliquus(word,gender):
    """
    Generate obliquus forms of a given word based on its gender and type.

    Parameters:
    - word (str): The word for which obliquus forms are generated.
    - gender (str): The gender of the word ('masculine', 'feminine', or 'other').

    Returns: obliquus_singular, obliquus_plural, gender, noun_type
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

    if noun_type == 'xeno' and gender == 'masculine':
        for case, (suffix_singular, suffix_plural) in suffixes.items():
            if case == "nominatív":
                paradigms["Singulár"][case] = word
                paradigms["Plurál"][case] = word[:-2] + "a" if word in masc_xeno_nom_pl_a else word[:-2] + "i"

            elif case == "akuzatív":
                if animacy == "životné":
                    paradigms["Singulár"][case] = word
                    paradigms["Plurál"][case] = obliquus_plural
                else:
                    paradigms["Singulár"][case] = word
                    paradigms["Plurál"][case] = obliquus_plural
            
            elif case == "vokatív":
                if animacy == "životné":
                    paradigms["Singulár"][case] = word[:-2] + "ona"
                    paradigms["Plurál"][case] = word[:-2] + "ale"

                else:
                    paradigms["Singulár"][case] = word
                    paradigms["Plurál"][case] = obliquus_plural
            
            elif case == "inštrumentál":
                paradigms["Singulár"][case] = word[:-1] + "ha"
                paradigms["Plurál"][case] = obliquus_plural + suffix_plural

            else:
                paradigms["Singulár"][case] = obliquus_singular + suffix_singular
                paradigms["Plurál"][case] = obliquus_plural + suffix_plural


    elif noun_type == 'oiko' and gender == 'masculine':
        for case, (suffix_singular, suffix_plural) in suffixes.items():
            if case == "nominatív":
                paradigms["Singulár"][case] = word
                if word.endswith("o"):
                    paradigms["Plurál"][case] = word[:-1] + "e"
                elif word in fem_oiko_i:
                    paradigms["Plurál"][case] = word[:-1] + "a"
                else:
                    paradigms["Plurál"][case] = word + "a"

            elif case == "akuzatív":
                if animacy == "životné":
                    paradigms["Singulár"][case] = obliquus_singular
                    paradigms["Plurál"][case] = obliquus_plural
                else:
                    paradigms["Singulár"][case] = word 
                    if word.endswith("o"):
                        paradigms["Plurál"][case] = word[:-1] + "e"
                    elif word in fem_oiko_i:
                        paradigms["Plurál"][case] = word[:-1] + "a"
                    else:
                        paradigms["Plurál"][case] = word + "a"

            elif case == "vokatív":
                if animacy == "životné":
                    paradigms["Singulár"][case] = word[:-1] + "eja" if word.endswith("o") else word + "eja"
                    paradigms["Plurál"][case] = word[:-1] + "ale" if word.endswith("o") else word + "ale"
                else:
                    paradigms["Singulár"][case] = word 
                    if word.endswith("o"):
                        paradigms["Plurál"][case] = word[:-1] + "e"
                    elif word in fem_oiko_i:
                        paradigms["Plurál"][case] = word[:-1] + "a"
                    else:
                        paradigms["Plurál"][case] = word + "a"

            elif case == "inštrumentál":
                paradigms["Singulár"][case] = obliquus_singular[:-1] + suffix_singular
                paradigms["Plurál"][case] = obliquus_plural + suffix_plural
            
            else:
                paradigms["Singulár"][case] = obliquus_singular + suffix_singular
                paradigms["Plurál"][case] = obliquus_plural + suffix_plural


    elif noun_type == 'xeno' and gender == 'feminine':
        for case, (suffix_singular, suffix_plural) in suffixes.items():
            if case == "nominatív":
                paradigms["Singulár"][case] = word
                paradigms["Plurál"][case] = word[:-1] + "i"

            elif case == "akuzatív":
                if animacy == "životné":
                    paradigms["Singulár"][case] = word
                    paradigms["Plurál"][case] = obliquus_plural
                else:
                    paradigms["Singulár"][case] = word
                    paradigms["Plurál"][case] = obliquus_plural

            elif case == "vokatív":
                if animacy == "životné":
                    paradigms["Singulár"][case] = word
                    paradigms["Plurál"][case] = word[:-1] + "i"
                else:
                    paradigms["Singulár"][case] = word
                    paradigms["Plurál"][case] = obliquus_plural

            else:
                paradigms["Singulár"][case] = obliquus_singular + suffix_singular
                paradigms["Plurál"][case] = obliquus_plural + suffix_plural
        
    
    elif noun_type == 'oiko' and gender == 'feminine':
        # Apply specific rules based on noun type and gender for singular and plural
        for case, (suffix_singular, suffix_plural) in suffixes.items():
            if case == "nominatív":
                paradigms["Singulár"][case] = word
                if word.endswith("i"):
                    paradigms["Plurál"][case] = word[:-1] + "a"
                else:
                    paradigms["Plurál"][case] = word + "a"
            
            elif case == "akuzatív":
                if animacy == "životné":
                    paradigms["Singulár"][case] = obliquus_singular
                    paradigms["Plurál"][case] = obliquus_plural
                else:
                    paradigms["Singulár"][case] = word
                    paradigms["Plurál"][case] = obliquus_plural


            elif case == "vokatív":
                if animacy == "životné":
                    if word.endswith("i"):
                        paradigms["Singulár"][case] = word[:-1] + "ije"
                        paradigms["Plurál"][case] = word[:-1] + "ale"   
                    else:
                        paradigms["Singulár"][case] = word + "ije"
                        paradigms["Plurál"][case] = word + "ale"
                else:
                    paradigms["Singulár"][case] = word
                    paradigms["Plurál"][case] = obliquus_plural

                      
            else:
                paradigms["Singulár"][case] = obliquus_singular + suffix_singular
                paradigms["Plurál"][case] = obliquus_plural + suffix_plural         

                

    else:
            for case, (suffix_singular, suffix_plural) in suffixes.items():
                paradigms["Singulár"][case] = obliquus_singular + suffix_singular
                paradigms["Plurál"][case] = obliquus_plural + suffix_plural
    
    return paradigms
if __name__ == '__main__':
            
    test = generate_obliquus("khosno","masculine")
    print(test)

    test2 = generate_noun_paradigms("uraviben", "uravibnas",	"uravibnen",	"masculine",	"oiko",	"neživotné")
    print(test2)
