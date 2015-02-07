import collections
import inspect
import sys

import asm.encoding
import debugger


MAGIC_HEADER = 0xDEADF00D
TIMER_PERIOD = 25

IDT_ADDR = 0x0100
PIC_ADDR = 0x0010
SCR_ADDR = 0x0020
EOI_VAL = 0x00AB

PC    = 8 # register
FLAGS = 9
EPC   = 10

IE = 1 # interrupts enabled flag bit


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

def show(*strs):
	sys.stdout.write(" ".join(map(str, strs)))


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
def ldw(cpu, tgt, base, index, ir):
	base = cpu.rget(base)
	if not ir: index = cpu.rget(index)
	cpu.rset(tgt, cpu.mget((base + index) * 2))

@op
def stw(cpu, base, src, offset):
	cpu.mset((offset + cpu.rget(base)) * 2, cpu.rget(src))

@op
def stw(cpu, base, src, index, ir):
	base = cpu.rget(base)
	if not ir: index = cpu.rget(index)
	cpu.mset((index + base) * 2, cpu.rget(src))

@op
def jmp(cpu, offset):
	# jmp is PC + offset + 1, but we've already incremented PC in cpu.fetch(),
	# and offset is also incremented by 1 in decode()
	cpu.reg[PC] += offset - 1

@op
def jmp(cpu, tgt):
	cpu.reg[PC] = cpu.rget(tgt)

@op
def add(cpu, tgt, op1, op2, ir):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	res = op1 + op2
	cpu.rset(tgt, res & 0xFFFF)

@op
def sub(cpu, tgt, op1, op2, ir):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	res = twoc_unsign(op1 - op2)
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
	imm = twoc_unsign(imm, 8)
	# TODO check overflow
	cpu.rset(tgt, cpu.rget(tgt) + imm)

@op
def shl(cpu, ir, op1, op2, tgt):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	n = (op1 << op2) & 0xFFFF
	cpu.rset(tgt, n)

@op
def shr(cpu, ir, op1, op2, tgt):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	n = (op1 >> op2) & 0xFFFF
	cpu.rset(tgt, n)

@op
def xor(cpu, tgt, src):
	cpu.rset(tgt, cpu.rget(tgt) ^ cpu.rget(src))

@op
def trap(cpu, reg):
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

@op
def reti(cpu):
	cpu.reg[PC] = cpu.reg[EPC]

@op
def inb(cpu, tgt, src):
	raise NotImplementedError()

@op
def outb(cpu, tgt, src):
	val = cpu.rget(src)
	addr = cpu.rget(tgt)
	if cpu.dev[addr]:
		cpu.dev[addr].read(val & 0x00FF)

@op
def ldiw(cpu, tgt, src):
	inst = cpu.iget(cpu.rget(src) * 2)
	cpu.rset(tgt, inst)

@op
def stiw(cpu, tgt, src):
	inst = cpu.rget(src)
	cpu.iset(cpu.rget(tgt) * 2, inst)


def send_debugger(fn):
	def wrapper(cpu, *args, **kwargs):
		debugger_call(cpu, fn.__name__, True, None, args, kwargs)
		res = fn(cpu, *args, **kwargs)
		debugger_call(cpu, fn.__name__, False, res, args, kwargs)
		return res
	return wrapper


def debugger_call(cpu, name, before, result, args, kwargs):
	func = lambda *args, **kwargs: None
	if cpu.debugger:
		name = ("before_" if before else "after_") + name
		func = getattr(cpu.debugger, name, func)
	func(result, *args, **kwargs)


class CPU(object):
	def __init__(self):
		self.reg  = [0] * 16
		self.imem = [0] * 2**17 # memory is 2**16 words therefore 2**17 bytes
		self.dmem = [0] * 2**17 # ...
		self.dev = [None] * 2**16
		self.pic = None
		self.halt = False
		self.clock = 0
		self.debugger = None

	@send_debugger
	def dload(self, chunk):
		self._load(self.dmem, chunk)

	@send_debugger
	def iload(self, chunk):
		self._load(self.imem, chunk)

	def _load(self, mem, (addr, words)):
		for i, word in enumerate(words):
			high = word >> 8
			low = word & 0x00FF
			j = (addr + i) * 2
			mem[j] = high
			mem[j+1] = low

	@send_debugger
	def run(self, stop_clock=None):
		while not self.halt:
			self.clock += 1
			self.pic.tick()
			if (self.reg[FLAGS] & IE) and self.pic.int_line:
				irq = self.pic.get_interrupt()
				self.reg[EPC] = self.reg[PC]
				self.reg[PC] = self.mget((IDT_ADDR | irq) * 2)
				self.reg[FLAGS] &= ~IE
			opcode = self.fetch()
			tok = asm.encoding.decode(opcode)
			func = lookup_op(tok)
			func(self, **tok.arguments())
			if self.clock == stop_clock:
				self.halt = True

	@send_debugger
	def fetch(self):
		pc = self.reg[PC]
		self.reg[PC] = (pc + 1) & 0xFFFF
		return self.iget(pc * 2)

	@send_debugger
	def iget(self, addr):
		self._check_addr(addr)
		high = self.imem[addr]
		low = self.imem[addr + 1]
		byte = (high << 8) | low
		return byte

	@send_debugger
	def iset(self, addr, val, byte=False):
		self._check_addr(addr)
		high = (val & 0xFF) if byte else (val >> 8)
		low  = 0            if byte else (val & 0xFF)
		self.imem[addr] = high
		if not byte:
			self.imem[addr + 1] = low

	@send_debugger
	def mget(self, addr):
		self._check_addr(addr)
		high = self.dmem[addr]
		low = self.dmem[addr + 1]
		byte = (high << 8) | low
		return byte

	@send_debugger
	def mset(self, addr, val, byte=False):
		self._check_addr(addr)
		high = (val & 0xFF) if byte else (val >> 8)
		low  = 0            if byte else (val & 0xFF)
		self.dmem[addr] = high
		if not byte:
			self.dmem[addr + 1] = low

	def _check_addr(self, addr):
		if addr >= 2**17:
			raise Exception("Invalid memory access: %04X" % addr)

	@send_debugger
	def rget(self, reg):
		return self.reg[reg]

	@send_debugger
	def rset(self, reg, value):
		if reg != 0:
			self.reg[reg] = value

	@send_debugger
	def crget(self, cr):
		val = self.reg[8 + cr]
		if cr == 0: val += 1
		return val

	@send_debugger
	def crset(self, cr, value):
		if cr != 0:
			self.reg[8 + cr] = value


