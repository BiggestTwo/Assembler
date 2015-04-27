import os
from lib import util
import pass1
import pass2
from pass2 import assembleFormatOne, assembleFormatTwo
from pass2 import assembleFormatThree, assembleFormatFour


if __name__ == '__main__':
    currDir = os.path.split( os.path.realpath(__file__) )[0]

    pass1Result = pass1.run( 'basic.txt' )
    intermediateFile = pass1Result['intermediate']
    SYMTAB = pass1Result['SYMTAB']
    reservedWords = util.getReservedWordTable(
                    os.path.join(currDir, 'lib/resource/reservedWord') )

    opcodeTable = util.getOpcodeTable(
                    os.path.join(currDir, 'lib/resource/opcode') )

    pass2.run(intermediateFile, SYMTAB, None, reservedWords, opcodeTable)
