from lib import util
from lib.util import fourBitBin
def assembleFormatFour( opcode,
						operand,
						PC,
						TA):
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
	if operand is not None:
		if len(operand[0]) > 2 and operand[0][0] == '#':
			n = '0'
			i = '1'
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

def assembleThreeImmediate(opcode, operand, PC, TA, SYMTAB, base = None):
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

def assembleThreePC( opcode, operand, PC, TA):

	#op n i x b p e disp
	opcode = util.formatHexString( opcode )
	op1 = fourBitBin(int(opcode[2], 16))[2:]
	op2 = fourBitBin(int(opcode[3], 16))[2:4]
	# by default it is PC-relative
	e = '0'
	b = '0'
	p = '1'
	if operand is not None and len( operand ) > 1:
		x = '1'
	else:
		x = '0'
	n = i = '1'

	if operand is not None and operand[0][0] == '@':
		# indirect addressing
		n = '1'
		i = '0'

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

def assembleThreeBase(opcode, operand, PC, TA, SYMTAB):
	# op n i x b p e disp
	opcode = util.formatHexString( opcode )
	op1 = fourBitBin(int(opcode[2], 16))[2:]
	op2 = fourBitBin(int(opcode[3], 16))[2:4]
	e = '0'
	b = '1'
	p = '0'
	# check for indexing addressing
	if operand is not None and len( operand ) > 1:
		x = '1'
	else:
		x = '0'
	n = i = '1'
	# check for indrect
	if operand is not None and operand[0][0] == '@':
		# indirect addressing
		n = '1'
		i = '0'	
	# decimal displacement
	if 'BASE' in SYMTAB:
		baseValue = SYMTAB['BASE']
	disp = int(TA, 16) - int(baseValue, 16)
	if disp < 0:
		# use 2's complement for negative number
		disp = util.towsCompliment(disp, 12)
	else:
		disp = bin(disp)[2:]
		while len(disp) < 12:
			disp = '0' + disp
	objectCode = op1 + op2 + n + i + x + b + p + e + disp
	return objectCode

def assembleThreeNoOperand(opcode):
	# op n i x b p e disp
	opcode = util.formatHexString( opcode )
	op1 = fourBitBin(int(opcode[2], 16))[2:]
	op2 = fourBitBin(int(opcode[3], 16))[2:4]
	e = '0'
	b = '0'
	p = '0'
	n = i = '1'
	x = '0'
	disp = '0' * 12
	objectCode = op1 + op2 + n + i + x + b + p + e + disp
	return objectCode

def assembleFormatThree(opcode, operand, PC, TA, SYMTAB):
	objectCode = None
	if operand is not None and operand[0][0] == '#':
		## immediate addressing
		objectCode = \
			assembleThreeImmediate(opcode, operand, PC, TA, SYMTAB )
	elif operand is None:
		# e.x., RSUB
		objectCode = assembleThreeNoOperand(opcode)
	else:
		disp = int(TA, 16) - int(PC, 16)
		if disp < -2048:
			# base relative needed
			objectCode = assembleThreeBase(opcode, operand, PC, TA, SYMTAB)
		else:
			objectCode = assembleThreePC(opcode, operand, PC, TA)

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

def calculateTargetAddress(operand, SYMTAB, reservedWords, LITTAB):
	"""
	calculateTargetAddress(operand, SYMTAB, reservedWords)->String
	calculate the TA of an Instruction, hexadecimal string
	"""
	TA = hex(0)
	labelString = checkLabel(operand, reservedWords)
	if labelString is not None:
		if labelString in SYMTAB.keys():
			# This is a defined label
			TA = SYMTAB[labelString]
		elif labelString[0] == '#':
			# immediate addressing
			try:
				# e.x., #0
				TA = int(labelString[1:])
				TA = hex(TA)
			except:
				# e.x., #LENGTH
				if labelString[1:] in SYMTAB.keys():
					TA = SYMTAB[labelString[1:]]
		elif len(labelString) >= 4 and labelString[0] == '=':
			# literal
			for literal in LITTAB:
				if literal['name'] == labelString:
					TA = literal['location']
					break

		elif len(labelString) >= 2 and labelString[0] == '@':
			# indirect addressing
			if labelString[1:] in SYMTAB.keys():
				TA = SYMTAB[labelString[1:]]

	return TA

