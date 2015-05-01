import sys, os
from lib import util

#   takes an expression as one of the three cases
#   a) * (curr location)
#   b) a symbol ( can be found in SYMTAB )
#   c) an expression involves two symbols (e.g. A - B or A + B)
#   returns the result IN HEXADECIMAL
def parseExpression(exp, SYMTAB, LOCCTR) :
    # case 1) * (curr location)
    if len(exp) == 1 and exp == '*' :
        return util.decToHex(LOCCTR)
    # case 2) not an expression
    if '+' not in exp and '-' not in exp :
        # find the location of this symbol from SYMTAB 
        return SYMTAB[exp]
    else : # case 3) an expression (+ or -)
        # find both symbols from SYMTAB and do a calculation
        if '+' in exp :
            pos = exp.find('+')
            op1 = exp[0:pos]
            op2 = exp[(pos + 1): len(exp)]
            result = int(util.hexToDec(str(SYMTAB[op1]))) + int(util.hexToDec(str(SYMTAB[op2])))
            return util.decToHex(result)
        if '-' in exp :
            pos = exp.find('-')
            op1 = exp[0:pos]
            op2 = exp[(pos + 1): len(exp)]
            result = int(util.hexToDec(str(SYMTAB[op1]))) - int(util.hexToDec(str(SYMTAB[op2])))
            return util.decToHex(result)
    return ''

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
    LITTAB = []
    LITARR = []
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
    opcodeTablePath = os.path.join( currDir, './lib/resource/opcode')

    # begin (read assembly code line by line)
    revisedAssemblyCode = []
    firstLine = 0
    for i in util.ParseFile( fileDir, reservedWords, opcodeTablePath ):
        opcode = i['operation']
        operand = i['operand']
        # read first line to see if START exists
        if firstLine == 0:
            firstLine = 1
            if opcode == 'START' :
                # starting address
                STARTING_ADDRESS = int(i['operand'][0], 16)
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
                    SYMTAB[label] = util.decToHex(LOCCTR)
            # search OPTAB for opcode
            # symbol defining
            if opcode == 'EQU' :
                # put the label into SYMTAB with its operand as value (immediate addressing)
                resultOfExpression = parseExpression(operand[0], SYMTAB, LOCCTR)
                SYMTAB[i['label']] = resultOfExpression
            # literal
            if opcode == 'LTORG' :
                # populate all literals up to now
                for counter in range(len(LITTAB)) :
                    currLiteral = LITTAB[counter]
                    if currLiteral['location'] == None : # not yet assigned
                        currLiteral['location'] = util.decToHex(LOCCTR)
                        LOCCTR += currLiteral['length']
                        # write into intermediate file
                        newLine = {}
                        newLine['format'] = 3
                        newLine['label'] = None
                        newLine['length'] = currLiteral['length']
                        newLine['location'] = currLiteral['location']
                        newLine['operation'] = currLiteral['name']
                        newLine['operand'] = None
                        revisedAssemblyCode.append(newLine)
            if OPTAB.has_key(opcode) :
                LOCCTR += i['length']
            elif opcode == 'WORD' :
                LOCCTR += 3
            elif opcode == 'RESW' :
                LOCCTR += 3 * int(i['operand'][0])
            elif opcode == 'RESB' :
                LOCCTR += int(i['operand'][0])
            elif opcode == 'BYTE' :
                LOCCTR += util.lengthOfVariable(i['operand'][0])
            else :
                # error
                ERROR = 1
            # operand

            # literal
            if util.isLiteral(operand) :
                # store into literal table
                literalOperand = operand[0]
                newLiteral = {}
                newLiteral['name'] = literalOperand
                newLiteral['value'] = util.buildLiteralValue(literalOperand) 
                newLiteral['location'] = None
                newLiteral['length'] = util.lengthOfLiteral(literalOperand)
                if literalOperand not in LITARR : 
                    LITTAB.append(newLiteral)
                    LITARR.append(newLiteral['name'])
        else :
            # write last line to intermediate file (END)
            i['location'] = util.decToHex(LOCCTR)
            revisedAssemblyCode.append(i)
            # populate LITTAB
            for counter in range(len(LITTAB)) :
                currLiteral = LITTAB[counter]
                if currLiteral['location'] == None : # not yet assigned
                    currLiteral['location'] = util.decToHex(LOCCTR)
                    LOCCTR += currLiteral['length']
                    # write into intermediate file
                    newLine = {}
                    newLine['format'] = 3
                    newLine['label'] = None
                    newLine['length'] = currLiteral['length']
                    newLine['location'] = currLiteral['location']
                    newLine['operation'] = currLiteral['name']
                    newLine['operand'] = None
                    revisedAssemblyCode.append(newLine)
            # save (LOCCTR - starting address) as program length
            PROGRAM_LENGTH = LOCCTR - STARTING_ADDRESS
            break
    # end pass 1

    # add register number to SYMTAB
    SYMTAB['A'] = '0'
    SYMTAB['X'] = '1'
    SYMTAB['L'] = '2'
    SYMTAB['B'] = '3'
    SYMTAB['S'] = '4'
    SYMTAB['T'] = '5'

    # return a dictionary containing intermediate code(with memory location) and SYMTAB
    result = {}
    result['intermediate'] = revisedAssemblyCode
    result['SYMTAB'] = SYMTAB
    result['LITTAB'] = LITTAB
    return result

# sample run
fileName = 'literals.txt'
result = run(fileName)
intermediate = result['intermediate']
symtab = result['SYMTAB']
littab = result['LITTAB']
# print out intermediate
print 'intermediate code: '
for i in range(len(intermediate)) : 
    print intermediate[i]
print 
# print out SYMTAB
print 'SYMTAB: '
print symtab
# print out LITTAB
print 'LITTAB: '
for i in range(len(littab)) :
    print littab[i]
# end sample run



