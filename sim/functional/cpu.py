import inspect
import collections

import sys
import asm.encoding

PC = 8 # register

class globals(object):
	trace = True
	step  = False
	mem_range = [0x00, 0x40]
	breakpoints = []
	break_clock = 1000

def sbin(n, x=0):
	return bin(n)[2:].zfill(z)
def shex(n, x=0):
	return hex(n)[2:].upper().zfill(x)
def num(s):
	return int(s.replace(" ", ""), 2)
def twoc_unsign(n, bits=16):
	return ((2**bits) + n) if n < 0 else n
def twoc_sign(n):
	return (n - (2**16)) if n >= (2**15) else n


condition_func = {
	"eq":	lambda x, y: twoc_sign(x) == twoc_sign(y),
	"ne":	lambda x, y: twoc_sign(x) != twoc_sign(y),
	"lt":	lambda x, y: twoc_sign(x) <  twoc_sign(y),
	"lte":	lambda x, y: twoc_sign(x) <= twoc_sign(y),
	"gt":	lambda x, y: twoc_sign(x) >  twoc_sign(y),
	"gte":	lambda x, y: twoc_sign(x) >= twoc_sign(y),
	"ult":	lambda x, y: twoc_unsign(x) < twoc_unsign(y),
	"ulte":	lambda x, y: twoc_unsign(x) <= twoc_unsign(y),
}

def traceop(tok):
	if globals.trace:
		print tok

def trace(*msg):
	if globals.trace:
		print " ".join(map(str, msg))


operations = collections.defaultdict(list)

def op(func):
	name = func.func_name
	if name.endswith("_"):
		name = name[:-1]
	name = name.replace("_", ".")
	operations[name].append(func)
	return func

def lookup_op(tok):
	argnames = sorted(tok.arguments().keys())
	for func in operations[tok.name]:
		fargs = inspect.getargspec(func).args[1:]
		if sorted(fargs) == argnames:
			return func
	raise Exception("%s not defined" % tok.name)

@op
def ldw(cpu, tgt, base, offset):
	cpu.rset(tgt, cpu.mget((cpu.rget(base) + offset) * 2))

@op
def ldw(cpu, tgt, base, index):
	cpu.rset(tgt, cpu.mget((cpu.rget(base) + cpu.rget(index)) * 2))

@op
def ldb(cpu, tgt, base, offset):
	cpu.rset(tgt, cpu.mget(cpu.rget(base) + offset) >> 8)

@op
def ldb(cpu, tgt, base, index):
	cpu.rset(tgt, cpu.mget(cpu.rget(base) + cpu.rget(index)) >> 8)

@op
def stw(cpu, base, src, offset):
	cpu.mset((offset + cpu.rget(base)) * 2, cpu.rget(src))

@op
def stw(cpu, base, src, index):
	cpu.mset((cpu.rget(index) + cpu.rget(base)) * 2, cpu.rget(src))

@op
def stb(cpu, base, src, offset):
	cpu.mset(offset + cpu.rget(base), cpu.rget(src) & 0xFF, byte=True)

@op
def stb(cpu, base, src, index):
	cpu.mset(cpu.rget(index) + cpu.rget(base), cpu.rget(src) & 0xFF, byte=True)

@op
def jmp(cpu, offset):
	cpu.reg[PC] += offset + 1

@op
def jmp(cpu, tgt):
	cpu.reg[PC] = cpu.rget(tgt)

@op
def add(cpu, tgt, op1, op2, ir):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	res = op1 + op2
	# TODO check for overflow
	cpu.rset(tgt, res & 0xFFFF)

@op
def sub(cpu, tgt, op1, op2, ir):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	res = op1 - op2
	# TODO check for underflow
	cpu.rset(tgt, res)

@op
def and_(cpu, tgt, op1, op2, ir):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	cpu.rset(tgt, op1 & op2)

@op
def or_(cpu, tgt, op1, op2, ir):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	cpu.rset(tgt, op1 | op2)

@op
def xor(cpu, tgt, op1, op2, ir):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	cpu.rset(tgt, op1 ^ op2)

@op
def s(cpu, cond, op1, op2, ir):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	func = condition_func[cond]
	if func(op1, op2):
		cpu.reg[PC] += 1

@op
def as_z(cpu, ir, op1, op2, tgt):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	# TODO check for overflow
	res = (op1 + op2) & 0xFFFF
	cpu.rset(tgt, res)
	if res == 0:
		cpu.reg[PC] += 1

@op
def as_nz(cpu, ir, op1, op2, tgt):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	res = op1 + op2
	cpu.rset(tgt, res)
	if res != 0:
		cpu.reg[PC] += 1

@op
def lui(cpu, imm, tgt):
	imm = twoc_unsign(imm, 8)
	cpu.rset(tgt, imm << 8)

