import isa
from tokens import *

def encoding(token):
	for code in isa.encodings:
		if code["name"] == token.name:
			code_args_names = [arg[0] for arg in code["args"]]
			token_args_names = [arg.name for arg in token.args]
			if sorted(token_args_names) == sorted(code_args_names):
				return code


def encode(token):
	if isinstance(token, Number):
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
		value = getattr(token, name).binary()
		word |= value << end
		if word < 0:
			raise Error("cannot encode negative word: " + hex(word))
	return [(word & 0xFF00) >> 8, word & 0xFF]


def decode(opcode):
	for code in isa.encodings:
		name = code["name"]
		prelude_val = code["prelude"]
		prelude_end = code["prelude_end"]
		args = code["args"]
		prelude = prelude_val << prelude_end
		prelude_mask = (2**(16 - prelude_end) - 1) << prelude_end
		if (opcode & prelude_mask) == prelude:
			tok_args = []
			for arg in args:
				aname, start, end = arg
				type = code["types"][aname] if aname != "ir" else "ir"
				mask = (1 << end) if start == end else ((2**(start - end + 1) - 1) << end)
				value = (opcode & mask) >> end
				def twoc(n, bits):
					if n & (1 << (bits-1)):
						return n - 2**bits
					return n

				if   type == "reg":
					arg = Register(value, aname)
				elif type == "ir":
					arg = IR(value, aname)
				elif type == "cond":
					arg = Condition(isa.conditions_rev[value], aname)
				elif type == "ireg":
					if tok_args[0].value == 1:
						n = Number((isa.immediates_rev[value], 10), 5, True)
						arg = Immediate(n, aname)
					else:
						arg = Register(value, aname)
				elif type == "s7":
					arg = Number((twoc(value, 7), 10), 7, True, aname)
				elif type == "s8":
					arg = Number((twoc(value, 8), 10), 8, True, aname)
				elif type == "s13":
					arg = Number((twoc(value, 13), 10), 13, True, aname)
				elif type == "u4":
					arg = Number((value, 10, 4), False, aname)
				else:
					raise ValueError("Unknown opcode argument type: " + type)
				arg.type = type
				tok_args.append(arg)
			return Instruction(name, *tok_args)
	raise ValueError("Unknown opcode: " + hex(opcode))
