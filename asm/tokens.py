
class Token(object):
	size = 0
	args = []


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
	def __init__(self, tokens):
		self.name = tokens[0]
		self.args = tokens[1:]
		self.size = 2

		# internal translations
		is_reg = lambda i: isinstance(self.args[i], Register)
		if self.name in ("ldw", "ldb") and is_reg(1):
			self.name += ".b"
		elif self.name in ("stw", "stb") and is_reg(0):
			self.name += ".b"
		elif self.name == "jmp" and is_reg(0):
			self.name += ".r"
	
	def __str__(self):
		return "<Inst %s %s>" % (self.name, ", ".join(map(repr, self.args)))
	__repr__ = __str__


class Number(Token):
	def __init__(self, n, base, bits, signed):
		self.n = n
		self.base = base
		self.bits = bits
		self.signed = signed
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
		if self.signed and self.n < 0:
			# two's complement by subtracting from 2^n
			m = 2 ** self.bits
			return m + self.n
		return self.n
	
	def __str__(self):
		signed = "s" if self.signed else "u"
		return "<Number %d %s>" % (self.n, signed)
	__repr__ = __str__


class Register(Token):
	def __init__(self, tokens):
		self.name = int(tokens[0])
	
	def binary(self):
		return self.name
	
	def __str__(self):
		return "<Reg %s>" % repr(self.name)
	__repr__ = __str__


class Immediate(Token):
	def __init__(self, tokens):
		self.value = int("".join(tokens))
	
	def binary(self):
		m = {8: 0, 4: 1, 2: 2, 1: 3, -1: 4, -2: 5, -4: 6, -8: 7}
		return m[self.value]

	def __str__(self):
		return "<Imm %d>" % self.value
	__repr__ = __str__


class Condition(Token):
	def __init__(self, tokens):
		self.type = tokens[0]
	
	def binary(self):
		m = {"eq": 0, "ne": 1, "gt": 2, "gte": 3, "lt": 4, "lte":5, "ult": 6, "ulte": 7}
		return m[self.type]

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
