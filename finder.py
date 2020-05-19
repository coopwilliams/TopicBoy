import re
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

    query : str
        - string containing the title of the document

    fuzzy : bool
        - If True, finds the document with fuzzy string matching

    Returns
    -------
    match : dict
        - dict containing Roam note with metadata
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


def contains_string(note, string, substring=False):
    """
    Returns True if note contains substring.
    
    Parameters
    ----------
    note : dict
        - Roam journal note

    string : str
        - string to find

    substring : bool
        - If True, accept notes containing the string as a substring
    """
    # return False for subnotes with no string
    if "uid" in note.keys():
        if not "string" in note.keys():
            # print("no string in", note['string'])
            return False
        else:
            # return True if note contains search string
            if substring:
                found = re.search(string, note['string'])
            else:
                found = re.search(f"\\b{string}\\b|\[\[{string}\]\]", note['string'])
            if found:
                return True
            else:
                # print("search failed for", note['string'])
                pass

    # return True if any child note contains search string
    if "children" in note.keys():
        found = False
        while not found:
            for child in note['children']:
                found = contains_string(child, string, substring=substring)
                if found:
                    return True
            # print("search failed for all children")
            return False
    else:
        # print("no children in this note")
        return False

def notes_by_string(roam_journal, string, substring=False):
    """
    Find multiple notes containing a given string.

    Parameters
    ----------
    roam_journal : array
        - Roam journal to search

    string : string
        - string that must appear in returned notes

    substring : bool
        - If True, include notes containing the string as a substring

    Returns
    -------
    matches : array
        - array of dicts containing the string
    """

    matches = []
    for note in roam_journal:
        if contains_string(note, string, substring=substring):
            matches.append(note)

    return matches