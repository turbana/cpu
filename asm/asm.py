import sys

import tokens
import directives
from grammer import *


def bin_str(n, bits=0):
	s = ""
	while n:
		s = ("1" if n & 1 else "0") + s
		n >>= 1
	return s.zfill(bits)


def grammer():
	base = (s7 | reg)
	ldw = Literal("ldw") + reg + comma + base + lparen + reg + rparen
	ldb = Literal("ldb") + reg + comma + base + lparen + reg + rparen
	stw = Literal("stw") + base + lparen + reg + rparen + comma + reg
	stb = Literal("stb") + base + lparen + reg + rparen + comma + reg

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
	macro = directives.grammer()
	line = Optional(label) + (instruction | macro)
	g = OneOrMore(line)
	g.ignore(comment)
	return g


def expand_labels(toks):
	labels = {}

	def add_label(label, pos):
		label.pos = pos
		if label.name not in labels:
			labels[label.name] = []
		labels[label.name].append(label)

	def lookup_label(label, pos, bits, pc_relative):
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
		addr = found.pos
		if pc_relative:
			addr -= pos
		# TODO check that number is in bounds for a N bit signed number
		return tokens.Number(addr, base=10, bits=bits, signed=True)

	i = 0
	pos = 0
	while i < len(toks):
		tok = toks[i]
		if isinstance(tok, tokens.Label):
			add_label(tok, pos)
			del toks[i]
			continue
		pos += tok.size
		i += 1
	
	pos = 0
	for i, tok in enumerate(toks):
		for j, arg in enumerate(tok.args):
			if isinstance(arg, tokens.Label):
				pc_relative = False
				if tok.name == "jmp":
					pc_relative = True
					bits = 13
				elif tok.name in ("ldw", "ldb", "stw", "stb"):
					bits = 7
				elif tok.name in ("lui", "addi"):
					bits = 8
				tok.args[j] = lookup_label(arg, pos, bits, pc_relative)
		pos += tok.size

	return toks


def apply_text_data(toks):
	text = []
	data = []
	current = data
	for tok in toks:
		if isinstance(tok, tokens.Macro):
			if tok.name == "text":
				current = text
				continue
			elif tok.name == "data":
				current = data
				continue
		current.append(tok)
	return text + data


def apply_macros(toks):
	g = grammer()
	pos = 0
	i = 0
	while i < len(toks):
		tok = toks[i]
		if isinstance(tok, tokens.Macro):
			result = tok.callback(pos, *tok.args)
			if result is not None:
				del toks[i]
				if isinstance(result, str):
					new_toks = g.parseString(result, parseAll=True)
				else:
					new_toks = result
				for tok in reversed(new_toks):
					pos += tok.size
					toks.insert(i, tok)
				i += len(new_toks)
				continue
		pos += toks[i].size
		i += 1
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
		if isinstance(token, tokens.Number):
			value = token.binary()
		else:
			inst = instructions[token.name]
			value = inst[0]
			for i, n in enumerate(inst[1:]):
				value |= token.args[i].binary() << n
			if token.name in extra:
				value = extra[token.name](token, value)
		size = token.size
		data = []
		while size > 0:
			data.append(value & 0xFF)
			value >>= 1
			size -= 1
		data.reverse()
		bytes.extend(data)
	return bytes


def main(args):
	if len(args) != 2:
		print "USAGE: asm source.asm output.o"
		return 2
	in_filename  = args[0]
	out_filename = args[1]
	try:
		g = grammer()
		toks = g.parseFile(in_filename, parseAll=True)
		if not toks:
			return 1
		toks = apply_text_data(toks)
		toks = apply_macros(toks)
		toks = expand_labels(toks)
		for tok in toks:
			print tok.size, tok
		#return 1
		bytes = translate(toks)
		fout = open(out_filename, "wb")
		for byte in bytes:
			#fout.write(bin_str(byte, 8) + "\n")
			fout.write(chr(byte))
	except (ParseException, ParseFatalException), err:
		print err.line
		print " "*(err.column-1) + "^"
		print err

if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
