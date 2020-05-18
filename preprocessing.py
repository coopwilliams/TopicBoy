import re

def remove_special(text):
    """Remove digits, special chars like \n, \t"""

    no_special = re.sub("\s+|\d+", " ", text)
    return no_special