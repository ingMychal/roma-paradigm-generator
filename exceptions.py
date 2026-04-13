"""
This module defines exceptions from certain groups of words where common rules do not apply.

Noun categories:
- `masc_xeno`: Nouns that appear as xenoclitic masculine, but are oikoclitic masculine w/ -Ø suff.
- `fem_oiko_i`: Nouns that appear as oikoclitic feminine w/ -i suff, but are masculine.

Verb categories:
- `verb_imper_i`: Class-2 verbs whose singular imperative uses the 'i!' ending instead of the default '!'.
- `verb_imper_e`: Class-2 verbs whose singular imperative uses the 'e!' ending instead of the default '!'.
"""

masc_xeno = ["mas"]
fem_oiko_i = ["voďi", "paňi"]
masc_xeno_nom_pl_a = ["lavutaris"]

verb_imper_i = ["chuťel", "ušťel", "urel"]
verb_imper_e = []  # populated by the 'del' ending rule in verbs.py
