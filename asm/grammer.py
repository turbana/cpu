from pyparsing import *

import tokens
import macros
import isa


# pyparsing does magic when calling parse actions that I do not want happening.
# It tries to guess how many parameters a function has by calling it again with
# a different number of parameters when an exception is raised. Unfortunately this
# masks any exception the function would otherwise raise. This disables that.
def _no_trim_arity(func, maxargs=None):
	return func
import pyparsing
pyparsing._trim_arity = _no_trim_arity


#
# ISA Grammer
#

colon = Literal(":")
dot = Literal(".")
lparen = Literal("(")
rparen = Literal(")")
comma = Literal(",")

unsigned = "u1 u2 u3 u4 u5 u6 u7 u8 u9 u10 u11 u12 u13 u14 u15 u16 "
signed   = "s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 s14 s15 s16 "
atoms = (signed + unsigned + "reg ireg creg cond z nz").split()

name = Word(alphas, alphanums)
inst_name = Combine(Optional(dot) + name + Optional(dot + oneOf(["z", "nz"])))
boundry = lparen | rparen | comma
arg_type = oneOf(atoms)
arg = Group(name + Suppress(colon) + arg_type)
args = OneOrMore(Optional(boundry) + arg + Optional(boundry))
modifier = dot + arg
inst = (inst_name + modifier) | inst_name

instruction = inst + Optional(args)



#
# Assembler Grammer
#

sign = Optional(Word("-+", exact=1))

to_base = lambda b: lambda s,l,t: (int(t[0], b), b)
num_bin = Suppress("b") + Word("01")
num_oct = Combine(sign + Word("0", "0123456"))
num_dec = Combine(sign + Word("123456789", nums))
num_hex = Suppress("0x") + Word(srange("[0-9a-fA-F]"))
num_bin.setParseAction(to_base(2))
num_oct.setParseAction(to_base(8))
num_dec.setParseAction(to_base(10))
num_hex.setParseAction(to_base(16))
num = (num_hex | num_bin | num_oct | num_dec)

to_int = lambda s,l,t: int("".join(t))

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

label_name = (Word(nums) + Word("fb", exact=1)) | Word(alphanums + "_")
label_name.setName("label")

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
	def inner(s, l, t):
		if isinstance(t, ParseResults):
			return [to_lists(s, l, tok) for tok in t]
		return t
	return inner(s, l, t)
expr.setParseAction(to_lists)
expr.setName("expr")


def number(bits, signed):
	n = num.copy().addParseAction(_build(tokens.Number, bits=bits, signed=signed))
	e = expr.copy().addParseAction(_build(tokens.Expression, bits=bits, signed=signed))
	return n ^ label_name ^ e

def _check_range(s, l, t):
	obj = t[0].value if isinstance(t[0], tokens.Expression) else t[0]
	if obj is None or obj.value not in [8,4,2,1,-1,-2,-4,-8]:
		raise ParseException(s, l, "Invalid value for spec immediate")
	return tokens.Immediate(obj)
spec_imm = number(5, True).addParseAction(_check_range)


#

label = label_name + colon
reg = Suppress("$") + Word("01234567").setParseAction(to_int)
ireg = reg | spec_imm
creg = Suppress("$cr") + Word("01").setParseAction(to_int)
cond = oneOf("eq ne gt gte lt lte ult ulte")("cond")

u1  = number( 1, False)
u2  = number( 2, False)
u3  = number( 3, False)
u4  = number( 4, False)
u5  = number( 5, False)
u6  = number( 6, False)
u7  = number( 7, False)
u8  = number( 8, False)
u9  = number( 9, False)
u10 = number(10, False)
u11 = number(11, False)
u12 = number(12, False)
u13 = number(13, False)
u14 = number(14, False)
u15 = number(15, False)
u16 = number(16, False)
s1  = number( 1, True)
s2  = number( 2, True)
s3  = number( 3, True)
s4  = number( 4, True)
s5  = number( 5, True)
s6  = number( 6, True)
s7  = number( 7, True)
s8  = number( 8, True)
s9  = number( 9, True)
s10 = number(10, True)
s11 = number(11, True)
s12 = number(12, True)
s13 = number(13, True)
s14 = number(14, True)
s15 = number(15, True)
s16 = number(16, True)

comment = ";" + restOfLine

# actions

creg.addParseAction(_build(tokens.ControlRegister))
reg.addParseAction(_build(tokens.Register))
cond.addParseAction(_build(tokens.Condition))
label_name.addParseAction(_build(tokens.Label))



def parse_ast(syntax):
	try:
		return instruction.parseString(syntax, parseAll=True)
	except (ParseException, ParseFatalException), err:
		print err.line
		print " "*(err.column-1) + "^"
		print err
		raise


def build_grammer(ast):
	""" convert parsed instruction format into pyparsing grammer """
	# ex: ['ldw', ['tgt', 'reg'], ',', ['offset', 's7'], '(', ['base', 'reg'], ')']
	def lookup(name, type):
		g = globals()[type].setResultsName(name).setName(name)
		def setname(s, l, t):
			t[0].name = name
			t[0].type = type
		g.addParseAction(setname)
		return g
	def punct(c):
		return Suppress(c).setResultsName(c).setName(c)
	if isinstance(ast[0], str):
		g = Literal(ast[0]).setResultsName(ast[0]).setName(ast[0])
	for arg in ast[1:]:
		g += punct(arg) if isinstance(arg, str) else lookup(*arg)
	return g


def add_instruction(syntax, token_type, kwargs={}):
	ast = parse_ast(syntax)
	g = build_grammer(ast)
	g.addParseAction(_build(token_type, **kwargs))
	instructions.append(g)
	return ast


def join_grammer(gs):
	g = gs[0]
	for ng in gs[1:]:
		g |= ng
	return g


def build_instruction_grammers():
	g = []
	for encoding in isa.encodings:
		if encoding["ast"]:
			g.append(encoding["grammer"])
			continue
		ast = parse_ast(encoding["syntax"])
		inst = build_grammer(ast)
		inst.addParseAction(_build(tokens.Instruction))
		types = dict(a for a in ast[1:] if not isinstance(a, str))
		format = isa.parse_format(ast)
		encoding["ast"] = ast
		encoding["grammer"] = inst
		encoding["types"] = types
		encoding["format"] = format
		g.append(inst)
	return join_grammer(g)


def build_macro_grammers():
	g = []
	for syntax, func in macros.macros:
		ast = parse_ast(syntax)
		macro = build_grammer(ast)
		macro.addParseAction(_build(tokens.Macro, callback=func))
		g.append(macro)
	return join_grammer(g)


def grammer(_cache=[None]):
	if _cache[0]:
		return _cache[0]
	instruction = build_instruction_grammers()
	instruction |= build_macro_grammers()
	line = (label + instruction) | instruction | label
	g = OneOrMore(line)
	g.ignore(comment)
	_cache[0] = g
	return g
