import glob
import json
import os
import spacy
import numpy as np
from finder import yield_text
from preprocessing import *
from reader import *


# load nlp model
try:
    nlp = spacy.load("en_core_web_md")
except:
    os.system("python -m spacy download en_core_web_md")
    nlp = spacy.load("en_core_web_md")

# LIBRARY_DIRPATH = r"test_files/"
# LIBRARY_DIRPATH = r"C:\Users\Cooper\Documents\06_Misc"
LIBRARY_DIRPATH = r"C:\Users\Cooper\Documents\06_Misc\1_BOOKS"
DEFAULT_FILETYPES = ["pdf", "epub"]
LIBRARY_VECTORS_PATH = r"data/library_vectors/library_vectors.json"


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def load_library_vectors(dirpath=LIBRARY_DIRPATH):

    """
    Loads library vectors from JSON to list, returning an empty list if
    file does not exist.
    """

    if os.path.exists(library_vectors_path):
        with open(library_vectors_path, encoding='utf-8') as json_file:
            vec_store = json.load(json_file)
    else:
        return list()


def vectorize_text(text):
    
    """
    Infer vector for a string of text. Handles extremely large strings.
    """

    # If text is too long for NER, chunk and then average vectors
    # This is kind of hacky but it might work.
    n = 1000000
    vectors = [nlp(text[i:i+n]).vector for i in range(0, len(text), n)]
    
    # disregard docs that can't be vectorized
    if len(vectors) == 0:
        return None

    # infer vector
    return sum(vectors) / len(vectors)


def vectorize_note(note):
    
    """
    Infer a vector for a note in a roam database.
    """
    
    note_text = ""

    # create one string from note using depth-first traversal
    for line in yield_text(note):
        if len(line) < 1:
            continue

        # join lines with full stops if they're not there already
        if line[-1] == '.':
            note_text += line
        else:
            note_text += line + '.'

    if len(note_text) == 0:
        return "None"

    # preprocess text
    note_text = remove_special(note_text)

    # vectorize text, returning vector for "None" if it fails
    vec = vectorize_text(note_text)
    if vec is not None:
        return vec
    else:
        return nlp("None").vector


def create_library_vectors(dirpath=LIBRARY_DIRPATH, 
                           filetypes=DEFAULT_FILETYPES):
    """
    Infer vectors for all new documents of the types specified, and store them
    with metadata for later use. This will be a time-consuming process that
    should run in the background. However, after the first run it will only
    process new documents.

    Parameters
    ----------
    dirpath : raw string
        path to directory of documents we want recommendations from

    filetypes : list of strings
        list of filetypes to create vectors for

    Returns
    -------
    None

    Side Effects
    ------------
    Creates a JSON array of labeled vectors corresponding to documents,
    and stores it in in data/library_vectors
    """
        
    # Get any vectors that already exist
    vec_store = load_library_vectors(library_vectors_path)
    
    # get paths of documents that are already processed
    done_paths = []
    for entry in vec_store:
        done_paths.append(entry['filepath'])

    # Get new files to process
    new_paths = []
    for ext in filetypes:
        new_paths.extend(glob.glob(dirpath + "/**/*." + ext, recursive=True))

    new_paths = list(set(new_paths).difference(set(done_paths)))

    print(new_paths)

    # read files
    new_docs = []
    for filepath in new_paths:
        print("reading", filepath)
        if filepath[-3:] == "pdf":
            new_docs.append(read_pdf(filepath))
        if filepath[-4:] == "epub":
            new_docs.append(read_epub(filepath))
        else:
            pass
    
    print(len(new_docs), "new docs")

    # TODO: change titles that are filepaths to be filenames

    for doc in new_docs:
        # preprocess text
        doc["full_text"] = remove_special(doc["full_text"])

        # infer vector, removing docs that can't be vectorized
        vec = vectorize_text(doc["full_text"])
        if vec is None:
            new_docs.remove(doc)
        else:
            doc["vector"] = vec

        # remove full text
        doc.pop("full_text", None)

    # update the vector store
    vec_store.extend(new_docs)

    # Save
    with open(LIBRARY_VECTORS_PATH, "w", encoding="utf8") as outfile:
        json.dump(vec_store, outfile, cls=NumpyEncoder)


def library_knn(vector, k=5, ord=None):

    """
    Given a vector, K nearest neighbors from library vectors.
    
    Parameters
    ----------
    vector : ndarray
        array matching the dimension of the language model in use.

    k : int
        number of neighbors to return

    ord : {non-zero int, inf, -inf, ‘fro’, ‘nuc’}, optional
        order of the norm (param for np.linalg.norm())

    Returns
    -------
    docs : list
        list of matching documents 
    """

    
    

if __name__ == "__main__":
    create_library_vectors(filetypes=['epub'])
    


    