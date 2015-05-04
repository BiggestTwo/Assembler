import os
import sys
from lib import util
import pass1
import pass2
from pass2 import assembleFormatOne, assembleFormatTwo
from pass2 import assembleFormatThree, assembleFormatFour


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'A source code file name should be provided' 

    else:
        fileName = sys.argv[1]
        objectProgramPath = 'object_program.txt'
        objectCodeFilePath = 'object_code.txt'
        currDir = os.path.split( os.path.realpath(__file__) )[0]
        objectCodeFilePath = os.path.join(currDir, objectCodeFilePath)
        objectProgramPath = os.path.join(currDir, objectProgramPath)


        pass1Result = pass1.run(fileName)
        intermediateFile = pass1Result['intermediate']
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

        with open(objectCodeFilePath, 'w') as f:
            for i in intermediateFile:
                if 'objectCode' in i and i['objectCode'] is not None:
                    temp = i['objectCode'].upper()[2:] 
                    f.write( temp + '\n' )
        with open( objectProgramPath, 'w' ) as f:
            for record in records:
                print record.upper()
                f.write( record.upper() + '\n' )