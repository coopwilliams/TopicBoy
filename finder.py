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


def contains_string(note, string, substring=False,
                    case_sensitive=False):
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
    # if not case-sensitive, set all text to lowercase
    if not case_sensitive:
        string = string.lower()

    # return False for subnotes with no string
    if "uid" in note.keys():
        if not "string" in note.keys():
            return False
        else:
            if not case_sensitive:
                text = note['string'].lower()   
            # return True if note contains search string
            if substring:
                found = re.search(string, text)
            else:
                found = re.search(f"\\b{string}\\b|\[\[{string}\]\]", text)
            if found:
                return True

    # return True if any child note contains search string
    if "children" in note.keys():
        for child in note['children']:
            found = contains_string(child, string, substring=substring,
                                    case_sensitive=case_sensitive)
            if found:
                return True
        return False
    else:
        return False

def notes_by_string(roam_journal, string, substring=False, 
                    case_sensitive=False):
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
        if contains_string(note, string, substring=substring, 
                           case_sensitive=case_sensitive):
            matches.append(note)

    return matches


def extract_text(note):
    """
    Generator the uses DFT to extract all text from a child note
    """
    if not "uid" in note.keys():
        if "children" in note.keys():
            for child in note['children']:
                yield from extract_text(child)
        else:
            yield ""
    else:
        if "string" in note.keys():
            yield note['string']
        if "children" in note.keys():
            for child in note['children']:
                yield from extract_text(child)


def text_by_string(roam_journal, string, substring=False, lines_only=False,
                    case_sensitive=False):
    """
    Find the concatenated text for any note containing a given string.

    Parameters
    ----------
    roam_journal : array
        - Roam journal to search

    string : string
        - string that must appear in returned text

    substring : bool
        - If True, include text containing the string as a substring

    lines_only : bool
        - If True, include only text from the line containing the string,
            not the entire note.

    Returns
    -------
    matches : array
        - array of dicts containing the string
    """
    
    matches = notes_by_string(roam_journal, string, substring=substring,
                              case_sensitive=case_sensitive)
    texts = []
    for note in matches:
        if lines_only:
            for text in extract_text(note):
                if string in text:
                    texts.append(text) 
        else:
            texts.append(" ".join(list(extract_text(note))))

    return texts