@op
def addi(cpu, imm, tgt):
	imm = twoc_unsign(imm)
	# TODO check overflow
	cpu.rset(tgt, cpu.rget(tgt) + imm)

@op
def shl(cpu, src, tgt):
	n = (cpu.rget(src) << 1) & 0xFFFF
	cpu.rset(tgt, n)

@op
def shr(cpu, src, tgt):
	n = (cpu.rget(src) >> 1) & 0xFFFF
	cpu.rset(tgt, n)

@op
def sar(cpu, src, tgt):
	n = cpu.rget(src)
	msb = n & 0x8000
	shr = (n >> 1) & 0xFFFF
	cpu.rset(tgt, shr | msb)

@op
def xor(cpu, tgt, src):
	cpu.rset(tgt, cpu.rget(tgt) ^ cpu.rget(src))

@op
def not_(cpu, tgt, src):
	cpu.rset(tgt, cpu.rget(src) ^ 0xFFFF)

@op
def halt(cpu):
	cpu.halt = True

@op
def trap(cpu, int):
	raise NotImplementedError()

@op
def sext(cpu, tgt, src):
	val = cpu.rget(src)
	if val & 0x80:
		val |= 0xFF00
	else:
		val &= 0x00FF
	cpu.rset(tgt, val)

@op
def lcr(cpu, tgt, cr):
	cpu.rset(tgt, cpu.crget(cr))

@op
def scr(cpu, cr, src):
	cpu.crset(cr, cpu.rget(src))


class CPU(object):
	def __init__(self):
		self.reg  = [0 for _ in xrange(10)]
		self.mem  = [0 for _ in xrange(2**17)]
		self.halt = True
		self.clock = 0
	
	def load(self, data):
		for i, n in enumerate(data):
			self.mem[i] = n
	
	def dump(self, mstart=None, mend=None):
		def hex_word(n):
			h = hex(n)[2:].upper().zfill(4)
			return h
		def hex_byte(n):
			return hex(n)[2:].upper().zfill(2)
		def bin_word(n):
			b = bin(n)[2:].zfill(16)
			return "%s %s  %s %s" % (b[0:4], b[4:8], b[8:12], b[12:16])
		print
		print " "*40 + "clock:", self.clock
		for r in xrange(1, 10):
			v = self.reg[r]
			name = ("  $%d" % r) if r < 8 else ("$cr%d" % (r-8))
			print "%s:  %s  |  %s  =  %5s" % (name, bin_word(v), hex_word(v), v)
		if mstart is not None and mend is not None:
			count = 0
			for addr in xrange(mstart*2, mend*2, 2):
				if not count:
					print "\n%s | " % hex_word(addr/2),
				word = (self.mem[addr] << 8) | self.mem[addr+1]
				print hex_word(word),
				count = (count + 1) % 8
			print
			print
	
	def run(self):
		self.halt = False
		while not self.halt:
			self.clock += 1
			if self.reg[PC] in globals.breakpoints or self.clock == globals.break_clock:
				globals.trace = False
				globals.step = True
			opcode = self.fetch()
			tok = asm.encoding.decode(opcode)
			if globals.step:
				self.dump(*globals.mem_range)
				print "%s> %s" % (shex(self.reg[PC]-1, 4), str(tok)),
				raw_input()
				print
			func = lookup_op(tok)
			func(self, **tok.arguments())
	
	def fetch(self):
		pc = self.reg[PC]
		self.reg[PC] = pc + 1
		return self.mget(pc * 2)
	
	def mget(self, addr):
		high = self.mem[addr]
		low = self.mem[addr + 1]
		byte = (high << 8) | low
		trace("  read  (%s) : %s" % (shex(addr, 4), shex(byte, 4)))
		return byte

	def mset(self, addr, val, byte=False):
		high = (val & 0xFF) if byte else (val >> 8)
		low  = 0            if byte else (val & 0xFF)
		trace("  write (%s) : %s%s" % (shex(addr, 4), shex(high, 2), shex(low, 2)))
		self.mem[addr] = high
		if not byte:
			self.mem[addr + 1] = low
	
	def rget(self, reg):
		return self.reg[reg]

	def rset(self, reg, value):
		if reg != 0:
			self.reg[reg] = value

	def crget(self, cr):
		val = self.reg[8 + cr]
		if cr == 0: val += 1
		return val

	def crset(self, reg, value):
		raise NotImplementedError()



def main(args):
	if len(args) != 1:
		print "USAGE: %s binary" % sys.argv[0]
		return 2
	data = map(ord, open(args[0], "rb").read())
	cpu = CPU()
	cpu.load(data)
	globals.mem_range[1] = (len(data)/2) + (len(data)%2)
	cpu.dump(*globals.mem_range)
	try:
		cpu.run()
		cpu.dump(*globals.mem_range)
	except KeyboardInterrupt:
		print
		return 0

if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
