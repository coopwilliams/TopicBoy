from ebooklib import epub
from pdfminer.high_level import extract_text

# define functions that take a document and produce
# the full text as a string.

def read_PDF(filepath):
    full_text = extract_text(filepath)
    
    doc = {
        'filepath' : filepath,
        'full_text' : full_text,
        'title' : filepath,
        'author' : "",
    }
    return doc

def read_EPUB(filepath):
    book = epub.read_epub(filepath)
    pass

def read_MOBI(filepath):
    pass

def read_DOCX(filepath):
    pass

def read_TXT(filepath):
    pass

