class Token(object):
	size = 0
	args = []
	name = ""


class Label(Token):
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


class Instruction(Token):
	def __init__(self, name, args):
		self.name = name
		self.args = args
		self.size = 2

		# construct I/R token
		if name in ("add", "sub", "and", "or", "s", "as.nz", "as.z") and not isinstance(args[0], IR):
			ir = not isinstance(self.op2, Register)
			self.args.insert(0, IR(ir, "ir"))

	def __getattr__(self, name):
		for arg in self.args:
			if arg.name == name:
				return arg
		raise AttributeError("'Instruction' object has no attribute '%s'" % name)

	def __str__(self):
		name = self.name
		args = self.args
		if name == "s":
			name += "." + self.cond.type
			args = [arg for arg in args if not isinstance(arg, Condition)]
		return name + "\t" + ", ".join(str(arg) for arg in args if not isinstance(arg, IR))

	def __repr__(self):
		s = ""
		for arg in self.args:
			s += " "
			if arg.name:
				s += arg.name + "="
			s += repr(arg)
		return "<Inst %s%s>" % (self.name, s)


class Number(Token):
	def __init__(self, n, base, bits, signed, name=""):
		self.value = n
		self.base = base
		self.bits = bits
		self.signed = signed
		self.name = name
		self.size = bits / 8
		self.size += 1 if bits % 8 else 0

		# check for valid value
		if signed and base == 10:
			if not (-2**(bits-1) <= n and n <= 2**(bits-1)-1):
				raise ValueError(
					"%s out of bounds for a %d bit signed number in base %d" % (n, bits, base))
		elif not (0 <= n and n < 2**bits):
			raise ValueError(
				"%s out of bounds for a %d bit unsigned number in base %d" % (n, bits, base))

	def binary(self):
		if self.signed and self.value < 0:
			# two's complement by subtracting from 2^n
			m = 2 ** self.bits
			return m + self.value
		return self.value

	def __str__(self):
		return "0x" + hex(self.binary())[2:].upper()

	def __repr__(self):
		signed = "s" if self.signed else "u"
		return "<Num %d %s%d>" % (self.value, signed, self.bits)


class Register(Token):
	def __init__(self, reg, name=""):
		self.name = name
		self.value = reg
	
	def binary(self):
		return self.value

	def __str__(self):
		return "$%d" % self.value

	def __repr__(self):
		return "<Reg %d>" % self.value


class Immediate(Token):
	def __init__(self, value, name=""):
		self.value = value
		self.name = name
	
	def binary(self):
		return immediates[self.value]

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return "<Imm %d>" % self.value


class Condition(Token):
	def __init__(self, type, name):
		self.type = type
		self.name = name
	
	def binary(self):
		return conditions[self.type]

	def __str__(self):
		return "<Cond %s>" % self.type
	__repr__ = __str__


class Macro(Token):
	def __init__(self, name, callback, args):
		self.name = name
		self.callback = callback
		self.args = args
	
	def __str__(self):
		if self.args:
			args = " " + ", ".join(map(repr, self.args))
		else:
			args = ""
		return "<Macro %s%s>" % (self.name, args)
	__repr__ = __str__


class IR(Token):
	def __init__(self, value, name=""):
		self.value = True if value else False
		self.name = name

	def binary(self):
		return 1 if self.value else 0

	def __str__(self):
		return "<IR %d>" % self.value
	__repr__ = __str__


encodings = []

def add(name, prelude, prelude_end, *args):
	encodings.append((name, prelude, prelude_end, args))

