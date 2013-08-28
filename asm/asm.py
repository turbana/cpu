import sys

import tokens
from grammer import *


def bin_str(n, bits=0):
	s = ""
	while n:
		s = ("1" if n & 1 else "0") + s
		n >>= 1
	return s.zfill(bits)


def grammer():
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
