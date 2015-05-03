import re

def towsCompliment(num, length):
    '''
    towsCompliment(num, length)->str
    '''
    if num > 0:
        pass
    else:
        num = -num
        num = bin(num)[2:]
        while len(num) < length:
            num = '0' + num

        num = list(num)
        # reverse
        for index, value in enumerate(num):
            if value == '0':
                num[index] = '1'
            else:
                num[index] = '0'

        # add 1
        flag = 1
        index = length - 1
        while index > 0:
            b = int(num[index])
            b = b + flag
            if b >= 2:
                flag = 1
                b = 0
            else:
                flag = 0
            num[index] = str(b)
            index = index - 1

    result = ''
    for x in num:
        result = result + x
    return result

def fourBitBin(x):
    """
        fourBitBin(x)->String
        given a decimal number(0-16), returns a four-bit binnary number.
        fourBitBin(1) -> "0b0001"
    """
    result = bin(x)
    result = result[2:]
    while len(result) % 4 != 0:
        result = '0' + result

    result = '0b' + result
    return result

def formatHexString( hexString ):
    """
        formatHexString( hexString ):->String
        given a HexString, returns a string with prefix '0x'
    """
    if len(hexString) < 2 or not (hexString[0] == '0' and hexString[1] == 'x'):
        hexString = '0x' + hexString

    return hexString

def formatBinString(binString):
    """
    formatBinString(binString)->String
    given a binary string, returns another one with leading '0b'
    """
    if len(binString) < 2 or not(binString[0] == '0' and binString[1] == 'b' ):
        binString = '0b' + binString

    return binString


def lineProcess(line, reservedWordTable, opcodeTable, MACROLabels):
    # for each line, check if it is a comment or
    if line.find('.') != -1:
    # get rid of the comment part
        length = line.find('.')
        line = line[:length]

    if len(line) <= 0:
        return None

    #get rid of leading/trailing spaces
    instruction = \
            {'label': None, 'operation': None, 'operand':None, 'length':0,\
             'format':3}
    state = 0
    wordPattern = r'\S+'
    while True:
        # get rid of extra spaces
        line = line.strip()
        # get the first non-blank word from the line
        if state == 0:
            match = re.match(wordPattern, line)
            if match is None:
                # no single word found, return None
                return None

            # set to 1 where there's a leading '+' on the operation
            extendedFlag = 0

            firstWordBackup = match.group(0)
            firstWord = firstWordBackup
            if firstWordBackup[0] == '+':
                extendedFlag = 1
                firstWord = firstWord[1:]

            if firstWord in reservedWordTable or firstWord in MACROLabels:
               state = 1 
               instruction['operation'] = firstWord

               # get information of this instruction
               if firstWord in opcodeTable.keys():
                   instruction['format'] = min(opcodeTable[firstWord]['format'])
                   instruction['length'] = instruction['format']

               # check if extended later
               if extendedFlag == 1:
                   instruction['length'] = 4
                   instruction['format'] = 4
            else:
                # there is a label
                instruction['label'] = firstWordBackup

            line = line[len(firstWordBackup):]
            continue

        if state == 1:
            operandPattern = r'((\S+\s*,\s*\S+)|(\S+))'
            match = re.match(operandPattern, line)
            if match is not None:
                # there is operand
                instruction['operand'] = match.group(0).split(',')
                removeSpaces = lambda x: x.strip()
                instruction['operand'] = \
                                    map(removeSpaces, instruction['operand'])
            state = 2

            if instruction['operation'] == 'RESW':
               instruction['length'] = 3 * int(instruction['operand'][0])
            if instruction['operation'] == 'RESB':
               instruction['length'] = 1 * int(instruction['operand'][0])

        if state == 2:
            # final state, resturn result
            return instruction

def getOpcodeTable( filePath ):
    """
    getOpcodeTable( filePath )->list
    """
    opcodeLines = []
    opcodeDict = {}
    with open( filePath, "r" ) as f:
        opcodeLines = f.readlines()
    for opcode in opcodeLines:
        opcode = opcode.strip()
        splitResult = opcode.split()
        name = splitResult[0]
        opcode = splitResult[1]
        instructionFormat = splitResult[2]
        if len(splitResult) > 3:
            note = splitResult[3]
        else:
            note = None
        # convert opcode to a format '0x*'
        opcode = hex( int(opcode, 16) )
        while len(opcode[2:]) < 2:
            opcode = '0x' + '0' + opcode[2:]
        instructionFormat = instructionFormat.split('/')
        instructionFormat = [ int(f) for f in instructionFormat ]
        opcodeDict[name] = { 'opcode' : opcode,
                             'format' : instructionFormat,
                             'note' : note}

    return opcodeDict

def getReservedWordTable( filePath ):
    lines = []
    with open(filePath, "r") as f:
        lines = f.readlines()

    operations = []
    for line in lines:
        words = line.strip()
        words = line.split()
        for word in words:
            if word != " ":
                operations.append( word )

    return operations


#   Parse a origin amssble file
#   @FilePath - the path of file
#   return - A parse array of assemble instructions
def ParseLine(line,
            reservedWordTable,
            opcodeTable,
            MACROLabels = []):
    '''
    ParseLine(line, reservedWordTable, opcodeTable, MACROLabels)->Dict
    '''
    assembleInstruction = None
    line = line.strip()
    if line != "":
        assembleInstruction = lineProcess(line,
                                        reservedWordTable,
                                        opcodeTable,
                                        MACROLabels)

    return assembleInstruction

# conversion functions between hex and dec
def decToHex(string_num):
    base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]
    num = int(string_num)
    if num == 0 :
        return '0'
    result = ''
    mid = []
    while True:
        if num == 0 :
            break
        num,rem = divmod(num, 16)
        mid.append(base[rem])
    for i in range(len(mid)) :
        result = result + mid[len(mid) - i - 1]
    return result
def hexToDec(string_num):
    return str(int(string_num, 16))

# literal processing functions

# return true if operand is in literal format
def isLiteral(operand) :
    if operand == None :
        return False
    if operand[0][0] == '=' :
        return True
    else :
        return False

# return the length of a literal value (in bytes)
def lengthOfLiteral(literal) :
    litLength = 0
    litType = literal[1]
    if litType == 'C' :
        litLength = len(literal) - 4
    if litType == 'X' :
        litLength = (len(literal) - 4) / 2
    return litLength
# return the length of a literal value (in bytes)
def lengthOfVariable(variable) :
    varLength = 0
    varType = variable[0]
    if varType == 'C' :
        varLength = len(variable) - 3
    if varType == 'X' :
        varLength = (len(variable) - 3) / 2
    return varLength

# build literal value
# case 1) hexidecimal : directly output the literal value
# case 2) character   : convert in to ascii code then output
def buildLiteralValue(literal) :
    literalType = literal[1]
    literalString = literal[3: (len(literal) - 1) ]
    if literalType == 'X' : # hexadecimal
        return literalString
    if literalType == 'C' : # char string
        resultString = ''
        for i in range(len(literalString)) :
            resultString = resultString + decToHex(str(ord(literalString[i])))
        return resultString
    return '00'
