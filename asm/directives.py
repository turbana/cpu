import tokens
import grammer as g

macros = []


def macro(arg):
	def add_macro(func, name, format):
		grammer = _build_grammer(name, format)
		def build_macro(s, l, t):
			return tokens.Macro(name, func, t[1:])
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
	unumber = g.Suppress("u") + g.num
	snumber = g.Suppress("s") + g.num
	unumber.setParseAction(lambda s,l,t: g.unsigned_num(t[0]))
	snumber.setParseAction(lambda s,l,t: g.signed_num(t[0]))
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
	offset = n.n - (pos % n.n)
	if offset != n.n:
		return [tokens.Number(n=0, base=10, bits=8*offset, signed=False)]
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
	""".format(imm=x.n)


#print macros
