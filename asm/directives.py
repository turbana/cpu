import isa
from grammer import macro


@macro("u8")
def db(pos, b):
	return [b]


@macro("u16")
def dw(pos, w):
	return [w]


@macro("u16")
def align(pos, n):
	offset = n.value - (pos % n.value)
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