def assembleInstructon(	opcode,
						operand,
						operandFormat,
						SYMTAB,
						PC,
						reservedWords,
						LITTAB):	
    TA = hex(0)
    TA = calculateTargetAddress(operand, SYMTAB, reservedWords, LITTAB)

    if operandFormat == 1:
		return assembleFormatOne(opcode)
    elif operandFormat == 2:
		return assembleFormatTwo(opcode, operand, SYMTAB)
    elif operandFormat == 3:
		return assembleFormatThree(opcode, operand, PC, TA, SYMTAB)
    elif operandFormat == 4:
		return assembleFormatFour(opcode, operand, PC, TA)

def checkLabel( operand, reservedWords):
	""" checkLabel( operand, reservedWords) -> String

		Given operand and a SYMTAB
		find those operands that are symbols
		return symbol or None
	"""
	if operand is None:
		return None
	for op in operand:
		if op not in reservedWords: 
			return op
	return None

def constructHeaderRecord(programName, startingAddress, Length):
	"""
	constructHeaderRecord(ProgramName, StartingAddress, Length)->String
	ProgramName : String
	StartingAddress : String (Hex string)
	Length : int
	Construt a Header record
	Col. 1 		H
	Col. 2-7	Program Name
	Col. 8-13	Starting address of object program(Hex)
	Col. 14-19	Length of object program in the bytes(Hex)
	"""
	HeaderRecord = 'H'
	if programName is None:
		programName = ''
	while len(programName) < 6:
		programName = programName + ' '

	startingAddress = util.formatHexString(startingAddress)[2:]
	while len(startingAddress) < 6:
		startingAddress = '0' + startingAddress

	Length = hex(Length)[2:]
	while len(Length) < 6:
		Length = '0' + Length

	HeaderRecord = 'H' + programName + startingAddress + Length
	return HeaderRecord

def constructEndRecord(intermediateFile):
	"""
	constructEndRecord(intermediate)->String
	Col. 1		E
	Col. 2-7	Address of first executable instruction in object program
				(hexadecimal)
	"""
	address = None
	for item in intermediateFile:
		if 'objectCode' in item and item['objectCode'] is not None:
			address = util.formatHexString(item['location'])[2:]
			while len(address) < 6:
				address = '0' + address
			break

	endRecord = 'E' + address
	return endRecord


def assembleTextRecord(textRecordStartingAddress, textRecordObjectCode):
	"""
	assembleTextRecord(textRecordStartingAddress, textRecordObjectCode)->String
	return a signle text Record
	"""
	if textRecordStartingAddress is None or textRecordObjectCode is None:
		return None

	textRecord = 'T'
	while len(textRecordStartingAddress) < 6:
		textRecordStartingAddress = '0' + textRecordStartingAddress
	textRecord = textRecord + textRecordStartingAddress
	recordLength = int(len( textRecordObjectCode ) / 2)
	recordLength = hex(recordLength)[2:]
	if len(recordLength) < 2:
		recordLength = '0' + recordLength
	textRecord = textRecord + recordLength
	textRecord = textRecord + textRecordObjectCode
	return textRecord


def constructTextRecord( intermediateFile ):
	"""
	constructTextRecord( intermediateFile )->list
	Col. 1 		T
	Col. 2-7	Starting address for object code in the record(Hex)
	Col. 8-9	Length of object code in this record in bytes(hexadecimal)
	Col. 10-69	Object code, represented in hexadecimal(2 columns per byte)
	"""
	textRecordObjectCodeLength = 60
	textRecords = []
	textRecordStartingAddress = None
	textRecordObjectCode = None

	for item in intermediateFile:
		# for RESW or RESB
		if item['operation'] == 'RESW' or item['operation'] == 'RESB':
			# create a new Text record to none
			textRecord = \
			 assembleTextRecord(textRecordStartingAddress, textRecordObjectCode)

			if textRecord is not None:
				textRecords.append( textRecord )

			textRecordStartingAddress = None
			textRecordObjectCode = None
			continue

		# for other instructions
		if not('objectCode' in item.keys() and item['objectCode'] is not None):
			continue
		# put object code into textRecord
		elif textRecordStartingAddress is None:
			# create a new Text record
			textRecordStartingAddress = item['location']
			textRecordObjectCode = item['objectCode'][2:]
		elif (len(textRecordObjectCode) + item['length'] * 2) > \
													textRecordObjectCodeLength:
			# object code will not fit into the current text record
			# assemble This text record
			textRecord = \
			 assembleTextRecord(textRecordStartingAddress, textRecordObjectCode)

			textRecords.append( textRecord )
			textRecordStartingAddress = item['location']
			textRecordObjectCode = item['objectCode'][2:]
		else:
			textRecordObjectCode = textRecordObjectCode + item['objectCode'][2:]

	textRecord = \
	 assembleTextRecord(textRecordStartingAddress, textRecordObjectCode)

	if textRecord is not None:
		textRecords.append( textRecord )
	return textRecords
			