def dump_short(cpu):
	for r in xrange(1, 10):
		v = cpu.reg[r]
		name = ("$%d" % r) if r < 8 else ("$cr%d" % (r-8))
		# print to stdout for runtest.sh
		print "%s 0x%04X" % (name, v)



class Device(object):
	def tick(self):
		pass

	def read(self, write=None):
		pass


class TimerDevice(Device):
	def __init__(self, period):
		self.count = 0
		self.period = period
		self.pic = None

	def tick(self):
		self.count += 1
		if self.count == self.period:
			self.count = 0
			self.pic.interrupt(self)

	def read(self, count=None):
		if count is None:
			return self.count
		self.count = count


class PICDevice(Device):
	def __init__(self, cpu):
		self.devices = [None] * 8
		self.cpu = cpu
		self.pending = 0
		self.int_line = False

	def tick(self):
		for dev in self.devices:
			if dev is not None:
				dev.tick()

	def read(self, val):
		if val != EOI_VAL:
			show("pic error: received wrong value for EOI:", val, "\n")
			sys.exit(1)
		irq = self.get_interrupt()
		self.pending &= ~(1 << irq)
		self.int_line = self.pending != 0

	def register(self, dev, irq):
		self.devices[irq] = dev
		dev.pic = self

	def interrupt(self, dev):
		irq = self.devices.index(dev)
		already = self.pending & (1 << irq)
		self.pending |= (1 << irq)
		# TODO check for priority
		if not already:
			self.int_line = True

	def get_interrupt(self):
		self.int_line = False
		for irq in range(8):
			if self.pending & (1 << irq):
				return irq
		return None


class KeyboardDevice(Device):
	pass


class ScreenDevice(Device):
	def read(self, val=None):
		if val is not None:
			sys.stdout.write(chr(val))


def load_devices(cpu):
	pic = PICDevice(cpu)
	timer = TimerDevice(TIMER_PERIOD)
	kb = KeyboardDevice()
	scr = ScreenDevice()
	pic.register(timer, 7)
	pic.register(kb, 2)
	cpu.pic = pic
	cpu.dev[PIC_ADDR] = pic
	cpu.dev[SCR_ADDR] = scr


def parse_file(filename):
	def read(stream, bytes):
		value = 0
		for byte in stream.read(bytes):
			value <<= 8
			value |= ord(byte)
		return value
	def read_chunks(stream):
		chunk_count = read(stream, 2)
		chunks = []
		for _ in range(chunk_count):
			addr = read(stream, 2)
			count = read(stream, 2)
			words = [read(stream, 2) for _ in range(count)]
			chunks.append((addr, words))
		return chunks

	with open(filename, "rb") as stream:
		if read(stream, 4) != MAGIC_HEADER:
			show("ERROR: Magic header not found\n")
			return None
		return read_chunks(stream), read_chunks(stream)


def main(args):
	if len(args) == 1:
		filename = args[0]
		stop_clock = None
	elif len(args) == 3 and args[1] == "--dump":
		filename = args[0]
		stop_clock = int(args[2])
	else:
		show("USAGE: %s binary [--dump clock]\n" % sys.argv[0])
		return 2
	chunks = parse_file(filename)
	if not chunks:
		return 1
	cpu = CPU()
	if not stop_clock:
		cpu.debugger = debugger.Debugger(cpu)
	map(cpu.dload, chunks[0])
	map(cpu.iload, chunks[1])
	load_devices(cpu)
	try:
		cpu.run(stop_clock)
		if stop_clock is not None:
			dump_short(cpu)
	except KeyboardInterrupt:
		show("\n")
		return 0

if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
