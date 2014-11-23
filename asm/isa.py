class Token(object):
	size = 0
	args = []
	name = ""


class Label(Token):
	def __init__(self, value, direction=None, name=""):
		self.value = value
		self.name = name
		self.direction = direction
		self.pos = -1
	
	def __str__(self):
		if self.direction:
			return "<Label %s %s>" % (repr(self.value), self.direction)
		elif self.pos >= 0:
			return "<Label %s @%d>" % (repr(self.value), self.pos)
		return "<Label %s>" % repr(self.value)
	__repr__ = __str__


class Instruction(Token):
	def __init__(self, name, args):
		self.name = name
		self.args = args
		self.size = 2

		# construct I/R token
		if name in ir_insts and not isinstance(args[0], IR):
			ir = not isinstance(self.op2, Register)
			self.args.insert(0, IR(ir, "ir"))

	def arguments(self):
		d = {}
		for arg in self.args:
			d[arg.name] = arg.value
		return d

	def __getattr__(self, name):
		for arg in self.args:
			if arg.name == name:
				return arg
		raise AttributeError("'Instruction' object has no attribute '%s'" % name)

	def __str__(self):
		name = self.name
		args = self.args
		if name == "s":
			name += "." + self.cond.value
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
	def __init__(self, (n, base), bits, signed, name=""):
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
		n = self.binary()
		bytes = []
		size = self.size
		while size > 0:
			# when self.binary() returns a python long: hex() prints an L
			byte = hex(n & 0xFF).replace("L", "")[2:].upper().zfill(2)
			bytes.append("0x" + byte)
			n >>= 8
			size -= 1
		return " ".join(reversed(bytes))

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


class ControlRegister(Register):
	def __str__(self):
		return "$cr%d" % self.value

	def __repr__(self):
		return "<CReg %d>" % self.value


class Immediate(Token):
	def __init__(self, value, name=""):
		self.number = value
		self.name = name
	
	def binary(self):
		return immediates[self.number.value]

	def __str__(self):
		return str(self.number.value)

	def __repr__(self):
		return "<Imm %d>" % self.number.value


class Condition(Token):
	def __init__(self, value, name):
		self.value = value
		self.name = name
	
	def binary(self):
		return conditions[self.value]

	def __str__(self):
		return "<Cond %s>" % self.value
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


class Expression(Token):
	def __init__(self, args, **kwargs):
		if len(args) == 3:
			possible_expr = (0, 2)
		elif len(args) == 2:
			possible_expr = (1, )
		for i in possible_expr:
			if isinstance(args[i], list):
				args[i] = Expression(args[i], name="", bits=64, signed=False)
		self.args = args
		self.name = kwargs["name"]
		self.bits = kwargs["bits"]
		self.signed = kwargs["signed"]
		self._value = None

	def binary(self):
		return self.value.binary()

	def _evaluate(self):
		if self._value is not None:
			return self._value
		if len(self.args) == 1:
			self._value = self.args[0].value
			return self._value
		elif len(self.args) == 2:
			op, op1 = self.args
			op2 = 0
		elif len(self.args) == 3:
			op1, op, op2 = self.args
		op1 = op1.value if isinstance(op1, Expression) else op1
		op1 = op1.value if isinstance(op1, Number)     else op1
		op1 = None      if isinstance(op1, Label)      else op1
		op2 = op2.value if isinstance(op2, Expression) else op2
		op2 = op2.value if isinstance(op2, Number)     else op2
		op2 = None      if isinstance(op2, Label)      else op2
		if op1 is None or op2 is None:
			# either op's are a Label or an Expression that can't be evaluated yet
			return None
		# evaluate
		if op == "~": res = ~op1
		elif op == "+": res = op1 + op2
		elif op == "-": res = op1 - op2
		elif op == "*": res = op1 * op2
		elif op == "/": res = op1 / op2
		elif op == "%": res = op1 % op2
		elif op == "&": res = op1 & op2
		elif op == "|": res = op1 | op2
		elif op == "^": res = op1 ^ op2
		elif op == "<<": res = op1 << op2
		elif op == ">>": res = op1 >> op2
		elif op == "**": res = op1 ** op2
		res &= (2 ** self.bits) - 1
		# Number() is unsigned as the result already has the bit pattern we want
		# and is in bounds, so no checking or conversion is neccesary.
		self._value = Number((res, 10), bits=self.bits, signed=False)
		return self._value
	value = property(_evaluate)

	def __str__(self):
		self._evaluate()
		sign = "s" if self.signed else "u"
		val = self._value if self._value is not None else self.args
		return "<Expr %s%s %s>" % (sign, self.bits, val)
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
add("xor",   0x2F, 10, ("ir", "ir", 9, 9), ("op1", "reg", 8, 6), ("op2", "ireg", 5, 3), ("tgt", "reg", 2, 0))

add("lui",   0x18, 11, ("imm", "s8", 10, 3), ("tgt", "reg", 2, 0))
add("addi",  0x19, 11, ("imm", "s8", 10, 3), ("tgt", "reg", 2, 0))

add("ldw",   0x68,  9, ("index", "reg",  8, 6), ("base", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("ldb",   0x69,  9, ("index", "reg",  8, 6), ("base", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("stw",   0x6A,  9, ("index", "reg",  8, 6), ("base", "reg", 5, 3), ("src", "reg", 2, 0))
add("stb",   0x6B,  9, ("index", "reg",  8, 6), ("base", "reg", 5, 3), ("src", "reg", 2, 0))

add("shl",   0x360, 6, ("src", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("shr",   0x361, 6, ("src", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("sext",  0x362, 6, ("src", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("sar",   0x363, 6, ("src", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("inw",   0x364, 6, ("src", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("inb",   0x365, 6, ("src", "reg", 5, 3), ("tgt", "reg", 2, 0))
add("outw",  0x366, 6, ("tgt", "reg", 5, 3), ("src", "reg", 2, 0))
add("outb",  0x367, 6, ("tgt", "reg", 5, 3), ("src", "reg", 2, 0))

add("halt", 0xFEDE, 0)
add("trap",  0xFEE, 4, ("sysnum", "u4", 3, 0))
add("jmp",  0x1FDF, 3, ("tgt", "reg", 2, 0))
add("lcr",   0x3FE, 6, ("cr", "creg", 5, 3), ("tgt", "reg", 2, 0))
add("scr",   0x3FF, 6, ("cr", "creg", 5, 3), ("src", "reg", 2, 0))


conditions = {"eq": 0, "ne": 1, "gt": 2, "gte": 3, "lt": 4, "lte":5, "ult": 6, "ulte": 7}
conditions_rev = dict(zip(conditions.values(), conditions.keys()))
immediates = {8: 0, 4: 1, 2: 2, 1: 3, -1: 4, -2: 5, -4: 6, -8: 7}
immediates_rev = dict(zip(immediates.values(), immediates.keys()))
ir_insts = [opcode[0] for opcode in encodings for arg in opcode[3] if arg[0] == "ir"]


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
	if not code:
		raise ValueError("unknown token: " + repr(token))
	opname, prelude, prelude_end, args = code
	word = prelude << prelude_end
	for name, type, start, end in args:
		value = getattr(token, name).binary()
		word |= value << end
		if word < 0:
			raise Error("cannot encode negative word: " + hex(word))
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
					if tok_args[0].value == 1:
						n = Number((immediates_rev[value], 10), 5, True)
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
				tok_args.append(arg)
			return Instruction(name, tok_args)
	raise ValueError("Unknown opcode: " + hex(opcode))
