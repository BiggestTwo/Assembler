import unittest
import sys
import os
from Assembler.lib import util
from Assembler import pass2

class TestUtilFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_compliment(self):
        self.assertEqual( util.towsCompliment( -2, 4 ), '1110' )
        
    def test_AssembleInstruction(self):
        currDir = os.path.split( os.path.realpath(__file__) )[0]
        testFolder = os.path.join(currDir, 'testFiles')
        basicFile = os.path.join(testFolder, 'basic.txt')
        reservedWords = os.path.join(currDir, '../lib/resource/reservedWord')
        opcodeTablePath = os.path.join( currDir, '../lib/resource/opcode')
        SYMTAB = {}
        SYMTAB['A'] = '0'
        SYMTAB['X'] = '1'
        SYMTAB['L'] = '2'
        SYMTAB['B'] = '3'
        SYMTAB['S'] = '4'
        SYMTAB['T'] = '5'
        SYMTAB['LENGTH'] = '0033'
        SYMTAB['WRREC'] = '105D'

        objectCode = pass2.assembleFormatOne('F0')
        self.assertEqual( objectCode, '0xF0')
        objectCode = pass2.assembleFormatTwo('B4', ['X'], SYMTAB)
        self.assertEqual( objectCode, '0xB410' )
        objectCode = pass2.assembleFormatTwo('A0', ['A', 'S'], SYMTAB)
        self.assertEqual( objectCode, '0xA004')
        objectCode = pass2.assembleFormatThree('00', ['LENGTH'],'000D','0033',\
                                                SYMTAB, False) 
        self.assertEqual( objectCode, '0x032026')
        objectCode = pass2.assembleFormatFour('48', ['WRREC'], '0017', '105D',\
                                                False)
        self.assertEqual( objectCode, '0x4b10105d')
        objectCode = pass2.assembleFormatThree('68', ['#LENGTH'], '0006', '0033',\
                                                SYMTAB, False)
        self.assertEqual( objectCode, '0x69202d')

    def test_getOpcodeTable(self):
        currDir = os.path.split( os.path.realpath(__file__) )[0]
        a = util.getOpcodeTable( os.path.join(currDir, '../lib/resource/opcode'))
        '''
        for key, value in a.items():
            print key, value
        '''

    def test_ParseFile(self):
        currDir = os.path.split( os.path.realpath(__file__) )[0]
        testFolder = os.path.join(currDir, 'testFiles')
        basicFile = os.path.join(testFolder, 'basic.txt')
        reservedWords = os.path.join(currDir, '../lib/resource/reservedWord')
        opcodeTablePath = os.path.join( currDir, '../lib/resource/opcode')

        reservedWordTable = util.getReservedWordTable( reservedWords )
        opcodeTable = util.getOpcodeTable( opcodeTablePath )
        f = open( basicFile )
        for line in f:
            line = util.ParseLine(line, reservedWordTable, opcodeTable)
            print line        
        f.close()


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

