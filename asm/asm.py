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
	ldw = Literal("ldw") + tgt + comma + offset + lparen + base + rparen
	ldb = Literal("ldb") + tgt + comma + offset + lparen + base + rparen
	stw = Literal("stw") + offset + lparen + base + rparen + comma + src
	stb = Literal("stb") + offset + lparen + base + rparen + comma + src

	jmp = Literal("jmp") + (s13 ^ label_name ^ reg("tgt"))
	
	add = Literal("add") + reg3_imm
	sub = Literal("sub") + reg3_imm
	and_i = Literal("and") + reg3_imm
	or_i = Literal("or") + reg3_imm
	addskipz = Literal("as.z") + reg3_imm
	addskipnz = Literal("as.nz") + reg3_imm

	skip = Literal("s") + Suppress(".") + condition + op1 + comma + reg_imm

	lui = Literal("lui")   + tgt + comma + s8("imm")
	addi = Literal("addi") + tgt + comma + s8("imm")

	shl = Literal("shl") + tgt + comma + src + comma + u4("count")
	shr = Literal("shr") + tgt + comma + src + comma + u4("count")

	xor = Literal("xor")   + tgt + comma + src
	not_i = Literal("not") + tgt + comma + src

	halt = Literal("halt")
	trap = Literal("trap") + u4("sysnum")
	sext = Literal("sext") + tgt

	instruction = ldw | ldb | stw | stb | jmp | add | sub | and_i | or_i | skip | addskipz
	instruction |= addskipnz | lui | addi | shl | shr | xor | not_i | halt | trap | sext
	instruction.setParseAction(lambda s,l,t: tokens.Instruction(t[0], t[1:]))
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
		addr /= 2
		# TODO check that number is in bounds for a N bit signed number
		return tokens.Number(addr, base=10, bits=bits, signed=True, name="offset")

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


def translate(toks):
	bytes = []
	map(bytes.extend, map(tokens.encode, toks))
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
		#for tok in toks: print str(tok)
		#return 1
		bytes = translate(toks)
		fout = open(out_filename, "wb")
		for byte in bytes:
			fout.write(bin_str(byte, 8) + "\n")
			#fout.write(chr(byte))
	except (ParseException, ParseFatalException), err:
		print err.line
		print " "*(err.column-1) + "^"
		print err

if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