add("ldw",    0x0, 13, ("offset", "s7", 12, 6), ("base", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("ldb",    0x1, 13, ("offset", "s7", 12, 6), ("base", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("stw",    0x2, 13, ("offset", "s7", 12, 6), ("base", "reg", 5, 3), ("src", "reg", 2, 0))
add("stb",    0x3, 13, ("offset", "s7", 12, 6), ("base", "reg", 5, 3), ("src", "reg", 2, 0))

add("jmp",    0x4, 13, ("offset", "s13", 12, 0))

add("add",   0x28, 10, ("ir", "ir", 9, 9), ("op1", "reg", 8, 6), ("op2", "ireg", 5, 3), ("tgt", "reg", 2, 0))
add("sub",   0x29, 10, ("ir", "ir", 9, 9), ("op1", "reg", 8, 6), ("op2", "ireg", 5, 3), ("tgt", "reg", 2, 0))
add("and",   0x2A, 10, ("ir", "ir", 9, 9), ("op1", "reg", 8, 6), ("op2", "ireg", 5, 3), ("tgt", "reg", 2, 0))
add("or",    0x2B, 10, ("ir", "ir", 9, 9), ("op1", "reg", 8, 6), ("op2", "ireg", 5, 3), ("tgt", "reg", 2, 0))
add("s",     0x2C, 10, ("ir", "ir", 9, 9), ("op1", "reg", 8, 6), ("op2", "ireg", 5, 3), ("cond", "cond", 2, 0))
add("as.z",  0x2D, 10, ("ir", "ir", 9, 9), ("op1", "reg", 8, 6), ("op2", "ireg", 5, 3), ("tgt", "reg", 2, 0))
add("as.nz", 0x2E, 10, ("ir", "ir", 9, 9), ("op1", "reg", 8, 6), ("op2", "ireg", 5, 3), ("tgt", "reg", 2, 0))

add("lui",   0x18, 11, ("imm", "s8", 10, 3), ("tgt", "reg", 2, 0))
add("addi",  0x19, 11, ("imm", "s8", 10, 3), ("tgt", "reg", 2, 0))

add("ldw",   0x68,  9, ("index", "reg",  8, 6), ("base", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("ldb",   0x69,  9, ("index", "reg",  8, 6), ("base", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("stw",   0x6A,  9, ("index", "reg",  8, 6), ("base", "reg", 5, 3), ("src", "reg", 2, 0))
add("stb",   0x6B,  9, ("index", "reg",  8, 6), ("base", "reg", 5, 3), ("src", "reg", 2, 0))

add("shl",   0x36, 10, ("count", "u4", 9, 6), ("src", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("shr",   0x37, 10, ("count", "u4", 9, 6), ("src", "reg", 5, 3), ("tgt", "reg", 2, 0))

add("xor",  0x380,  6, ("src", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("not",  0x381,  6, ("src", "reg", 5, 3), ("tgt", "reg", 2, 0))

add("halt", 0xFEDE, 0)
add("trap",  0xFEE, 4, ("sysnum", "u4", 3, 0))
add("sext", 0x1FDE, 3, ("tgt", "reg", 2, 0))
add("jmp",  0x1FDF, 3, ("tgt", "reg", 2, 0))


conditions = {"eq": 0, "ne": 1, "gt": 2, "gte": 3, "lt": 4, "lte":5, "ult": 6, "ulte": 7}
conditions_rev = dict(zip(conditions.values(), conditions.keys()))
immediates = {8: 0, 4: 1, 2: 2, 1: 3, -1: 4, -2: 5, -4: 6, -8: 7}
immediates_rev = dict(zip(immediates.values(), immediates.keys()))


def encoding(token):
	for code in encodings:
		if code[0] == token.name:
			code_args_names = [arg[0] for arg in code[3]]
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
	if code:
		opname, prelude, prelude_end, args = code
		word = prelude << prelude_end
		for name, type, start, end in args:
			value = getattr(token, name).binary()
			word |= value << end
		return [(word & 0xFF00) >> 8, word & 0xFF]


def decode(opcode):
	for code in encodings:
		name, prelude_val, prelude_end, args = code
		prelude = prelude_val << prelude_end
		prelude_mask = (2**(16 - prelude_end) - 1) << prelude_end
		if (opcode & prelude_mask) == prelude:
			tok_args = []
			for arg in args:
				aname, type, start, end = arg
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
					arg = Condition(conditions_rev[value], aname)
				elif type == "ireg":
					if tok_args[0].value:
						arg = Immediate(immediates_rev[value], aname)
					else:
						arg = Register(value, aname)
				elif type == "s7":
					arg = Number(twoc(value, 7), 10, 7, True, aname)
				elif type == "s8":
					arg = Number(twoc(value, 8), 10, 8, True, aname)
				elif type == "s13":
					arg = Number(twoc(value, 13), 10, 13, True, aname)
				elif type == "u4":
					arg = Number(value, 10, 4, False, aname)
				else:
					raise ValueError("Unknown opcode argument type: " + type)
				tok_args.append(arg)
			return Instruction(name, tok_args)
	raise ValueError("Unknown opcode: " + hex(opcode))
