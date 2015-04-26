import re

def formatHexString( hexString ):
    """
        formatHexString( hexString ):->String
        given a HexString, returns a string with prefix '0x'
    """
    if not (hexString[0] == '0' and hexString == 'x'):
        hexString = '0x' + hexString

    return hexString


def lineProcess(line, reservedWordTable, opcodeTable):
    # for each line, check if it is a comment or
    if line.find('.') != -1:
    # get rid of the comment part
        length = line.find('.')
        line = line[:length]

    #get rid of leading/trailing spaces
    instruction = \
            {'label': None, 'operation': None, 'operand':None, 'length':3,\
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
                # no match, return None
                return instruction

            # set to 1 where there's a leading '+' on the operation
            extendedFlag = 0

            firstWordBackup = match.group(0)
            firstWord = firstWordBackup
            if firstWordBackup[0] == '+':
                extendedFlag = 1
                firstWord = firstWord[1:]

            if firstWord in reservedWordTable:
               state = 1 
               instruction['operation'] = firstWord

               # get information of this instruction
               if firstWord in opcodeTable.keys():
                   instruction['format'] = min(opcodeTable[firstWord]['format'])
                   instruction['length'] = instruction['format']
               elif firstWord == 'RESW':
                   instruction['length'] = 3
               elif firstWord == 'RESB':
                   instruction['length'] = 1

               # check if extended later
               if extendedFlag == 1:
                   instruction['length'] = 4
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
        name, opcode, instructionFormat = opcode.split()
        # convert opcode to a format '0x*'
        opcode = hex( int(opcode, 16) )
        instructionFormat = instructionFormat.split('/')
        instructionFormat = [ int(f) for f in instructionFormat ]
        opcodeDict[name] = { 'opcode' : opcode, 'format' : instructionFormat }

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
def ParseFile( FilePath,
               reserveTablePath,
               opcodeTablePath ):
    reservedWordTable = getReservedWordTable( reserveTablePath )
    opcodeTable = getOpcodeTable( opcodeTablePath )

    lines = []

    with open(FilePath, "r") as f:
        lines = f.readlines()

    assembleInstructions = []
    for line in lines:
        line = line.strip()
        if line != "":
            assembleInstructions.append(
                            lineProcess(line, reservedWordTable, opcodeTable) )

    return assembleInstructions

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
    return str(int(string_num.upper(), 16))

