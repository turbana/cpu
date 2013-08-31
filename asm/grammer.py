from pyparsing import *
import isa


sign = Optional(Word("-+", exact=1))

to_base = lambda b: lambda s,l,t: (int(t[0], b), b)
num_bin = Suppress("b") + Word("01")
num_oct = Combine(sign + Word("0", nums))
num_dec = Combine(sign + Word("123456789", nums))
num_hex = Suppress("0x") + Word(srange("[0-9a-fA-F]"))
num_bin.setParseAction(to_base(2))
num_oct.setParseAction(to_base(8))
num_dec.setParseAction(to_base(10))
num_hex.setParseAction(to_base(16))
num = (num_hex | num_bin | num_oct | num_dec)

def number(bits, signed):
	def _parse_action(s, l, toks):
		name = toks.keys()[0] if toks.keys() else ""
		value, base = toks[0]
		try:
			return isa.Number(value, base, bits, signed, name)
		except ValueError, e:
			raise ParseFatalException(s, l, str(e))
	return num.copy().setParseAction(_parse_action)

to_int = lambda s,l,t: int("".join(t))
def replace(what):
	return lambda s,l,t: [what] + t[1:]

def _build(type):
	def _parse_action(s, l, toks):
		name = toks.keys()[0] if toks.keys() else ""
		return type(*toks, name=name)
	return _parse_action


# puncuation
comma = Suppress(",")
colon = Suppress(":")
lparen = Suppress("(")
rparen = Suppress(")")

# numbers
s7 = number(7, True)
s8 = number(8, True)
s13 = number(13, True)
u4 = number(4, False)

# values
reg = Suppress("$") + Word("01234567").setParseAction(to_int)
reg.setName("register")
reg.setParseAction(_build(isa.Register))
num = Word(nums).setParseAction(to_int)
label_name = (num + Optional(Word("fb", exact=1))) | Word(alphanums)
label_name.setName("label")
label_name.setParseAction(isa.Label)
label = label_name + colon
spec_imm = Combine(sign + Word("1248", exact=1))
spec_imm.setParseAction(to_int)
spec_imm.addParseAction(_build(isa.Immediate))

offset = (s7("offset") | reg("index"))
tgt = reg("tgt")
src = reg("src")
base = reg("base")
op1 = reg("op1")
op2 = reg("op2")

reg_imm = op2 | spec_imm("op2")
reg3_imm = tgt + comma + op1 + comma + reg_imm

condition = oneOf("eq ne gt gte lt lte ult ulte")("cond")
condition.setParseAction(_build(isa.Condition))

comment = ";" + restOfLine
