import sys
import isa

TRACE = True

def sbin(n):
	return bin(n)[2:]
def shex(n):
	return hex(n)[2:].upper()
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
	if TRACE:
		items = [key+"="+str(val) for key, val in kwargs.items()]
		print "%-8s %s" % (name, " ".join(items))


operations = {}

def op(func):
	def wrap(*args, **kwargs):
		trace(func.func_name, args, kwargs)
		return func(*args, **kwargs)
	operations[func.func_name] = wrap
	return wrap


@op
def ldw(cpu, tgt, base, offset):
	# TODO handle reg ldw
	cpu.rset(tgt, cpu.mget(base + offset))

@op
def stw(cpu, offset, base, src):
	# TODO handle reg stw
	cpu.mset(offset + base, cpu.rget(src))

@op
def jmp(cpu, offset):
	cpu.reg[7] += offset - 1

@op
def add(cpu, tgt, op1, op2, ir):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	cpu.rset(tgt, op1 + op2)

@op
def sub(cpu, tgt, op1, op2, ir):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	cpu.rset(tgt, op1 - op2)

@op
def s(cpu, cond, op1, op2, ir):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	func = condition_func[cond]
	if func(op1, op2):
		cpu.reg[7] += 1

@op
def halt(cpu):
	cpu.halt = True


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
			return "%s %s" % (h[0:2], h[2:4])
		def hex_byte(n):
			return hex(n)[2:].upper().zfill(2)
		def bin_word(n):
			b = bin(n)[2:].zfill(16)
			return "%s %s  %s %s" % (b[0:4], b[4:8], b[8:12], b[12:16])
		for r in xrange(1, 8):
			v = self.reg[r]
			print "reg %d:  %s | %s = %5s" % (r, bin_word(v), hex_word(v), v)
		if mstart is not None and mend is not None:
			count = 0
			for addr in xrange(mstart, mend+1):
				if not count:
					print "\n%s | " % hex_word(addr),
				print hex_byte(self.mem[addr]),
				count = (count + 1) % 16
			print
			print
	
	def run(self):
		self.halt = False
		while not self.halt:
			opcode = self.fetch()
			# XXX
			if self.reg[7] > 0x13:
				return
			tok = isa.decode(opcode)
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

	def mset(self, addr, val):
		high = (val >> 8)
		low = val & 0xFF
		self.mem[addr*2] = high
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
	cpu.dump(0, 47)
	cpu.run()
	cpu.dump(0, 47)

if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
