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
    LOCCTR = [0, 0, 0]
    currBLK = 0 # default block 
    STARTING_ADDRESS = 0
    PROGRAM_LENGTH = 0
    SYMTAB = {}
    BLKASSIGN = {}
    BLKTAB = []
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
    revisedAssemblyCode_BLK1 = []
    revisedAssemblyCode_BLK2 = []
    revisedAssemblyCode_BLK3 = []
    revisedAssemblyCode = [revisedAssemblyCode_BLK1, 
            revisedAssemblyCode_BLK2, revisedAssemblyCode_BLK3]
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
                LOCCTR[currBLK] = STARTING_ADDRESS
                # write line to intermediate file
                i['location'] = None
                revisedAssemblyCode.append(i)
                # read next input line
                continue
            else :
                LOCCTR[currBLK] = 0
        if opcode != 'END' :
            # write line to intermediate file
            i['location'] = util.decToHex(LOCCTR[currBLK])
            revisedAssemblyCode[currBLK].append(i)
            # assign label with memory addr
            if i['label'] != None :
                label = i['label']
                # search SYMTAB for LABEL
                if SYMTAB.has_key(label) :
                    # set error flag
                    ERROR = 1
                else :
                    SYMTAB[label] = util.decToHex(LOCCTR[currBLK])
                    BLKASSIGN[label] = currBLK
            # search OPTAB for opcode
            # symbol defining
            if opcode == 'EQU' :
                # put the label into SYMTAB with its operand as value (immediate addressing)
                resultOfExpression = parseExpression(operand[0], SYMTAB, LOCCTR[currBLK])
                SYMTAB[i['label']] = resultOfExpression
            # literal
            if opcode == 'LTORG' :
                # populate all literals up to now
                for counter in range(len(LITTAB)) :
                    currLiteral = LITTAB[counter]
                    if currLiteral['location'] == None : # not yet assigned
                        currLiteral['location'] = util.decToHex(LOCCTR[currBLK])
                        LOCCTR[currBLK] += currLiteral['length']
                        # write into intermediate file
                        newLine = {}
                        newLine['format'] = 3
                        newLine['label'] = None
                        newLine['length'] = currLiteral['length']
                        newLine['location'] = currLiteral['location']
                        newLine['operation'] = currLiteral['name']
                        newLine['operand'] = None
                        revisedAssemblyCode[currBLK].append(newLine)
            # program block directives
            if opcode == 'USE' :
                # default block
                if operand == None :
                    currBLK = 0
                # CDATA
                elif operand[0] == 'CDATA' :
                    currBLK = 1
                # CBLKS
                elif operand[0] == 'CBLKS' :
                    currBLK = 2
                continue
            # normal condition
            if OPTAB.has_key(opcode) :
                LOCCTR[currBLK] += i['length']
            elif opcode == 'WORD' :
                LOCCTR[currBLK] += 3
            elif opcode == 'RESW' :
                LOCCTR[currBLK] += 3 * int(i['operand'][0])
            elif opcode == 'RESB' :
                LOCCTR[currBLK] += int(i['operand'][0])
            elif opcode == 'BYTE' :
                LOCCTR[currBLK] += util.lengthOfVariable(i['operand'][0])
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
            i['location'] = util.decToHex(LOCCTR[currBLK])
            revisedAssemblyCode[currBLK].append(i)
            # populate LITTAB
            for counter in range(len(LITTAB)) :
                currLiteral = LITTAB[counter]
                if currLiteral['location'] == None : # not yet assigned
                    currLiteral['location'] = util.decToHex(LOCCTR[currBLK])
                    LOCCTR[currBLK] += currLiteral['length']
                    # write into intermediate file
                    newLine = {}
                    newLine['format'] = 3
                    newLine['label'] = None
                    newLine['length'] = currLiteral['length']
                    newLine['location'] = currLiteral['location']
                    newLine['operation'] = currLiteral['name']
                    newLine['operand'] = None
                    revisedAssemblyCode[currBLK].append(newLine)
            # calculate length of each program block (block number, starting_addr, length)
            # default block
            newDict = {}
            newDict['blockNumber'] = 0
            newDict['address'] = str(STARTING_ADDRESS)
            newDict['length'] = util.decToHex(LOCCTR[0])
            BLKTAB.append(newDict)
            # CDATA
            newDict = {}
            newDict['blockNumber'] = 1
            newDict['address'] = util.decToHex( 
                int(util.hexToDec(str(STARTING_ADDRESS) ) ) + LOCCTR[0] )
            newDict['length'] = util.decToHex(LOCCTR[1])
            BLKTAB.append(newDict)
            # CBLKS
            newDict = {}
            newDict['blockNumber'] = 2
            newDict['address'] = util.decToHex( 
                int(util.hexToDec(str(STARTING_ADDRESS) ) ) + LOCCTR[0] + LOCCTR[1])
            newDict['length'] = util.decToHex(LOCCTR[2])
            BLKTAB.append(newDict)

            # re-assign address to symbols in SYMTAB
            # new address should be relative to the start of the whole program
            # (instead of relative to the start of its program block)
            for symbol, address in SYMTAB.items() :
                # find its block
                blockNumber = BLKASSIGN[symbol]
                # calculate (new address = former address + start of its block)
                newLocation = address + BLKTAB[blockNumber]['address']
            # re-assign addresses to lines in each block
            # CDATA
            for line in range(len(revisedAssemblyCode[1])) :
                # new addr = curr addr + length of default block
                lengthOfDefault = BLKTAB[0]['length']
                currAddr = util.hexToDec(revisedAssemblyCode[1][line]['location'])
                newAddr = int(currAddr) + int(util.hexToDec(lengthOfDefault))
                newAddr = util.decToHex(int(newAddr) )
                revisedAssemblyCode[1][line]['location'] = newAddr
            # CBLKS
            for line in range(len(revisedAssemblyCode[2])) :
                # new addr = curr addr + length of default block
                lengthOfDefault = BLKTAB[0]['length']
                lengthOfCDATA = BLKTAB[1]['length']
                currAddr = util.hexToDec(revisedAssemblyCode[2][line]['location'])
                newAddr = int(currAddr) + int(util.hexToDec(lengthOfDefault)) \
                            + int(util.hexToDec(lengthOfCDATA))
                newAddr = util.decToHex(int(newAddr) )
                revisedAssemblyCode[2][line]['location'] = newAddr
            # merge assembly code together
            mergedAssemblyCode = []
            # default
            for line in range(len(revisedAssemblyCode[0])) :
                mergedAssemblyCode.append(revisedAssemblyCode[0][line])
            # CDATA
            for line in range(len(revisedAssemblyCode[1])) :
                mergedAssemblyCode.append(revisedAssemblyCode[1][line])
            # CBLKS
            for line in range(len(revisedAssemblyCode[2])) :
                mergedAssemblyCode.append(revisedAssemblyCode[2][line])
            # save (LOCCTR[2] - starting address) as program length
            PROGRAM_LENGTH = LOCCTR[2] - STARTING_ADDRESS
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
    result['intermediate'] = mergedAssemblyCode
    result['SYMTAB'] = SYMTAB
    result['LITTAB'] = LITTAB
    return result

# sample run
fileName = 'prog_blocks.txt'
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



