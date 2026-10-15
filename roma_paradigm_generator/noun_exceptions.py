"""Nouns that the regular declension rules in ``nouns.py`` would misclassify."""

# Ends in -as/-is/-os/-us like a xenoclitic masculine, but declines as an
# oikoclitic masculine with a zero ending (mas -> mases).
OIKOCLITIC_MASCULINE_LOOKALIKES = frozenset({"mas"})

# Ends in -i like an oikoclitic feminine, but is masculine (voďi -> voďes).
MASCULINE_ENDING_IN_I = frozenset({"voďi", "paňi"})

# Xenoclitic masculines whose nominative plural ends in -a, not -i
# (lavutaris -> lavutara).
XENOCLITIC_NOMINATIVE_PLURAL_IN_A = frozenset({"lavutaris"})
