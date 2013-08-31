import isa
import grammer as g

macros = []


def macro(arg):
	def add_macro(func, name, format):
		grammer = _build_grammer(name, format)
		def build_macro(s, l, t):
			return isa.Macro(name, func, t[1:])
		grammer.setParseAction(build_macro)
		macros.append(grammer)
	if hasattr(arg, "__call__"):
		add_macro(arg, arg.func_name, None)
		return arg
	def _decorator(func):
		add_macro(func, func.func_name, arg)
		return func
	return _decorator


def grammer():
	gram = macros[0]
	for m in macros[1:]:
		gram |= m
	return gram


def _build_grammer(name, format):
	name = g.Suppress(".") + g.Literal(name)
	if not format:
		return name
	unumber = g.Suppress("u") + g.num_dec
	snumber = g.Suppress("s") + g.num_dec
	unumber.setParseAction(lambda s,l,t: g.number(t[0][0], False))
	snumber.setParseAction(lambda s,l,t: g.number(t[0][0], True))
	types = unumber | snumber

	toks = g.OneOrMore(types).parseString(format, parseAll=True)
	grammer = toks[0]
	for tok in toks[1:]:
		grammer |= tok
	return name - grammer


@macro("u8")
def db(pos, b):
	return [b]


@macro("u16")
def dw(pos, w):
	return [w]


@macro("u16")
def align(pos, n):
	offset = n.value - (pos % n.calue)
	if offset != n.value:
		return [isa.Number(n=0, base=10, bits=8*offset, signed=False)]
	return []


@macro
def text(pos):
	pass


@macro
def data(pos):
	pass


@macro("s8")
def test(pos, x):
	return """
		lui $1, {imm}
		lui $2, {imm}
		lui $3, {imm}
		lui $4, {imm}
		lui $5, {imm}
		lui $6, {imm}
		lui $7, {imm}
	""".format(imm=x.value)


#print macros
