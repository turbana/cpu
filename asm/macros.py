import inspect

import tokens


macros = []


def macro(arg):
	def add_macro(func, name, format):
		fargs = inspect.getargspec(func).args
		syntax = ".%s " % name
		if format:
			syntax += " , ".join("%s:%s" % (n,t) for n,t in zip(fargs, format.split()))
		def macro_wrapper(*args):
			res = func(*args)
			if isinstance(res, str):
				res = res.format(**dict(zip(fargs, args)))
			return res
		macros.append((syntax, macro_wrapper))
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

@macro
def text():
	pass


@macro
def data():
	pass


@macro("u16")
def org(target):
	pass


@macro("u16")
def align(n):
	pass


@macro("iden u16")
def set(name, val):
	pass


#
# Macros
#

@macro("u16+")
def dw(words):
	return [tokens.Expression([word, "+", 0], name=".dw", bits=16, signed=False)
			for word in words]

@macro("string")
def ascii(string):
	return dw(map(ord, string))


@macro("u16")
def zero(count):
	words = count.value
	return [tokens.Number((0, 10), bits=16, signed=False) for _ in range(words)]


@macro("reg s16")
def ldi(reg, imm):
	return """
		lui  {reg}, (({imm.value} & 0xFF00) >> 8) + (({imm.value} & 0x0080) >> 7)
		addi {reg}, ({imm.value} & 0x00FF)
	"""


@macro("reg")
def push(reg):
	return """
		sub $7, $7, 1
		stw 0($7), {reg}
	"""


@macro("reg")
def pop(reg):
	return """
		ldw	{reg}, 0($7)
		add $7, $7, 1
	"""


@macro("u16")
def call(addr):
	return """
		sub $7, $7, 1
		stw 0($7), $6
		lcr $6, $cr0
		jmp {addr}
		ldw $6, 0($7)
		add $7, $7, 1
	"""


@macro("u8")
def enter(words):
	# XXX figure out immediate value
	return """
		sub  $7, $7, 1
		stw  0($7), $6
		add  $6, $7, 1
		addi $7, -{words.value}
	"""


@macro
def leave():
	return """
		add $7, $0, $6
		ldw $6, -1($6)
		jmp $6
	"""
