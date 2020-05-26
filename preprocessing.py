import re

def remove_special(text):
    """Remove digits, special chars like \n, \t"""

    no_special = re.sub("\s+|\d+", " ", text)
    return " ".join(no_special.split())

def remove_non_alpha(text):
    """Remove all non-alphabet chars"""
    all_alpha = re.sub("[^a-zA-Z]+", " ", text)
    return " ".join(all_alpha.split())



# TODO: replace \n with a period to denote the end of a sentence.