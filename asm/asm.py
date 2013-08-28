import sys

from pyparsing import *

import tokens



def bin_str(n, bits=0):
	s = ""
	while n:
		s = ("1" if n & 1 else "0") + s
		n >>= 1
	return s.zfill(bits)


def grammer():
	def convert_signed(base, bits):
		def convert(s, loc, toks):
			val = "".join(toks)
			#if val == "-": return -1
			n = int(val, base)
			if base == 10:
				if -2**(bits-1) <= n and n <= 2**(bits-1)-1:
					return [tokens.Number(n, base, bits, signed=True)]
			elif n < 2**bits:
				return [tokens.Number(n, base, bits, signed=True)]
			raise ParseFatalException(s, loc,
				"%s out of bounds for a %d bit signed number in base %d" % (val, bits, base))
		return convert
	
	def convert_unsigned(base, bits):
		def convert(s, loc, toks):
			n = int("".join(toks), base)
			if 0 <= n and n < 2**bits:
				return [tokens.Number(n, base, bits, signed=False)]
			raise ParseFatalException(s, loc,
				"%s out of bounds for a %d bit unsigned number in base %d" % (val, bits, base))
		return convert

	to_int = lambda s,l,t: int("".join(t))
	def replace(what):
		return lambda s,l,t: [what] + t[1:]

	# puncuation
	comma = Suppress(",")
	colon = Suppress(":")
	lparen = Suppress("(")
	rparen = Suppress(")")

	# values
	reg = Literal("$").suppress() + Word("01234567")
	reg.setName("register")
	reg.setParseAction(tokens.Register)
	num = Word(nums).setParseAction(to_int)
	label_name = (num + Optional(Word("fb", exact=1))) | Word(alphanums)
	label_name.setName("label")
	label_name.setParseAction(tokens.Label)
	label = label_name + colon
	sign = Optional(Word("-+", exact=1))
	spec_imm = sign + Word("1248", exact=1)
	spec_imm.setParseAction(tokens.Immediate)
	reg_imm = reg | spec_imm
	reg3_imm = reg + comma + reg + comma + reg_imm
	reg3 = reg + comma + reg + comma + reg
	comment = ";" + restOfLine
	condition = oneOf("eq ne gt gte lt lte ult ulte")
	condition.setParseAction(tokens.Condition)

	def signed_num(bits):
		bin = Suppress("b") + Word("01")
		oct = sign + Word("0", nums)
		dec = sign + Word("123456789", nums)
		hex = Suppress("0x") + Word(srange("[0-9a-fA-F]"))
		bin.setParseAction(convert_signed(2, bits))
		oct.setParseAction(convert_signed(8, bits))
		dec.setParseAction(convert_signed(10, bits))
		hex.setParseAction(convert_signed(16, bits))
		return NoMatch().setName("%d-bit signed number" % bits) | (bin ^ oct ^ dec ^ hex)

	def unsigned_num(bits):
		bin = Suppress("b") + Word("01")
		oct = Word("0", nums)
		dec = Word("123456789", nums)
		hex = Suppress("0x") + Word(srange("[0-9a-fA-F]"))
		bin.setParseAction(convert_unsigned(2, bits))
		oct.setParseAction(convert_unsigned(8, bits))
		dec.setParseAction(convert_unsigned(10, bits))
		hex.setParseAction(convert_unsigned(16, bits))
		return NoMatch().setName("%d-bit signed number" % bits) | (bin ^ oct ^ dec ^ hex)

	# numbers
	s7 = signed_num(7)
	s8 = signed_num(8)
	s13 = signed_num(13)
	u4 = unsigned_num(4)

	# instructions
	ldw = Literal("ldw") + reg + comma + (s7 | reg) + lparen + reg + rparen
	ldb = Literal("ldb") + reg + comma + (s7 | reg) + lparen + reg + rparen
	stw = Literal("stw") + (s7 | reg) + lparen + reg + rparen + comma + reg
	stb = Literal("stb") + (s7 | reg) + lparen + reg + rparen + comma + reg

	jmp = Literal("jmp") + (s13 ^ label_name ^ reg)
	
	add = Literal("add") + reg3_imm
	sub = Literal("sub") + reg3_imm
	and_i = Literal("and") + reg3_imm
	or_i = Literal("or") + reg3_imm
	addskipz = Literal("as.z") + reg3_imm
	addskipnz = Literal("as.nz") + reg3_imm

	skip = Literal("s") + Suppress(".") + condition + reg + comma + reg_imm

	lui = Literal("lui") + reg + comma + s8
	addi = Literal("addi") + reg + comma + s8

	shl = Literal("shl") + reg + comma + reg + comma + u4
	shr = Literal("shr") + reg + comma + reg + comma + u4

	xor = Literal("xor") + reg + comma + reg
	not_i = Literal("not") + reg + comma + reg

	halt = Literal("halt")
	trap = Literal("trap") + u4
	sext = Literal("sext") + reg

	instruction = ldw | ldb | stw | stb | jmp | add | sub | and_i | or_i | skip | addskipz
	instruction |= addskipnz | lui | addi | shl | shr | xor | not_i | halt | trap | sext
	instruction.setParseAction(tokens.Instruction)
	line = Optional(label) + instruction
	g = OneOrMore(line)
	g.ignore(comment)
	return g


