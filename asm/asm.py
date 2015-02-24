#!/usr/bin/python

import collections
import os.path
import sys

import pyparsing

import isa
import encoding
import tokens
import macros
import grammer


MAGIC_HEADER = [0xDEAD, 0xF00D]
CHUNK_SEC, CHUNK_ADDR, CHUNK_TOKS = range(3)


### macros

def apply_macros(toks):
	for tok in toks:
		if isinstance(tok, tokens.Macro):
			results = tok.callback(*tok.args)
			if results is None:
				results = [tok]
			elif isinstance(results, str):
				results = apply_macros(parse_macro(results))
			for mtok in results:
				yield mtok
		else:
			yield tok


def parse_macro(macro):
	try:
		g = grammer.grammer()
		return g.parseString(macro, parseAll=True)
	except RuntimeError, e:
		print macro
		print "Error while parsing expanded macro .%s; check macro syntax." % tok.name
		sys.exit(1)


### directives

def apply_directives(toks):
	chunks = {
		".text": [(".text", 0, [])],
		".data": [(".data", 0, [])],
	}
	chunk = chunks[".text"][-1]
	vars = {}
	for tok in toks:
		if isinstance(tok, tokens.Macro):
			if tok.name in (".text", ".data"):
				chunk = chunks[tok.name][-1]
				continue
			elif tok.name == ".org":
				section = chunk[CHUNK_SEC]
				addr = tok.args[0].value
				chunk = (section, addr, [])
				chunks[section].append(chunk)
				continue
			elif tok.name == ".align":
				align = tok.args[0].value
				addr = chunk[CHUNK_ADDR] + chunk_size(chunk)
				padding = 0 if (addr % align) == 0 else align - (addr % align)
				for _ in range(padding):
					chunk[CHUNK_TOKS].append(tokens.Number((0, 10), bits=16, signed=False))
				continue
			elif tok.name == ".set":
				name = tok.args[0].value
				value = tok.args[1]
				apply_variables(value, vars)
				vars[name] = value
				continue
		apply_variables(tok, vars)
		chunk[CHUNK_TOKS].append(tok)
	for chunklist in chunks.values():
		for chunk in chunklist:
			yield chunk


def apply_variables(tok, vars):
	for i,arg in enumerate(tok.args):
		if isinstance(arg, tokens.Label):
			if arg.value in vars:
				arg_name = tok.args[i].name
				tok.args[i] = vars[arg.value]
				tok.args[i].name = arg_name
		elif isinstance(arg, tokens.Expression):
			apply_variables(arg, vars)


### labels

def lookup_labels(chunks):
	labels = collections.defaultdict(list)
	new_chunks = []
	addrs = collections.defaultdict(int)
	for section, start_addr, insts in chunks:
		addr = start_addr
		if start_addr < 0:
			addr = addrs[section]
			start_addr = addr
		non_labels = []
		for inst in insts:
			if isinstance(inst, tokens.Label):
				labels[inst.value].append(addr)
			else:
				non_labels.append(inst)
				addr += 1
		addrs[section] = addr
		new_chunks.append((section, start_addr, non_labels))
	return new_chunks, labels


def apply_labels(chunks, labels):
	for section, start_addr, insts in chunks:
		addr = start_addr
		insts = list(insts)
		for inst in insts:
			label_apply(labels, inst, addr)
			addr += inst.size
		yield section, start_addr, insts


def label_apply(labels, tok, pos, signed=True, pc_relative=False):
	for j, arg in enumerate(tok.args):
		if tok.name == "jmp":
			pc_relative = True
		if isinstance(arg, tokens.Expression):
			label_apply(labels, arg, pos, False, pc_relative)
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
			tok.args[j] = label_find(labels, arg, pos, bits, signed, pc_relative)


