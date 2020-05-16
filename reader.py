import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from pdfminer.high_level import extract_text

# define functions that take a document and produce
# the full text with metadata.

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
    blacklist = [
        '[document]',
        'noscript', 
        'header',   
        'html', 
        'meta', 
        'head',
        'input', 
        'script',
    ]

    book = epub.read_epub(filepath)

    # get EPUB content as HTML chapters
    def epub2thtml(book):
        chapters = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                chapters.append(item.get_content()) 
        return chapters

    # get HTML chapter as text
    def chap2text(chap):
        output = ''
        soup = BeautifulSoup(chap, 'html.parser')
        text = soup.find_all(text=True)
        for t in text:
            if t.parent.name not in blacklist:
                output += '{} '.format(t)
        return output

    # parse all html chapters
    def thtml2ttext(thtml):
        output = []
        for html in thtml:
            text = chap2text(html)
            output.append(text)
        return " ".join(output)

    # return full text
    def epub2text(book):
        chapters = epub2thtml(book)
        ttext = thtml2ttext(chapters)
        return ttext

    # this package has a get_metadata() function.
    # But this helper function will get the same result
    # regardless of the namespace, which can be 'DC' or 'OPF'
    def find_by_key(data, target):
        for key, value in data.items():
            if isinstance(value, dict):
                yield from find_by_key(value, target)
            elif key == target:
                yield value

    full_text = epub2text(book)
    title = next(find_by_key(book.metadata, 'title'))
    author = next(find_by_key(book.metadata, 'creator'))

    # get the string values out of lists or tuples
    while isinstance(title, list) or isinstance(title, tuple):
        title = title[0] 
    while isinstance(author, list) or isinstance(author, tuple):
        author = author[0] 

    doc = {
        'filepath' : filepath,
        'full_text' : full_text,
        'title' : title,
        'author' : author,
    }
    
    return doc

def read_MOBI(filepath):
    pass

def read_DOCX(filepath):
    pass

def read_TXT(filepath):
    pass

