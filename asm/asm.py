import sys

import isa
import directives
import macros
from grammer import *


def bin_str(n, bits=0):
	s = ""
	while n:
		s = ("1" if n & 1 else "0") + s
		n >>= 1
	return s.zfill(bits)


def expand_labels(toks):
	labels = {}

	def add_label(label, pos):
		label.pos = pos
		if label.value not in labels:
			labels[label.value] = []
		labels[label.value].append(label)

	def lookup_label(label, pos, bits, signed, pc_relative):
		if label.value not in labels:
			raise Exception("Unknown label %s" % repr(label.value))
		search = labels[label.value]
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
		return isa.Number((addr, 10), bits=bits, signed=signed, name=label.name)

	def apply_labels(tok, pos, signed=True, pc_relative=False):
		for j, arg in enumerate(tok.args):
			if tok.name == "jmp":
				pc_relative = True
			if isinstance(arg, isa.Expression):
				apply_labels(arg, pos, False, pc_relative)
			elif isinstance(arg, isa.Label):
				if tok.name == "jmp":
					bits = 13
				elif tok.name in ("ldw", "ldb", "stw", "stb"):
					bits = 7
				elif tok.name in ("lui", "addi"):
					bits = 8
				elif isinstance(tok, isa.Expression):
					bits = tok.bits
				tok.args[j] = lookup_label(arg, pos, bits, signed, pc_relative)

	i = 0
	pos = 0
	while i < len(toks):
		tok = toks[i]
		if isinstance(tok, isa.Label):
			add_label(tok, pos)
			del toks[i]
			continue
		pos += tok.size
		i += 1
	
	pos = 0
	for i, tok in enumerate(toks):
		apply_labels(tok, pos)
		pos += tok.size

	return toks


def apply_text_data(toks):
	text = []
	data = []
	section = data
	for tok in toks:
		if isinstance(tok, isa.Macro):
			if tok.name == "text":
				section = text
				continue
			elif tok.name == "data":
				section = data
				continue
		section.append(tok)
	return text + data


def apply_macros(toks):
	g = grammer()
	pos = 0
	i = 0
	had_macros = False
	while i < len(toks):
		tok = toks[i]
		if isinstance(tok, isa.Macro):
			result = tok.callback(pos, *tok.args)
			if result is not None:
				had_macros = True
				del toks[i]
				if isinstance(result, str):
					try:
						new_toks = g.parseString(result, parseAll=True)
					except RuntimeError, e:
						print result
						print "Error while parsing expanded macro .%s; check macro syntax." % tok.name
						sys.exit(1)
				else:
					new_toks = result
				for tok in reversed(new_toks):
					pos += tok.size
					toks.insert(i, tok)
				i += len(new_toks)
				continue
		pos += toks[i].size
		i += 1
	if had_macros:
		return apply_macros(toks)
	return toks


def translate(toks):
	bytes = []
	map(bytes.extend, map(isa.encode, toks))
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
		#for tok in toks: print repr(tok)
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
		return 1

if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
