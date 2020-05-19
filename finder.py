import warnings
warnings.filterwarnings("ignore", message="Using slow pure-python")

from fuzzywuzzy import process

def one_note_by_title(roam_journal, query, fuzzy=False):
    """
    Find one note by its title.
    
    Parameters
    ----------
    roam_journal : array
        - Roam journal to search

    query : string
        - string containing the title of the document

    fuzzy : boolean
        - If True, finds the document with fuzzy string matching
    """

    titles = {note['title']: note for note in roam_journal}

    if fuzzy is True:
        to_match = process.extractOne(query, titles.keys())[0]
        print("fuzzy matched", to_match)
    else:
        to_match = query

    try:
        match = titles[to_match]
    except KeyError:
        # if non-fuzzy matching finds no match, return an empty dictionary
        print("keyerror")
        match = dict()

    return match

