from lib import util
from lib.util import fourBitBin
def assembleFormatFour( opcode,
						operand,
						PC,
						TA,
						XOnly,
						base = None):
	#op n x b p e address
	opcode = util.formatHexString( opcode )
	op1 = fourBitBin(int(opcode[2], 16))[2:]
	op2 = fourBitBin(int(opcode[3], 16))[2:4]
	#
	e = '1'
	b = '0'
	p = '0'
	if len( operand ) > 1:
		x = '1'
	else:
		x = '0'

	n = i = '1'
	# decimal displacement
	address = int(TA, 16)
	address = bin(address)[2:]
	while len(address) < 20:
		address = '0' + address

	objectCode = op1 + op2 + n + i + x + b + p + e + address
	objectCode = hex( int(objectCode, 2) )
	while len(objectCode[2:]) < 8:
		objectCode = '0x' + '0' + objectCode[2:]
	return objectCode

def assembleThreeImmediate(opcode, operand, PC, TA, SYMTAB, XOnly, base = None):
	#op n i x b p e disp
	opcode = util.formatHexString(opcode)
	op1 = fourBitBin(int(opcode[2], 16))[2:]
	op2 = fourBitBin(int(opcode[3], 16))[2:4]
	n = '0'
	i = '1'
	x = '0'
	b = p = e = '0'
	try:
		disp = int(operand[0][1:])
		p = '0'
	except:
		# it is a symbol
		symbolString = operand[0][1:]
		TA = SYMTAB[symbolString]
		disp = int(TA, 16) - int(PC, 16)
		p = '1'

	disp = bin(disp)[2:]
	while len(disp) < 12:
		disp = '0' + disp
	objectCode = op1 + op2 + n + i + x + b + p + e + disp
	return objectCode

def assembleThreePC( opcode, operand, PC, TA, XOnly, base = None ):

	#op n i x b p e disp
	opcode = util.formatHexString( opcode )
	op1 = fourBitBin(int(opcode[2], 16))[2:]
	op2 = fourBitBin(int(opcode[3], 16))[2:4]
	# by default it is PC-relative
	e = '0'
	b = '0'
	p = '1'
	if len( operand ) > 1:
		x = '1'
	else:
		x = '0'
	n = i = '1'

	# decimal displacement
	disp = int(TA, 16) - int(PC, 16)
	if disp < 0:
		# use 2's complement for negative number
		disp = util.towsCompliment(disp, 12)
	else:
		disp = bin(disp)[2:]
		while len(disp) < 12:
			disp = '0' + disp
	objectCode = op1 + op2 + n + i + x + b + p + e + disp
	return objectCode

def assembleFormatThree(opcode, operand, PC, TA, SYMTAB, XOnly, base = None):
	objectCode = None
	if operand[0][0] == '#':
		## immediate addressing
		objectCode = \
			assembleThreeImmediate(opcode, operand, PC, TA, SYMTAB, XOnly, base)
	else:
		objectCode = assembleThreePC(opcode, operand, PC, TA, XOnly, base)

	objectCode = hex(int(objectCode, 2))
	while len(objectCode[2:]) < 6:
		objectCode = '0x' + '0' + objectCode[2:]
	return objectCode

def assembleFormatTwo( opcode,
					   operand,
					   SYMTAB):
	# 2 bytes
	# OP r1 r2
	opcode = util.formatHexString(opcode)
	if len(operand) > 0:
		r1 = operand[0]
		if r1 in SYMTAB.keys():
			r1 = util.formatHexString( SYMTAB[r1] )
	else:
		r1 = hex(0)
	if len(operand) > 1:
		r2 = operand[1]
		if r2 in SYMTAB.keys():
			r2 = util.formatHexString( SYMTAB[r2] )
	else:
		r2 = hex(0)
	objectCode = opcode + r1[2:] + r2[2:]
	return util.formatHexString( objectCode )

def assembleFormatOne( opcode ):
	# 1 byte
	# op
	objectCode = util.formatHexString( opcode )
	return objectCode

def assembleInstructon(	opcode,
						operand,
						operandFormat,
						SYMTAB,
						PC,
						reservedWords,
						XOnly = True,
						Base = None):
    TA = hex(0)
    labelString = checkLabel(operand, reservedWords)
    if (labelString is not None) and (labelString in SYMTAB.keys()):
    	TA = SYMTAB[labelString]

    if operandFormat == 1:
		return assembleFormatOne(opcode)
    elif operandFormat == 2:
		return assembleFormatTwo(opcode, operand, SYMTAB)
    elif operandFormat == 3:
		return assembleFormatThree(opcode, operand, PC, TA, SYMTAB, XOnly, Base)
    elif operandFormat == 4:
		return assembleFormatFour(opcode, operand, PC, TA, XOnly, Base)

def checkLabel( operand, reservedWords):
	""" checkLabel( operand, reservedWords) -> String

		Given operand and a SYMTAB
		find those operands that are symbols
		return symbol or None
	"""
	for op in operand:
		if op not in reservedWords and op[0] != '#':
			return op
	return None

def constructHeaderRecord(ProgramName, StartingAddress, Length):
	"""
	constructHeaderRecord(ProgramName, StartingAddress, Length)->String
	ProgramName : String
	StartingAddress : String (binary string)
	Length : 
	Construt a Header record
	Col. 1 		H
	Col. 2-7	Program Name
	Col. 8-13	Starting address of object program(Hex)
	Col. 14-19	Length of object program in the bytes(Hex)
	"""
	HeaderRecord = 'H'
	while len(programName) < 6:
		programName = programName + ' '

#
#	Parameters
#	@intermediateFile : list of dicts
#	@SYMTAB : Dict, { symbol: address }
#	@OPTAB : Dict, {Operation: OPCODE}
#	@objectProgramPath : String
#
def run(intermediateFile,
		 SYMTAB,
		 objectProgramPath,
		 reservedWords,
		 opcodeTable):
	'''
	run(intermediateFile,
		 SYMTAB,
		 objectProgramPath,
		 reservedWords,
		 opcodeTable)->None
	'''
	records = []
	programName = None
	startingAddress = hex(0)
	if intermediateFile[0]['operation'] == 'START':
		programName = intermediateFile[0]['label']
		startingAddress = util.formatHexString(
											intermediateFile[0]['operand'][0])

	# write Header record to object program
	# initialize first Text record
	# Text record: T starting_address( bits) Length(8 bits) opcode
	
	for index, intermediateCode in enumerate(intermediateFile):
		operation = intermediateCode['operation']

		if operation in opcodeTable.keys():
			opcode = opcodeTable[operation]['opcode']
		else:
			opcode = None

		operand = intermediateCode['operand']
		operandFormat = intermediateCode['format']
		PC = int(intermediateCode['location'], 16) + intermediateCode['length']
		PC = hex(PC)
		XOnly = True
		if opcode is not None and opcodeTable[operation]['note'] != 'X':
			XOnly = False

		if  operation == 'END':
			# end of the file
			break
		objectCode = None
		if opcode is not None:	
			# Assemble the object code
			objectCode = assembleInstructon( opcode,
											operand,
											operandFormat,
											SYMTAB,
											PC,
											reservedWords,
											XOnly )
			print objectCode
		elif opcode is None and (operation == 'BYTE' or operation == 'WORD'):
			# covert constant to object code
			pass


