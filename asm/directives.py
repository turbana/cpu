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


# the following macros don't have a body as the Macro object itself is used as
# a placeholder during expansion

@macro
def text(pos):
	pass


@macro
def data(pos):
	pass