def parse(filename):
	toks = None
	g = grammer()
	try:
		toks = g.parseFile(filename, parseAll=True)
	except (ParseException, ParseFatalException), err:
		print err.line
		print " "*(err.column-1) + "^"
		print err
	return toks


def expand_labels(toks):
	labels = {}

	def add_label(label, pos):
		label.pos = pos
		if label.name not in labels:
			labels[label.name] = []
		labels[label.name].append(label)

	def lookup_label(label, pos):
		if label.name not in labels:
			raise Exception("Unknown label %s" % repr(label.name))
		search = labels[label.name]
		if len(search) == 1:
			found = search[0]
		else:
			if label.direction == "f":
				found = [l for l in search if l.pos > pos][0]
			elif label.direction == "b":
				found = [l for l in search if l.pos <= pos][-1]
		# TODO check that delta is in bounds for a 13 bit signed number
		delta = found.pos - pos
		return tokens.Number(delta, base=10, bits=13, signed=True)


	i = 0
	while i < len(toks):
		tok = toks[i]
		if isinstance(tok, tokens.Label):
			add_label(tok, i*2)
			del toks[i]
			continue
		i += 1
	
	for i, tok in enumerate(toks):
		for j, arg in enumerate(tok.args):
			if isinstance(arg, tokens.Label):
				tok.args[j] = lookup_label(arg, i*2)

	return toks


def set_imm(inst, byte):
	if isinstance(inst.args[2], tokens.Immediate):
		byte |= 1 << 9
	return byte

instructions = {
	"ldw":		(  0 << 13, 0, 6, 3),
	"ldb":		(  1 << 13, 0, 6, 3),
	"stw":		(  2 << 13, 6, 3, 0),
	"stb":		(  3 << 13, 6, 3, 0),
	"jmp":		(  4 << 13, 0),
	"add":		( 40 << 10, 0, 6, 3),
	"sub":		( 41 << 10, 0, 6, 3),
	"and":		( 42 << 10, 0, 6, 3),
	"or":		( 43 << 10, 0, 6, 3),
	"s":		( 44 << 10, 0, 6, 3),
	"as.z":		( 45 << 10, 0, 6, 3),
	"as.nz":	( 46 << 10, 0, 6, 3),
	"lui":		( 24 << 11, 0, 3),
	"addi":		( 25 << 11, 0, 3),
	"ldw.b":	(104 <<  9, 0, 3, 6),
	"ldb.b":	(105 <<  9, 0, 3, 6),
	"stw.b":	(106 <<  9, 3, 6, 0),
	"stb.b":	(107 <<  9, 3, 6, 0),
	"shl":		( 54 << 10, 0, 3, 6),
	"shr":		( 55 << 10, 0, 3, 6),
	"xor":		(896 <<  6, 0, 3),
	"not":		(897 <<  6, 0, 3),
	"halt":		(65246, ),
	"trap":		(4078 << 4, 0),
	"sext":		(4079 << 4, 0),
	"jmp.r":	(8159 << 3, 0),
}

extra = {
	"add":   set_imm,
	"sub":   set_imm,
	"and":   set_imm,
	"or":    set_imm,
	"s":     set_imm,
	"as.z":  set_imm,
	"as.nz": set_imm,
}

def translate(toks):
	bytes = []
	for token in toks:
		inst = instructions[token.name]
		byte = inst[0]
		for i, n in enumerate(inst[1:]):
			byte |= token.args[i].binary() << n
		if token.name in extra:
			byte = extra[token.name](token, byte)
		bytes.append(byte)
	return bytes


def main(args):
	if len(args) != 2:
		print "USAGE: asm source.asm output.o"
		return 2
	in_filename  = args[0]
	out_filename = args[1]
	toks = parse(in_filename)
	if not toks:
		return 1
	toks = expand_labels(toks)
	bytes = translate(toks)
	#for tok in toks:
	#	print tok
	#return 1
	#print map(lambda b: bin_str(b, 16), bytes)
	fout = open(out_filename, "w")
	for byte in bytes:
		fout.write(bin_str(byte, 16) + "\n")

if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
