from pyparsing import *
import isa

# pyparsing does magic when calling parse actions that I do not want happening.
# It tries to guess how many parameters a function has by calling it again with
# a different number of parameters when an exception is raised. Unforunatly this
# masks any exception the function would otherwise raise. This disables that.
def _no_trim_arity(func, maxargs=None):
	return func
import pyparsing
pyparsing._trim_arity = _no_trim_arity


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
comma = Suppress(",")
colon = Suppress(":")
lparen = Suppress("(")
rparen = Suppress(")")
dot = Suppress(".")

# values
reg = Suppress("$") + Word("01234567").setParseAction(to_int)
reg.setName("register")
reg.setParseAction(_build(isa.Register))
lnum = Word(nums).setParseAction(to_int)
label_name = (lnum + Word("fb", exact=1)) | Word(alphas, alphanums)
label_name.setName("label")
label_name.setParseAction(_build(isa.Label))
label = label_name + colon
spec_imm = Combine(sign + Word("1248", exact=1))
spec_imm.setParseAction(to_int)
spec_imm.addParseAction(_build(isa.Immediate))


_just_int_value = lambda s,l,t: t[0][0]
expr_num = num.copy().addParseAction(_just_int_value)
operand = expr_num | label_name

expr = operatorPrecedence(operand, [
	(oneOf("~"), 1, opAssoc.RIGHT),
	(oneOf("* /"), 2, opAssoc.LEFT),
	(oneOf("<< >> **"), 2, opAssoc.LEFT),
	(oneOf("+ -"), 2, opAssoc.LEFT),
	(oneOf("% & ^ |"), 2, opAssoc.LEFT),
])

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
	return grammer.addParseAction(set_name)


# numbers
s7  = number( 7,  True)
s8  = number( 8,  True)
s13 = number(13,  True)
u4  = number( 4, False)

#
offset = (name(label_name, "offset") ^ name(reg, "index") ^ name(s7, "offset"))
tgt = name(reg, "tgt")
src = name(reg, "src")
base = name(reg, "base")
op1 = name(reg, "op1")
op2 = name(reg, "op2")

reg_imm = op2 | name(spec_imm, "op2")
reg3_imm = tgt + comma + op1 + comma + reg_imm
jmp_target = (name(label_name, "offset") | name(reg, "tgt") | name(s13, "offset"))
imm8 = (name(label_name, "imm") | name(s8, "imm"))
count = name(u4, "count")
sysnum = name(u4, "sysnum")

condition = oneOf("eq ne gt gte lt lte ult ulte")("cond")
condition.setParseAction(_build(isa.Condition))

comment = ";" + restOfLine

ldw = Literal("ldw") + tgt + comma + offset + lparen + base + rparen
ldb = Literal("ldb") + tgt + comma + offset + lparen + base + rparen
stw = Literal("stw") + offset + lparen + base + rparen + comma + src
stb = Literal("stb") + offset + lparen + base + rparen + comma + src

jmp = Literal("jmp") + jmp_target

add = Literal("add") + reg3_imm
sub = Literal("sub") + reg3_imm
and_i = Literal("and") + reg3_imm
or_i = Literal("or") + reg3_imm
addskipz = Literal("as.z") + reg3_imm
addskipnz = Literal("as.nz") + reg3_imm

skip = Literal("s") + dot + condition + op1 + comma + reg_imm

lui = Literal("lui")   + tgt + comma + imm8
addi = Literal("addi") + tgt + comma + imm8

shl = Literal("shl") + tgt + comma + src + comma + count
shr = Literal("shr") + tgt + comma + src + comma + count

xor = Literal("xor")   + tgt + comma + src
not_i = Literal("not") + tgt + comma + src

halt = Literal("halt")
trap = Literal("trap") + sysnum
sext = Literal("sext") + tgt

instruction = ldw | ldb | stw | stb | jmp | add | sub | and_i | or_i | skip | addskipz
instruction |= addskipnz | lui | addi | shl | shr | xor | not_i | halt | trap | sext
instruction.setParseAction(lambda s,l,t: isa.Instruction(t[0], t[1:]))


def grammer(_cache=[None]):
	if _cache[0]:
		return _cache[0]
	macro = _macros_grammer()
	line = Optional(label) + (instruction | macro)
	g = OneOrMore(line)
	g.ignore(comment)
	_cache[0] = g
	return g


#
# Macros
#

_macros = []

def macro(arg):
	def add_macro(func, name, format):
		try:
			grammer = _build_macro_grammer(name, format)
		except (ParseException, ParseFatalException), err:
			print err.line
			print " "*(err.column-1) + "^"
			print err
			print "Error encountered while parsing macro definition for", name
			import sys
			sys.exit(1)
		def build_macro(s, l, t):
			return isa.Macro(name, func, t[1:])
		grammer.setParseAction(build_macro)
		_macros.append(grammer)
	if hasattr(arg, "__call__"):
		add_macro(arg, arg.func_name, None)
		return arg
	def _decorator(func):
		add_macro(func, func.func_name, arg)
		return func
	return _decorator


def _macros_grammer():
	gram = _macros[0]
	for m in _macros[1:]:
		gram |= m
	return gram


def _build_macro_grammer(name, format):
	name = dot + Literal(name)
	if not format:
		return name
	unumber = Suppress("u") + num_dec
	snumber = Suppress("s") + num_dec
	unumber.setParseAction(lambda s,l,t: label_name ^ number(t[0][0], False))
	snumber.setParseAction(lambda s,l,t: label_name ^ number(t[0][0], True))
	reg_macro = Literal("reg").setParseAction(lambda s,l,t: reg)
	types = unumber | snumber | reg_macro

	toks = OneOrMore(types).parseString(format, parseAll=True)
	grammer = toks[0]
	for tok in toks[1:]:
		grammer = grammer + comma + tok
	return name - grammer
