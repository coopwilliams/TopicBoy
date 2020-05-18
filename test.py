import unittest
import sys
import io
import reader
from os import listdir
from os.path import isfile, join

test_dir = "test_files"

class ReadingTest(unittest.TestCase):
    def setUp(self):
        self.test_documents = [f for f in listdir(test_dir) if isfile(join(test_dir, f))]
    
    def test_epub(self):
        for i in self.test_documents:
            if i[-4:] == "epub":
                doc = reader.read_epub(test_dir + "/" + i)
        print(doc['filepath'])
        print(doc['title'])
        print(doc['author'])
        print(doc['full_text'][10:], "\n")
        self.assertGreater(len(doc['full_text']), 0)
    
    def test_pdf(self):
        for i in self.test_documents:
            if i[-3:] == "pdf":
                doc = reader.read_pdf(test_dir + "/" + i)
        print(doc['filepath'])
        print(doc['title'])
        print(doc['author'])
        print(doc['full_text'][10:], "\n")
        self.assertGreater(len(doc['full_text']), 0)
    
    def test_mobi(self):
        for i in self.test_documents:
            if i[-4:] == "mobi":
                doc = reader.read_mobi(test_dir + "/" + i)
        print(doc['filepath'])
        print(doc['title'])
        print(doc['author'])
        print(doc['full_text'][10:], "\n")
        self.assertGreater(len(doc['full_text']), 0)

if __name__ == '__main__':
    unittest.main()