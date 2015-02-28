import copy

import isa
from tokens import *
import grammer

def encoding(token):
	for code in isa.encodings:
		if code["name"] == token.name:
			code_args_names = [arg[0] for arg in code["args"]]
			token_args_names = [arg.name for arg in token.args]
			if sorted(token_args_names) == sorted(code_args_names):
				return code


def encode(token):
	grammer.grammer() # ensure all encodings have been fully loaded
	if isinstance(token, (Number, Expression)):
		words = []
		size = token.size
		num = token.binary()
		while size > 0:
			words.append(num & 0xFF)
			num >>= 8
			size -= 1
		return reversed(words)
	code = encoding(token)
	if not code:
		raise ValueError("unknown token: " + repr(token))
	opname = code["name"]
	prelude = code["prelude"]
	prelude_end = code["prelude_end"]
	args = code["args"]
	word = prelude << prelude_end
	for name, start, end in args:
		value = getattr(token, name)
		if opname == "jmp" and name == "offset":
			# create shallow copy of value so we don't modify the token object
			value = copy.copy(value)
			value.value -= 1
		word |= value.binary() << end
		if word < 0:
			raise Error("cannot encode negative word: " + hex(word))
	return [(word & 0xFF00) >> 8, word & 0xFF]


def _load_cache(cache):
	grammer.grammer() # ensure all encodings have been fully loaded
	for code in isa.encodings:
		prelude = code["prelude"]
		pend = code["prelude_end"]
		if pend == 13:
			prelude <<= 2
		cache[prelude] = code


def decode(opcode, _cache={}):
	if not _cache:
		_load_cache(_cache)
	mask5 = opcode >> 11
	mask3 = mask5 & 0x1D
	code = _cache.get(mask5, None)
	if code is None:
		code = _cache.get(mask3, None)
		if code is None:
			raise ValueError("Unknown opcode: " + hex(opcode))
	name = code["name"]
	args = code["args"]
	tok_args = []
	for arg in args:
		aname, start, end = arg
		type = aname if aname in ("ir", "epc") else code["types"][aname]
		mask = ((2**(start - end + 1) - 1) << end)
		value = (opcode & mask) >> end
		def twoc(n, bits):
			if n & (1 << (bits-1)):
				return n - 2**bits
			return n

		if   type == "reg":
			arg = Register(value, aname)
		elif type == "creg":
			arg = ControlRegister(value, aname)
		elif type in ("ir", "epc"):
			arg = Bit(value, aname)
		elif type == "cond":
			arg = Condition(isa.conditions_rev[value], aname)
		elif type == "ireg":
			if tok_args[0].value == 1:
				n = Number((isa.immediates_rev[value], 10), 5, True)
				arg = Immediate(n, aname)
			else:
				arg = Register(value, aname)
		elif type == "jreg":
			if tok_args[0].value == 1:
				arg = ControlRegister(value, aname)
			else:
				arg = Register(value, aname)
		elif type.startswith("s"):
			n = int(type[1:])
			arg = Number((twoc(value, n), 10), n, True, aname)
		elif type.startswith("u"):
			n = int(type[1:])
			arg = Number((value, 10), n, False, aname)
		else:
			raise ValueError("Unknown opcode argument type: " + type)
		arg.type = type
		if name == "jmp" and aname == "offset":
			arg.value += 1
		arg.dest = False
		tok_args.append(arg)
	if tok_args:
		tok_args[-1].dest = True # set the rightmost argument as the destination (HACK)
	return Instruction(name, *tok_args)
