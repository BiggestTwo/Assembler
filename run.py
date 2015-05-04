import os
from lib import util
import pass1
import pass2
from pass2 import assembleFormatOne, assembleFormatTwo
from pass2 import assembleFormatThree, assembleFormatFour


if __name__ == '__main__':

    currDir = os.path.split( os.path.realpath(__file__) )[0]


    pass1Result = pass1.run( 'prog_blocks.txt' )
    intermediateFile = pass1Result['intermediate']
    for k in intermediateFile:
        print k
    SYMTAB = pass1Result['SYMTAB']
    LITTAB = pass1Result['LITTAB']
    reservedWords = util.getReservedWordTable(
                    os.path.join(currDir, 'lib/resource/reservedWord') )

    opcodeTable = util.getOpcodeTable(
                    os.path.join(currDir, 'lib/resource/opcode') )

    records = \
        pass2.run(intermediateFile,
                    SYMTAB,
                    None,
                    reservedWords,
                    opcodeTable,
                    LITTAB)

    for record in records:
        print record.upper()
