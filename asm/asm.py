import sys

import pyparsing

import isa
import encoding
import tokens
import macros
import grammer


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
		return tokens.Number((addr, 10), bits=bits, signed=signed, name=label.name)

	def apply_labels(tok, pos, signed=True, pc_relative=False):
		for j, arg in enumerate(tok.args):
			if tok.name == "jmp":
				pc_relative = True
			if isinstance(arg, tokens.Expression):
				apply_labels(arg, pos, False, pc_relative)
			elif isinstance(arg, tokens.Label):
				if tok.name == "jmp":
					bits = 11
				elif tok.name in ("ldw", "stw"):
					bits = 5
				elif tok.name in ("lui", "addi"):
					bits = 8
				elif isinstance(tok, tokens.Expression):
					# expressions will do their own bit checks and we need to ensure
					# label values aren't truncated
					bits = 64
				tok.args[j] = lookup_label(arg, pos, bits, signed, pc_relative)

	toks = list(toks)
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
		apply_labels(tok, pos)
		pos += tok.size

	return toks


def apply_text_data(toks):
	text = []
	data = []
	section = data
	for tok in toks:
		if isinstance(tok, tokens.Macro):
			if tok.name == ".text":
				section = text
				continue
			elif tok.name == ".data":
				section = data
				continue
		section.append(tok)
	return text + data


def parse_macro(tok, macro):
	try:
		g = grammer.grammer()
		return g.parseString(macro, parseAll=True)
	except RuntimeError, e:
		print macro
		print "Error while parsing expanded macro .%s; check macro syntax." % tok.name
		sys.exit(1)


def expand_macro(tok, byte_pos):
	result = tok.callback(byte_pos/2, *tok.args)
	if isinstance(result, str):
		toks = apply_macros(parse_macro(tok, result), byte_pos)
	else:
		toks = result
	for tok in toks:
		yield tok


def apply_macros(toks, byte_pos=0):
	for tok in toks:
		if isinstance(tok, tokens.Macro):
			for mtok in expand_macro(tok, byte_pos):
				yield mtok
				byte_pos += mtok.size
		else:
			yield tok
			byte_pos += tok.size


def translate(toks):
	bytes = []
	map(bytes.extend, map(encoding.encode, toks))
	return bytes


def main(args):
	if len(args) != 2:
		print "USAGE: asm source.asm output.o"
		return 2
	in_filename  = args[0]
	out_filename = args[1]
	try:
		g = grammer.grammer()
		toks = g.parseFile(in_filename, parseAll=True)
		if not toks:
			return 1
		toks = apply_text_data(toks)
		toks = apply_macros(toks)
		toks = expand_labels(toks)
		bytes = translate(toks)
		fout = open(out_filename, "wb")
		for byte in bytes:
			#fout.write(bin_str(byte, 8) + "\n")
			fout.write(chr(byte))
	except (pyparsing.ParseException, pyparsing.ParseFatalException), err:
		print err.line
		print " "*(err.column-1) + "^"
		print err
		return 1

if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
