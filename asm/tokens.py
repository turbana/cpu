# this is set by isa.py to give us a reference to the encodings
#encodings = None

import isa


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
	def __init__(self, *args, **kwargs):
		self.name = args[0]
		self.args = list(args[1:])
		self.size = 2

		# construct I/R token
		for arg in self.args:
			if arg.type == "ir":
				break
			if arg.type == "ireg":
				ir = not isinstance(arg, Register)
				self.args.insert(0, IR(ir, "ir"))
				break

	def arguments(self):
		return dict((a.name, a.value) for a in self.args)

	def __getattr__(self, name):
		for arg in self.args:
			if arg.name == name:
				return arg
		raise AttributeError("'Instruction' object has no attribute '%s'" % name)

	def __str__(self):
		import encoding # import late to avoid circular imports
		args = dict((a.name, a) for a in self.args)
		code = encoding.encoding(self)
		return code["format"].format(**args)

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
			bytes.append(byte)
			n >>= 8
			size -= 1
		return "0x" + "".join(reversed(bytes))

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
		self.value = self.number.value
	
	def binary(self):
		return isa.immediates[self.number.value]

	def __str__(self):
		return str(self.number.value)

	def __repr__(self):
		return "<Imm %d>" % self.number.value


class Condition(Token):
	def __init__(self, value, name):
		self.value = value
		self.name = name
	
	def binary(self):
		return isa.conditions[self.value]

	def __str__(self):
		return self.value

	def __repr__(self):
		return "<Cond %s>" % self.value


class Macro(Token):
	def __init__(self, *args, **kwargs):
		self.name = args[0]
		self.args = args[1:]
		self.callback = kwargs["callback"]
	
	def __str__(self):
		if self.args:
			args = " " + ", ".join(["%s=%s" % (a.name,repr(a)) for a in self.args])
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
		self.size = self.bits / 8
		self.size += 1 if self.bits % 8 else 0
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
		if   op == "~": res = ~op1
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
