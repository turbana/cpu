import inspect

import tokens


macros = []


def macro(arg):
	def add_macro(func, name, format):
		fargs = inspect.getargspec(func).args[1:]
		syntax = ".%s " % name
		if format:
			syntax += " , ".join("%s:%s" % (n,t) for n,t in zip(fargs, format.split()))
		macros.append((syntax, func))
	if hasattr(arg, "__call__"):
		add_macro(arg, arg.func_name, None)
		return arg
	def _decorator(func):
		add_macro(func, func.func_name, arg)
		return func
	return _decorator


#
# Directives
#

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
		return [tokens.Number(n=0, base=10, bits=8*offset, signed=False)]
	return []


# the following macros don't have a body as the Macro object itself is used as
# a placeholder during expansion

@macro
def text(pos):
	pass


@macro
def data(pos):
	pass



#
# Macros
#


@macro("u16")
def zero(pos, count):
	words = count.value
	return [tokens.Number((0, 10), bits=16*words, signed=False)]


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
