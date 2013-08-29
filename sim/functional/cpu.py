import sys

def sbin(n):
	return bin(n)[2:]
def shex(n):
	return hex(n)[2:].upper()
def num(s):
	return int(s.replace(" ", ""), 2)


def bits(n, h, l):
	mask = (2**(h-l+1) - 1) << l
	return (n & mask) >> l

def signed(n, bits):
	# two's complement
	if n & (1 << bits - 1):
		return n - (2**bits)
	return n

def unsigned(n, bits):
	# two's complement
	return (2**bits) + n



def imm(n):
	return (8, 4, 2, 1, -1, -2, -4, 8)[n]

def cond(n):
	map = (lambda x, y: x == y,
		   lambda x, y: x != y,
		   lambda x, y: x  > y,
		   lambda x, y: x >= y,
		   lambda x, y: x  < y,
		   lambda x, y: x <= y,
		   lambda x, y: unsigned(x, 16)  < unsigned(y, 16),
		   lambda x, y: unsigned(x, 16) <= unsigned(y, 16))
	return map[n]


#
# instructions
#

def jmp(cpu, opcode):
	addr = signed(bits(opcode, 12, 0), 13)
	print "jmp", addr
	cpu.reg[7] += addr - 1
	#cpu.dump()

def ldw(cpu, opcode):
	offset = signed(bits(opcode, 12, 6), 7)
	base = bits(opcode, 5, 3)
	tgt = bits(opcode, 2, 0)
	print "ldw", offset, base, tgt
	base = cpu.reg[base]
	value = cpu.fetch(base + offset)
	cpu.reg[tgt] = value

def stw(cpu, opcode):
	offset = signed(bits(opcode, 12, 6), 7)
	base = bits(opcode, 5, 3)
	src = bits(opcode, 2, 0)
	print "stw", offset, base, src
	base = cpu.reg[base]
	value = cpu.reg[src]
	cpu.set(base + offset, value)

def add(cpu, opcode):
	ir = bits(opcode, 9, 9)
	op1 = bits(opcode, 8, 6)
	op2 = bits(opcode, 5, 3)
	tgt = bits(opcode, 2, 0)
	print "add", ir, op1, op2, tgt
	op1 = cpu.reg[op1]
	op2 = imm(op2) if ir else cpu.reg[op2]
	cpu.reg[tgt] = op1 + op2

def sub(cpu, opcode):
	ir = bits(opcode, 9, 9)
	op1 = bits(opcode, 8, 6)
	op2 = bits(opcode, 5, 3)
	tgt = bits(opcode, 2, 0)
	print "sub", ir, op1, op2, tgt
	op1 = cpu.reg[op1]
	op2 = imm(op2) if ir else cpu.reg[op2]
	cpu.reg[tgt] = op1 - op2

def skip(cpu, opcode):
	ir = bits(opcode, 9, 9)
	op1 = bits(opcode, 8, 6)
	op2 = bits(opcode, 5, 3)
	c = bits(opcode, 2, 0)
	print "skip", ir, op1, op2, c
	op1 = cpu.reg[op1]
	op2 = imm(op2) if ir else cpu.reg[op2]
	if cond(c)(op1, op2):
		cpu.reg[7] += 1

def halt(cpu, opcode):
	print "halt"
	cpu.halt = True



class Registers(object):
	def __init__(self):
		self.values = [0 for _ in xrange(8)]
	
	def __setitem__(self, i, v):
		if i != 0:
			self.values[i] = v
	
	def __getitem__(self, i):
		return self.values[i]


class CPU(object):
	def __init__(self):
		self.reg  = Registers()
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
			opcode = self.fetch_inst()
			inst = self.decode(opcode)
			inst(self, opcode)
	
	def fetch_inst(self):
		pc = self.reg[7]
		self.reg[7] = pc + 1
		# XXX
		#if pc >= 16: raise ValueError("all done")
		return self.fetch(pc)
	
	def fetch(self, addr):
		high = self.mem[addr*2]
		low = self.mem[addr*2+1]
		byte = (high << 8) | low
		return byte

	def set(self, addr, val):
		high = (val >> 8)
		low = val & 0xFF
		self.mem[addr*2] = high
		self.mem[addr*2+1] = low
	
	def decode(self, opcode):
		if   bits(opcode, 15, 13) == int("000", 2):
			return ldw
		# ...
		elif bits(opcode, 15, 13) == int("010", 2):
			return stw
		# ...
		elif bits(opcode, 15, 13) == int("100", 2):
			return jmp
		# ...
		elif bits(opcode, 15, 10) == int("101000", 2):
			return add
		elif bits(opcode, 15, 10) == int("101001", 2):
			return sub
		# ...
		elif bits(opcode, 15, 10) == int("101100", 2):
			return skip
		# ...
		elif bits(opcode, 15,  0) == int("1111111011011110", 2):
			return halt
		print "decode", bin(opcode)
		return lambda *args: None



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

#	def sbin(n):
#		print bin(n)[2:].zfill(16)
#	def num(s):
#		return int(s.replace(" ", ""), 2)
#	
#	n = num("0001 0011 0101 1101")
#	sbin(n)
#	sbin(bits(n, 15, 12))

if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
