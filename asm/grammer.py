from pyparsing import *
import isa


sign = Optional(Word("-+", exact=1))

to_base = lambda b: lambda s,l,t: (int(t[0], b), b)
num_bin = Suppress("b") + Word("01")
num_oct = Combine(sign + Word("0", nums))
num_dec = Combine(sign + Word("123456789", nums))
num_hex = Suppress("0x") + Word(srange("[0-9a-fA-F]"))
num_bin.setParseAction(to_base(2)).setName("num_bin")
num_oct.setParseAction(to_base(8)).setName("num_oct")
num_dec.setParseAction(to_base(10)).setName("num_dec")
num_hex.setParseAction(to_base(16)).setName("num_hex")
num = (num_hex | num_bin | num_oct | num_dec)
num.setName("num")

to_int = lambda s,l,t: int("".join(t))
def replace(what):
	return lambda s,l,t: [what] + t[1:]

def _build(typ, **kwargs):
	def _parse_action(s, l, toks):
		name = toks.keys()[0] if toks.keys() else ""
		kwargs["name"] = name
		return typ(*toks, **kwargs)
	return _parse_action


# puncuation
comma = Suppress(",").setName("comma")
colon = Suppress(":").setName("colon")
lparen = Suppress("(").setName("lparen")
rparen = Suppress(")").setName("rparen")
dot = Suppress(".").setName("dot")

# values
reg = Suppress("$") + Word("01234567").setParseAction(to_int)
reg.setName("reg")
reg.setParseAction(_build(isa.Register))
lnum = Word(nums).setParseAction(to_int)
lnum.setName("lnum")
label_name = (lnum + Optional(Word("fb", exact=1))) | Word(alphanums)
label_name.setParseAction(_build(isa.Label))
label_name.setName("label_name")
label = label_name + colon
label.setName("label")
spec_imm = Combine(sign + Word("1248", exact=1))
spec_imm.setParseAction(to_int)
spec_imm.addParseAction(_build(isa.Immediate))
spec_imm.setName("spec_imm")

# expressions
bin_op = oneOf("<< >> **") | Word("+-*/%&^|", exact=1)
bin_op.setName("bin_op")
unary_op = Word("~", exact=1)
unary_op.setName("unary_op")
_just_int_value = lambda s,l,t: t[0][0]
expr_num = num.copy().addParseAction(_just_int_value)
expr_num.setName("expr_num")

expr = Forward()
operand = expr_num | label_name | expr
operand.setName("operand")

bin_expr_val = Group(operand + bin_op + operand)
bin_expr_val.setName("bin_expr_val")
bin_expr = (lparen + bin_expr_val + rparen) | bin_expr_val
bin_expr.setName("bin_expr")

unary_expr_val = Group(unary_op + operand)
unary_expr_val.setName("unary_expr_val")
unary_expr = (lparen + unary_expr_val + rparen) | unary_expr_val
unary_expr.setName("unary_expr")

expr <<= unary_expr | bin_expr
expr.setName("expr")

def to_lists(s, l, t):
	if isinstance(t, ParseResults):
		return [to_lists(s, l, tok) for tok in t]
	return t
expr.setParseAction(to_lists)

def number(bits, signed):
	n = num.copy().setParseAction(_build(isa.Number, bits=bits, signed=signed))
	e = expr.copy().addParseAction(_build(isa.Expression, bits=bits, signed=signed))
	return n | e

def name(grammer, name):
	grammer = grammer.setResultsName(name)
	def set_name(s, l, toks):
		name = toks.keys()[0] if toks.keys() else ""
		toks[0].name = name
	return grammer.addParseAction(set_name).setName(name)


# numbers
s7  = number( 7,  True).setName("s7")
s8  = number( 8,  True).setName("s8")
s13 = number(13,  True).setName("s13")
u4  = number( 4, False).setName("u4")

#
offset = (name(reg, "index") | name(s7, "offset") | name(label_name, "offset"))
offset.setName("offset")
tgt = name(reg, "tgt")
src = name(reg, "src")
base = name(reg, "base")
op1 = name(reg, "op1")
op2 = name(reg, "op2")

reg_imm = op2 | name(spec_imm, "op2")
reg_imm.setName("reg_imm")
reg3_imm = tgt + comma + op1 + comma + reg_imm
reg3_imm.setName("reg3_imm")
jmp_target = (name(reg, "tgt") | name(s13, "offset") | name(label_name, "offset"))
jmp_target.setName("jmp_target")
imm8 = (name(s8, "imm") | name(label_name, "imm"))
imm8.setName("imm8")
count = name(u4, "count")
sysnum = name(u4, "sysnum")

condition = oneOf("eq ne gt gte lt lte ult ulte")("cond")
condition.setParseAction(_build(isa.Condition))
condition.setName("condition")

comment = ";" + restOfLine
comment.setName("comment")
