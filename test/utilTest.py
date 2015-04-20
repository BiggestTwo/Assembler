import unittest
import sys
import os
from Assembler.lib import util

class TestUtilFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_ParseFile(self):
        currDir = os.path.split( os.path.realpath(__file__) )[0]
        testFolder = os.path.join(currDir, 'testFiles')
        basicFile = os.path.join(testFolder, 'basic.txt')
        reservedWords = os.path.join(currDir, '../lib/resource/reservedWord')

        lines = util.ParseFile( basicFile, reservedWords)
        for i in lines:
            print i
        print len(lines)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