def label_find(labels, label, pos, bits, signed, pc_relative):
	if label.value == "@":
		return pos
	if label.value not in labels:
		raise Exception("unknown label %s" % repr(label.value))
	pos /= 2
	search = labels[label.value]
	if len(search) == 1:
		addr = search[0]
	else:
		if label.direction == "f":
			addr = [l for l in search if l > pos][0]
		elif label.direction == "b":
			addr = [l for l in search if l <= pos][-1]
		else:
			raise Exception("Ambiguous definition for label %s" % repr(label.value))
	if pc_relative:
		addr -= pos
	return tokens.Number((addr, 10), bits=bits, signed=signed, name=label.name)


### chunks

def merge_chunks(chunks):
	schunks = sorted(chunks, key=lambda (sec,addr,insts): (sec, addr))
	prev_chunk = schunks[0]
	for chunk in schunks[1:]:
		merged, new_chunk = chunk_merge(prev_chunk, chunk)
		if not merged:
			yield prev_chunk
		prev_chunk = new_chunk
	yield prev_chunk


def chunk_merge(left_chunk, right_chunk):
	lsect, lstart, linsts = left_chunk
	rsect, rstart, rinsts = right_chunk
	lend = lstart + chunk_size(left_chunk)
	rend = rstart + chunk_size(right_chunk)
	# if sections are different: return only right
	# if right starts within left: zip right into left
	# if right ends within left: zip left into right
	# if left is subset of right: return only right (left is subsumed by right)
	# otherwise no intersection: return only right
	if lsect != rsect:
		return False, right_chunk
	elif lstart <= rstart <= lend:
		return True, chunk_zip(left_chunk, right_chunk)
	elif lstart <= rend <= lend:
		return True, chunk_zip(right_chunk, left_chunk)
	elif rstart <= lstart <= rend:
		return True, right_chunk
	return False, right_chunk


def chunk_zip(left_chunk, right_chunk):
	section, laddr, linsts = left_chunk
	_, raddr, rinsts = right_chunk
	insts = []
	addr = laddr
	while addr < (laddr + chunk_size(left_chunk)):
		if addr == raddr:
			insts.extend(rinsts)
			addr += chunk_size(right_chunk)
		else:
			insts.append(linsts[addr - laddr])
			addr += 1
	return section, laddr, insts


def chunk_size(chunk):
	return sum(inst.size for inst in chunk[CHUNK_TOKS]) / 2


### translation

def translate(chunks):
	for section, addr, insts in chunks:
		bytes = []
		map(bytes.extend, map(encoding.encode, insts))
		yield section, addr, bytes


def emit(stream, chunks):
	def emit_word(word):
		stream.write(chr(word >> 8))
		stream.write(chr(word & 0x00FF))
	def emit_chunk(chunk):
		_, addr, bytes = chunk
		emit_word(addr)
		emit_word(len(bytes) / 2)
		map(stream.write, map(chr, bytes))
	chunks = [chunk for chunk in chunks if chunk[CHUNK_TOKS]]
	dchunks = filter(lambda c: c[CHUNK_SEC] == ".data", chunks)
	ichunks = filter(lambda c: c[CHUNK_SEC] == ".text", chunks)
	map(emit_word, MAGIC_HEADER)
	emit_word(len(dchunks))
	map(emit_chunk, dchunks)
	emit_word(len(ichunks))
	map(emit_chunk, ichunks)


### main

def main(args):
	if len(args) != 2:
		print "USAGE: asm source.asm output.o"
		return 2
	in_filename  = args[0]
	out_filename = args[1]
	macro_filename = in_filename[:in_filename.rfind(".")] + ".py"
	try:
		if os.path.exists(macro_filename):
			execfile(macro_filename, {"macro": macros.macro})
		g = grammer.grammer()
		tokens = g.parseFile(in_filename, parseAll=True)
		if not tokens:
			return 1
		tokens = apply_macros(tokens)
		chunks = apply_directives(tokens)
		chunks = list(chunks)
		chunks, labels = lookup_labels(chunks)
		chunks = apply_labels(chunks, labels)
		chunks = merge_chunks(chunks)
		chunks = translate(chunks)
		with open(out_filename, "wb") as stream:
			emit(stream, chunks)
	except (pyparsing.ParseException, pyparsing.ParseFatalException), err:
		print err.line
		print " "*(err.column-1) + "^"
		print err
		return 1

if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
