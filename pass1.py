import sys, os
from lib import util

#   perform pass one
#   @fileName - file name (does not include directory)
#   return - a dictionary : {'intermediate' : an array of assembly code (location included)
#                            'SYMTABL' : SYMTAB}
def run(fileName) :
    # variables (data structures)
    LOCCTR = 0
    STARTING_ADDRESS = 0
    PROGRAM_LENGTH = 0
    SYMTAB = {}
    OPTAB = {}
    ERROR = 0
    # end variables

    # load OPTAB from file
    opcodeFileDir = './lib/resource/opcode'

    opcodeFile = open(opcodeFileDir)
    for line in opcodeFile :
        opPair = line.split(' ')
        op = opPair[0]
        code = opPair[1]
        code = code.replace('\n', '')
        OPTAB[op] = code
    # print OPTAB

    # file directory
    currDir = os.path.split( os.path.realpath(__file__) )[0]
    testFolder = os.path.join(currDir, './test/testFiles')
    fileDir = os.path.join(testFolder, fileName)
    reservedWords = os.path.join(currDir, './lib/resource/reservedWord')

    # begin (read assembly code line by line)
    revisedAssemblyCode = []
    firstLine = 0
    for i in util.ParseFile( fileDir, reservedWords):
        # print i
        opcode = i['operation']
        # read first line to see if START exists
        if firstLine == 0:
            firstLine = 1
            if opcode == 'START' :
                # starting address
                STARTING_ADDRESS = int(i['operand'][0])
                LOCCTR = STARTING_ADDRESS
                # write line to intermediate file
                i['location'] = None
                revisedAssemblyCode.append(i)
                # read next input line
                continue
            else :
                LOCCTR = 0
        if opcode != 'END' :
            # write line to intermediate file
            i['location'] = util.decToHex(LOCCTR)
            revisedAssemblyCode.append(i)
            # assign label with memory addr
            if i['label'] != None :
                label = i['label']
                # search SYMTAB for LABEL
                if SYMTAB.has_key(label) :
                    # set error flag
                    ERROR = 1
                else :
                    SYMTAB[label] = LOCCTR
            # search OPTAB for opcode
            if OPTAB.has_key(opcode) :
                LOCCTR += i['length']
            elif opcode == 'WORD' :
                LOCCTR += 3
            elif opcode == 'RESW' :
                LOCCTR += 3 * int(i['operand'][0])
            # elif opcode == 'BYTE' :
                # find length of constant
            else :
                # error
                ERROR = 1
        else :
            # write last line to intermediate file (END)
            i['location'] = util.decToHex(LOCCTR)
            revisedAssemblyCode.append(i)
            # save (LOCCTR - starting address) as program length
            PROGRAM_LENGTH = LOCCTR - STARTING_ADDRESS
            break
    # end pass 1

    # return a dictionary containing intermediate code(with memory location) and SYMTAB
    result = {}
    result['intermediate'] = revisedAssemblyCode
    result['SYMTAB'] = SYMTAB
    return result

# sample run
fileName = 'basic.txt'
result = run(fileName)
intermediate = result['intermediate']
symtab = result['SYMTAB']
# print out intermediate
print 'intermediate code: '
for i in range(len(intermediate)) : 
    print intermediate[i]
print 
# print out SYMTAB
print 'SYMTAB: '
print symtab
# end sample run
