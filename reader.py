import ebooklib
import ftfy.bad_codecs
import json
import os
import re
import zipfile
from bs4 import BeautifulSoup
from ebooklib import epub
from mobi import Mobi
from pdfminer.high_level import extract_text

ROAM_DIR_PATH = r"C:\Users\Cooper\Documents\07_Misc_Notes\Roam_exports"
ROAM_LATEST_EXPORT_PATH = ""
HOME_PATH = os.getcwd()

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

def unpack_roam(dirpath):
    """Unpack the latest Roam Research export, set ROAM_PATH"""
    os.chdir(dirpath)
    
    # Find most recent Roam Export
    latest_export = 0
    for file in os.listdir():
        if file[-4:] == ".zip" and file[:12] == "Roam-Export-":
            export_id = int(file.lstrip("Roam-Export-")[:-4])
            if export_id > latest_export:
                latest_export = export_id

    # If it hasn't been unpacked, unpack it
    target_name = "Roam-Export-" + str(latest_export)
    target_path = os.path.join(dirpath, target_name)

    if not os.path.exists(target_path):
        with zipfile.ZipFile(target_path + ".zip", 'r') as zip_ref:
            zip_ref.extractall(target_path)
    else:
        print("latest export found")
        
    # set target path for read_roam() to find
    global ROAM_LATEST_EXPORT_PATH
    ROAM_LATEST_EXPORT_PATH = target_path
    
    # change working directory back to home
    os.chdir(HOME_PATH)

def read_roam(filepath):
    """Read the latest unpacked Roam Research export (JSON)"""

    # Make sure .zip file has been unpacked
    if not ROAM_LATEST_EXPORT_PATH:
        unpack_roam(ROAM_DIR_PATH)

    # get the file
    os.chdir(ROAM_LATEST_EXPORT_PATH)
    roam_file = os.listdir()[0]
    
    with open(roam_file, encoding='utf-8') as json_file:
        roam_journal = json.load(json_file)  

    # change working directory back to home
    os.chdir(HOME_PATH)

    return roam_journal