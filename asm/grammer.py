from pyparsing import *
import tokens

def convert_signed(base, bits):
	def convert(s, loc, toks):
		val = "".join(toks)
		#if val == "-": return -1
		n = int(val, base)
		if base == 10:
			if -2**(bits-1) <= n and n <= 2**(bits-1)-1:
				return [tokens.Number(n, base, bits, signed=True)]
		elif n < 2**bits:
			return [tokens.Number(n, base, bits, signed=True)]
		raise ParseFatalException(s, loc,
			"%s out of bounds for a %d bit signed number in base %d" % (val, bits, base))
	return convert

def convert_unsigned(base, bits):
	def convert(s, loc, toks):
		n = int("".join(toks), base)
		if 0 <= n and n < 2**bits:
			return [tokens.Number(n, base, bits, signed=False)]
		raise ParseFatalException(s, loc,
			"%s out of bounds for a %d bit unsigned number in base %d" % (val, bits, base))
	return convert

def signed_num(bits):
	bin = Suppress("b") + Word("01")
	oct = sign + Word("0", nums)
	dec = sign + Word("123456789", nums)
	hex = Suppress("0x") + Word(srange("[0-9a-fA-F]"))
	bin.setParseAction(convert_signed(2, bits))
	oct.setParseAction(convert_signed(8, bits))
	dec.setParseAction(convert_signed(10, bits))
	hex.setParseAction(convert_signed(16, bits))
	return NoMatch().setName("%d-bit signed number" % bits) | (bin ^ oct ^ dec ^ hex)

def unsigned_num(bits):
	bin = Suppress("b") + Word("01")
	oct = Word("0", nums)
	dec = Word("123456789", nums)
	hex = Suppress("0x") + Word(srange("[0-9a-fA-F]"))
	bin.setParseAction(convert_unsigned(2, bits))
	oct.setParseAction(convert_unsigned(8, bits))
	dec.setParseAction(convert_unsigned(10, bits))
	hex.setParseAction(convert_unsigned(16, bits))
	return NoMatch().setName("%d-bit signed number" % bits) | (bin ^ oct ^ dec ^ hex)

to_int = lambda s,l,t: int("".join(t))
def replace(what):
	return lambda s,l,t: [what] + t[1:]

# puncuation
comma = Suppress(",")
colon = Suppress(":")
lparen = Suppress("(")
rparen = Suppress(")")

# values
sign = Optional(Word("-+", exact=1))
reg = Literal("$").suppress() + Word("01234567")
reg.setName("register")
reg.setParseAction(tokens.Register)
num = Word(nums).setParseAction(to_int)
label_name = (num + Optional(Word("fb", exact=1))) | Word(alphanums)
label_name.setName("label")
label_name.setParseAction(tokens.Label)
label = label_name + colon
spec_imm = sign + Word("1248", exact=1)
spec_imm.setParseAction(tokens.Immediate)
reg_imm = reg | spec_imm
reg3_imm = reg + comma + reg + comma + reg_imm
reg3 = reg + comma + reg + comma + reg
comment = ";" + restOfLine
condition = oneOf("eq ne gt gte lt lte ult ulte")
condition.setParseAction(tokens.Condition)

# numbers
s7 = signed_num(7)
s8 = signed_num(8)
s13 = signed_num(13)
u4 = unsigned_num(4)