def getObjectCode(intermediateFile,
				 SYMTAB,
				 reservedWords,
				 opcodeTable,
				 LITTAB):
	for index, intermediateCode in enumerate(intermediateFile):
		operation = intermediateCode['operation']
		if operation == 'START':
			continue

		if operation == 'BASE':
			# sotre the value of the base
			operand = intermediateCode['operand'][0]
			if operand in SYMTAB.keys():
				SYMTAB['BASE'] = SYMTAB[operand]
			else:
				# set an error
				pass

		if operation in opcodeTable.keys():
			opcode = opcodeTable[operation]['opcode']
		else:
			opcode = None

		operand = intermediateCode['operand']
		operandFormat = intermediateCode['format']
		PC = int(intermediateCode['location'], 16) + intermediateCode['length']
		PC = hex(PC)

		if  operation == 'END':
			# end of the file
			continue
		objectCode = None
		if opcode is not None:	
			# Assemble the object code
			objectCode = assembleInstructon( opcode,
											operand,
											operandFormat,
											SYMTAB,
											PC,
											reservedWords,
											LITTAB)
		elif opcode is None and operation == 'BYTE':
			# covert constant to object code
			op = operand[0]
			objectCode = None
			try:
				op = int(op)
				objectCode = hex(op)[2:]
			except:
				# Hex character , e.g. X'05'
				objectCode = op[2:4]

		elif opcode is None and operation == 'WORD':
			op = operand[0]
			objectCode = None
			try:
				op = int(op)
				objectCode = hex(op)[2:]
			except:
				# Hex characters, e.g. X'05'
				objectCode = op[2:len(op)-1]

		elif operation is not None and \
									len(operation) >= 4 and operation[0] == '=':
			# for literal generation
			# find the value from the LITTAB table
			for literal in LITTAB:
				if literal['name'] == operation:
					objectCode = literal['value']
					break

		if objectCode is not None:
			objectCode = util.formatHexString(objectCode)
			print objectCode.upper()[2:]
		intermediateFile[index]['objectCode'] = objectCode

	return intermediateFile
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
		 opcodeTable,
		 LITTAB = None):
	'''
	run(intermediateFile,
		 SYMTAB,
		 objectProgramPath,
		 reservedWords,
		 opcodeTable)->None
	'''
	records = []
	programName = ''
	startingAddress = hex(0)
	programLength = 0
	if intermediateFile[0]['operation'] == 'START':
		programName = intermediateFile[0]['label']
		startingAddress = util.formatHexString(
											intermediateFile[0]['operand'][0])

	endingAddress = 0
	if intermediateFile[-1]['operation'] == 'END':
		endingAddress = int(intermediateFile[-1]['location'], 16)
	else:
		endingAddress = int(intermediateFile[-1]['location'], 16) + \
						intermediateFile[-1]['length']

	programLength = endingAddress - int(startingAddress, 16)
	records.append(
			constructHeaderRecord(programName, startingAddress, programLength))
	# write Header record to object program
	# initialize first Text record
	# Text record: T starting_address( bits) Length(8 bits) opcode
	
	intermediateFile = getObjectCode(intermediateFile,
									SYMTAB,
									reservedWords,
									opcodeTable,
									LITTAB)

	textRecords = constructTextRecord(intermediateFile)
	records = records + textRecords
	endRecord = constructEndRecord(intermediateFile)
	records = records + [endRecord]
	return records
