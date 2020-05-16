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
                text = reader.read_EPUB(test_dir + "/" + i)
        print(text)
        self.assertGreater(len(text), 0)

if __name__ == '__main__':
    unittest.main()