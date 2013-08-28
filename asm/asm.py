import sys

from pyparsing import *


class Label(object):
	def __init__(self, tokens):
		self.name = tokens[0]
		self.direction = tokens[1] if len(tokens) == 2 else None
		self.pos = -1
	
	def __str__(self):
		if self.direction:
			return "<Label %s %s>" % (repr(self.name), self.direction)
		elif self.pos >= 0:
			return "<Label %s @%d>" % (repr(self.name), self.pos)
		return "<Label %s>" % repr(self.name)
	__repr__ = __str__


class Inst(object):
	def __init__(self, tokens):
		self.name = tokens[0]
		self.args = tokens[1:]

		# internal translations
		is_reg = lambda i: isinstance(self.args[i], Register)
		if self.name in ("ldw", "ldb") and is_reg(1):
			self.name += ".b"
		elif self.name in ("stw", "stb") and is_reg(0):
			self.name += ".b"
		elif self.name == "jmp" and is_reg(0):
			self.name += ".r"
	
	def __str__(self):
		return "<Inst %s %s>" % (self.name, ", ".join(map(repr, self.args)))
	__repr__ = __str__


class Number(object):
	def __init__(self, n, base, bits, signed):
		self.n = n
		self.base = base
		self.bits = bits
		self.signed = signed
	
	def binary(self):
		if self.signed and self.n < 0:
			# two's complement by subtracting from 2^n
			m = 2 ** self.bits
			return m + self.n
		return self.n
	
	def __str__(self):
		signed = "s" if self.signed else "u"
		return "<Number %d %s>" % (self.n, signed)
	__repr__ = __str__


class Register(object):
	def __init__(self, tokens):
		self.name = int(tokens[0])
	
	def binary(self):
		return self.name
	
	def __str__(self):
		return "<Reg %s>" % repr(self.name)
	__repr__ = __str__


class Immediate(object):
	def __init__(self, tokens):
		self.value = int("".join(tokens))
	
	def binary(self):
		m = {8: 0, 4: 1, 2: 2, 1: 3, -1: 4, -2: 5, -4: 6, -8: 7}
		return m[self.value]

	def __str__(self):
		return "<Imm %d>" % self.value
	__repr__ = __str__


class Condition(object):
	def __init__(self, tokens):
		self.type = tokens[0]
	
	def binary(self):
		m = {"eq": 0, "ne": 1, "gt": 2, "gte": 3, "lt": 4, "lte":5, "ult": 6, "ulte": 7}
		return m[self.type]

	def __str__(self):
		return "<Cond %s>" % self.type
	__repr__ = __str__


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
					return [Number(n, base, bits, signed=True)]
			elif n < 2**bits:
				return [Number(n, base, bits, signed=True)]
			raise ParseFatalException(s, loc,
				"%s out of bounds for a %d bit signed number in base %d" % (val, bits, base))
		return convert
	
	def convert_unsigned(base, bits):
		def convert(s, loc, toks):
			n = int("".join(toks), base)
			if 0 <= n and n < 2**bits:
				return [Number(n, base, bits, signed=False)]
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
	reg.setParseAction(Register)
	num = Word(nums).setParseAction(to_int)
	label_name = (num + Optional(Word("fb", exact=1))) | Word(alphanums)
	label_name.setName("label")
	label_name.setParseAction(Label)
	label = label_name + colon
	sign = Optional(Word("-+", exact=1))
	spec_imm = sign + Word("1248", exact=1)
	spec_imm.setParseAction(Immediate)
	reg_imm = reg | spec_imm
	reg3_imm = reg + comma + reg + comma + reg_imm
	reg3 = reg + comma + reg + comma + reg
	comment = ";" + restOfLine
	condition = oneOf("eq ne gt gte lt lte ult ulte")
	condition.setParseAction(Condition)

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
	
#	ldw1 = Literal("ldw") + reg + comma + s7 + lparen + reg + rparen
#	ldw2 = Literal("ldw") + reg + comma + reg + lparen + reg + rparen
#	ldw2.setParseAction(replace("ldw.b"))
#	ldw = ldw1 | ldw2
#
#	ldb1 = Literal("ldb") + reg + comma + s7 + lparen + reg + rparen
#	ldb2 = Literal("ldb") + reg + comma + reg + lparen + reg + rparen
#	ldb2.setParseAction(replace("ldb.b"))
#	ldb = ldb1 | ldb2
#
#	stw1 = Literal("stw") + s7 + lparen + reg + rparen + comma + reg
#	stw2 = Literal("stw") + reg + lparen + reg + rparen + comma + reg
#	stw2.setParseAction(replace("stw.b"))
#	stw = stw1 | stw2
#
#	stb1 = Literal("stb") + s7 + lparen + reg + rparen + comma + reg
#	stb2 = Literal("stb") + reg + lparen + reg + rparen + comma + reg
#	stb2.setParseAction(replace("stb.b"))
#	stb = stb1 | stb2
#
#	jmp1 = Literal("jmp") + (s13 ^ label_name)
#	jmp2 = Literal("jmp") + reg
#	jmp2.setParseAction(replace("jmp.r"))
#	jmp = jmp1 | jmp2
	
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
	instruction.setParseAction(Inst)
	line = Optional(label) + instruction
	g = OneOrMore(line)
	g.ignore(comment)
	return g


def parse(filename):
	tokens = None
	g = grammer()
	try:
		tokens = g.parseFile(filename, parseAll=True)
	except (ParseException, ParseFatalException), err:
		print err.line
		print " "*(err.column-1) + "^"
		print err
	return tokens


def expand_labels(tokens):
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
		return Number(delta, base=10, bits=13, signed=True)


	i = 0
	while i < len(tokens):
		tok = tokens[i]
		if isinstance(tok, Label):
			add_label(tok, i*2)
			del tokens[i]
			continue
		i += 1
	
	for i, tok in enumerate(tokens):
		for j, arg in enumerate(tok.args):
			if isinstance(arg, Label):
				tok.args[j] = lookup_label(arg, i*2)

	return tokens


def set_imm(inst, byte):
	if isinstance(inst.args[2], Immediate):
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

def translate(tokens):
	bytes = []
	for token in tokens:
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
	tokens = parse(in_filename)
	if not tokens:
		return 1
	tokens = expand_labels(tokens)
	bytes = translate(tokens)
	#for tok in tokens:
	#	print tok
	#return 1
	#print map(lambda b: bin_str(b, 16), bytes)
	fout = open(out_filename, "w")
	for byte in bytes:
		fout.write(bin_str(byte, 16) + "\n")

if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
