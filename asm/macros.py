from directives import macro
import isa


@macro("u16")
def zero(pos, count):
	words = count.value
	return [isa.Number((0, 10), bits=16*words, signed=False)]


@macro("reg s16")
def ldi(pos, reg, imm):
	return """
		lui  {reg}, (({imm} & 0xFF00) >> 8)
		addi {reg}, ({imm} & 0x00FF)
	""".format(reg=reg, imm=imm.value)


@macro("reg")
def push(pos, reg):
	return """
		sub $6, $6, 1
		stw 0($6), {reg}
	""".format(reg=reg)


@macro("reg")
def pop(pos, reg):
	return """
		ldw	{reg}, 0($6)
		add $6, $6, 1
	""".format(reg=reg)


@macro("u16")
def call(pos, addr):
	return """
		.ldi  $5, {pc}
		.push $5
		jmp   {addr}
	""".format(addr=addr.value, pc=pos+5)


@macro
def ret(pos):
	return """
		.pop $5
		jmp  $5
	"""
