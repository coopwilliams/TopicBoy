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
    
    def test_EPUB(self):
        for i in self.test_documents:
            if i[-4:] == "epub":
                doc = reader.read_EPUB(test_dir + "/" + i)
        self.assertGreater(len(doc['full_text']), 0)
    
    def test_PDF(self):
        for i in self.test_documents:
            if i[-3:] == "pdf":
                doc = reader.read_PDF(test_dir + "/" + i)
        self.assertGreater(len(doc['full_text']), 0)

if __name__ == '__main__':
    unittest.main()