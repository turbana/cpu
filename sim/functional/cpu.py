import sys
import isa

class globals(object):
	trace = True
	step  = False
	mem_range = [0x00, 0x20]
	breakpoints = []

def sbin(n, x=0):
	return bin(n)[2:].zfill(z)
def shex(n, x=0):
	return hex(n)[2:].upper().zfill(x)
def num(s):
	return int(s.replace(" ", ""), 2)


condition_func = {
	"eq":	lambda x, y: x == y,
	"ne":	lambda x, y: x != y,
	"lt":	lambda x, y: y <  y,
	"lte":	lambda x, y: y <= x,
	"gt":	lambda x, y: y >  x,
	"gte":	lambda x, y: y >= x,
	"ult":	lambda x, y: UnimplmentedError(),
	"ulte":	lambda x, y: UnimplmentedError(),
}

def trace(name, args, kwargs):
	if globals.trace:
		items = [key+"="+str(val) for key, val in kwargs.items()]
		print "%-8s %s" % (name, " ".join(items))


operations = {}

def op(func):
	name = func.func_name
	if name.endswith("_"):
		name = name[:-1]
	name = name.replace("_", ".")
	def wrap(*args, **kwargs):
		trace(name, args, kwargs)
		return func(*args, **kwargs)
	operations[name] = wrap
	return wrap


@op
def ldw(cpu, tgt, base, offset):
	# TODO handle reg ldw
	cpu.rset(tgt, cpu.mget(cpu.rget(base) + offset))

@op
def ldb(cpu, tgt, base, offset):
	# TODO handle reg ldb
	cpu.rset(tgt, cpu.mget(cpu.rget(base) + offset) >> 8)

@op
def stw(cpu, offset, base, src):
	# TODO handle reg stw
	cpu.mset(offset + cpu.rget(base), cpu.rget(src))

@op
def stb(cpu, offset, base, src):
	# TODO handle reg stb
	cpu.mset(offset + cpu.rget(base), cpu.rget(src) & 0xFF, byte=True)

@op
def jmp(cpu, offset=None, tgt=None):
	if offset is not None:
		cpu.reg[7] += offset - 1
	elif tgt is not None:
		cpu.reg[7] = cpu.rget(tgt)

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
def s(cpu, cond, op1, op2, ir):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	func = condition_func[cond]
	if func(op1, op2):
		cpu.reg[7] += 1

@op
def as_z(cpu, ir, op1, op2, tgt):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	# TODO check for overflow
	res = (op1 + op2) & 0xFFFF
	cpu.rset(tgt, res)
	if res == 0:
		cpu.reg[7] += 1

@op
def as_nz(cpu, ir, op1, op2, tgt):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	res = op1 + op2
	cpu.rset(tgt, res)
	if res != 0:
		cpu.reg[7] += 1

@op
def lui(cpu, imm, tgt):
	imm = ((2**8) + imm) if imm < 0 else imm
	cpu.rset(tgt, imm << 8)

@op
def addi(cpu, imm, tgt):
	imm = ((2**8) + imm) if imm < 0 else imm
	cpu.rset(tgt, cpu.rget(tgt) + imm)

@op
def shl(cpu, count, src, tgt):
	cpu.rset(tgt, cpu.rget(src) >> count)

@op
def shr(cpu, count, src, tgt):
	cpu.rset(tgt, cpu.rget(src) << count)

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
def sext(cpu, tgt):
	val = cpu.rget(tgt)
	if val & (2**7):
		cpu.rset(tgt, val | 0xFF00)


class CPU(object):
	def __init__(self):
		self.reg  = [0 for _ in xrange(8)]
		self.mem  = [0 for _ in xrange(2**16)]
		self.halt = True
	
	def load(self, data):
		for i, n in enumerate(data):
			self.mem[i] = n
	
	def dump(self, mstart=None, mend=None):
		def hex_word(n):
			h = hex(n)[2:].upper().zfill(4)
			return h
			#return "%s %s" % (h[0:2], h[2:4])
		def hex_byte(n):
			return hex(n)[2:].upper().zfill(2)
		def bin_word(n):
			b = bin(n)[2:].zfill(16)
			return "%s %s  %s %s" % (b[0:4], b[4:8], b[8:12], b[12:16])
		for r in xrange(1, 8):
			v = self.reg[r]
			print "$%d:  %s  |  %s  =  %5s" % (r, bin_word(v), hex_word(v), v)
		if mstart is not None and mend is not None:
			count = 0
			for addr in xrange(mstart*2, mend*2, 2):
				if not count:
					print "\n%s | " % hex_word(addr/2),
				word = (self.mem[addr] << 8) | self.mem[addr+1]
				print hex_word(word),
				#print hex_byte(self.mem[addr]),
				count = (count + 1) % 8
			print
			print
	
	def run(self):
		self.halt = False
		while not self.halt:
			if self.reg[7] in globals.breakpoints:
				globals.trace = False
				globals.step = True
			opcode = self.fetch()
			# XXX
			if self.reg[7] > 0x80:
				return
			tok = isa.decode(opcode)
			if globals.step:
				self.dump(*globals.mem_range)
				print "%s> %s" % (shex(self.reg[7]-1, 4), str(tok)),
				raw_input()
				print
			operations[tok.name](self, **tok.arguments())
	
	def fetch(self):
		pc = self.reg[7]
		self.reg[7] = pc + 1
		# XXX
		#if pc >= 16: raise ValueError("all done")
		return self.mget(pc)
	
	def mget(self, addr):
		high = self.mem[addr*2]
		low = self.mem[addr*2+1]
		byte = (high << 8) | low
		return byte

	def mset(self, addr, val, byte=False):
		high = (val & 0xFF) if byte else (val >> 8)
		low  = 0            if byte else (val & 0xFF)
		#print "setting", shex(addr, 2), shex(high, 2), shex(low, 2)
		self.mem[addr*2]   = high
		self.mem[addr*2+1] = low
	
	def rget(self, reg):
		return self.reg[reg]

	def rset(self, reg, value):
		if reg not in (0, 7):
			self.reg[reg] = value



def main(args):
	if len(args) != 1:
		print "USAGE: %s binary" % sys.argv[0]
		return 2
	data = map(ord, open(args[0], "rb").read())
	cpu = CPU()
	cpu.load(data)
	globals.mem_range[1] = len(data)/2
	cpu.dump(*globals.mem_range)
	cpu.run()
	cpu.dump(*globals.mem_range)

if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
