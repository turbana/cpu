from directives import macro
import isa


@macro("u8")
def zero(pos, count):
	words = count.value
	return [isa.Number((0, 10), bits=16*words, signed=False)]


@macro("reg u16")
def ldi(pos, reg, imm):
	return """
		lui  {reg}, (({imm} & 0xFF00) >> 8)
		addi {reg}, ({imm} & 0x00FF)
	""".format(reg=reg, imm=imm.value)
