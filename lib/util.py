import re

def lineProcess(line, reservedWordTable):
    # for each line, check if it is a comment or
    if line.find('.') != -1:
    # get rid of the comment part
        length = line.find('.')
        line = line[:length]

    #get rid of leading/trailing spaces
    instruction = \
            {'label': None, 'operation': None, 'operand':None, 'length':3}
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
def ParseFile( FilePath, OPPath ):
    reservedWordTable = getReservedWordTable(OPPath)

    lines = []

    with open(FilePath, "r") as f:
        lines = f.readlines()

    assembleInstructions = []
    for line in lines:
        line = line.strip()
        if line != "":
            assembleInstructions.append( lineProcess(line, reservedWordTable) )

    return assembleInstructions
