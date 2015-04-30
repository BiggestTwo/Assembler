def buildLiteralValue(literal) :
    literalType = literal[1]
    literalString = literal[3: (len(literal) - 1) ]
    if literalType == 'X' : # hexadecimal
        return literalString
    if literalType == 'C' : # char string
        resultString = ''
        for i in range(len(literalString)) :
            resultString = resultString + str(ord(literalString[i]))
        return resultString
    return '00'
print buildLiteralValue("=X'0F'")