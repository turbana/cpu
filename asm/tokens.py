# this is set by isa.py to give us a reference to the encodings
#encodings = None

import re

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
		if self.direction is not None:
			return self.value + self.direction
		return self.value

	def __repr__(self):
		if self.direction:
			return "<Label %s %s>" % (repr(self.value), self.direction)
		elif self.pos >= 0:
			return "<Label %s @%d>" % (repr(self.value), self.pos)
		return "<Label %s>" % repr(self.value)


class Instruction(Token):
	def __init__(self, *args, **kwargs):
		self.name = args[0]
		self.args = list(args[1:])
		self.size = 2
		self._arguments = {a.name:a for a in self.args}

	def arguments(self):
		return self._arguments

	def __getattr__(self, name):
		for arg in self.args:
			if arg.name == name:
				return arg
		raise AttributeError("'Instruction' object has no attribute '%s'" % name)

	def __str__(self):
		import encoding # import late to avoid circular imports
		code = encoding.encoding(self)
		types = code["types"]
		args = dict((a.name, pretty_print(a, types.get(a.name, ""))) for a in self.args)
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
		return str(self.value)

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
	def __init__(self, reg, name=""):
		self.name = name
		self.value = reg

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


class ImmRegister(Token):
	def __init__(self, value, name="", decode=False):
		self.name = name
		if decode:
			self.imm = (value & 1) == 1
			value >>= 1
			if self.imm:
				imm = isa.immediates_rev[value]
				num = Number((imm, 10), 5, True)
				self.value = Immediate(num, name)
			else:
				self.value = Register(value & 0x07, name)
		else:
			self.imm = isinstance(value, Immediate)
			self.value = value

	def binary(self):
		return (self.value.binary() << 1) | (1 if self.imm else 0)

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return "<IReg %s>" % repr(self.value)


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


class Bit(Token):
	def __init__(self, value, name=""):
		self.value = True if value else False
		self.name = name

	def binary(self):
		return 1 if self.value else 0

	def __str__(self):
		return "<Bit %d>" % self.value
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
			op1 = 0
			op, op2 = self.args
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
		if   op == "~": res = ~op2
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
		if self._value is not None:
			return str(self._value)
		return "(" + " ".join(map(str, self.args)) + ")"

	def __repr__(self):
		self._evaluate()
		sign = "s" if self.signed else "u"
		val = self._value if self._value is not None else self.args
		return "<Expr %s%s %s>" % (sign, self.bits, val)


_number = re.compile("^(s|u)[0-9]")
def pretty_print(arg, type):
	if isinstance(arg, Number) and _number.match(type):
		signed = type[0] == "s"
		bits = int(type[1:])
		n = arg.value
		return (n - (2**bits)) if n >= (2**(bits-1)) else n
	return arg
