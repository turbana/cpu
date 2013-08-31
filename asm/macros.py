from directives import macro
import isa


@macro("u8")
def zero(pos, count):
	words = count.value
	return [isa.Number(n=0, base=10, bits=16*words, signed=False)]
