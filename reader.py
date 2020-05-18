import ebooklib
import re
from bs4 import BeautifulSoup
from ebooklib import epub
from mobi import Mobi
from pdfminer.high_level import extract_text




# define functions that take a document and produce
# the full text with metadata.

def read_pdf(filepath):
    try:
        full_text = extract_text(filepath)
    except:
        full_text = ""

    doc = {
        'filepath' : filepath,
        'full_text' : full_text,
        'title' : filepath,
        'author' : "",
    }
    return doc

def read_epub(filepath):
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

    # Get metadata regardless of the namespace, 
    # which for EPUBs can be 'DC' or 'OPF'
    def find_by_key(data, target):
        for key, value in data.items():
            if isinstance(value, dict):
                yield from find_by_key(value, target)
            elif key == target:
                yield value

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
                output += '{0} '.format(t)
        return output

    # parse all html chapters
    def thtml2ttext(thtml):
        output = []
        for html in thtml:
            text = chap2text(html)
            output.append(text)
        return "".join(output)

    # return full text
    def epub2text(book):
        chapters = epub2thtml(book)
        ttext = thtml2ttext(chapters)
        return ttext

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

def read_mobi(filepath):
    book = Mobi(filepath)
    book.parse()

    records = []
    for record in book:
        records.append(record)

    full_text = ' '.join(records)
    title = book.title().decode('utf-8')
    author = book.author().decode('utf-8')

    doc = {
        'filepath' : filepath,
        'full_text' : full_text,
        'title' : title,
        'author' : author,
    }

    return doc

def read_docx(filepath):
    pass

def read_txt(filepath):
    pass

if __name__ == "__main__":
    try:
        epub = read_epub("test_files/slightly.epub")
        pdf = read_pdf("test_files/ncnl.pdf")
    except:
        print("couldn't rest the test files.")