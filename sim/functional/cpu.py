#!/usr/bin/python

import argparse
import collections
import inspect
import random
import select
import sys

import asm.encoding
import debugger
import listeners


MAGIC_HEADER = 0xDEADF00D
TIMER_PERIOD = 250

IDT_ADDR = 0x0100
PIC_ADDR = 0x0010
SCR_ADDR = 0x0020
KB_ADDR  = 0x0030
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
	addr = cpu.rget(src)
	val = cpu.io(addr)
	cpu.rset(tgt, val)

@op
def outb(cpu, tgt, src):
	val = cpu.rget(src)
	addr = cpu.rget(tgt)
	cpu.io(addr, val & 0x00FF)

@op
def ldiw(cpu, tgt, src):
	inst = cpu.iget(cpu.rget(src) * 2)
	cpu.rset(tgt, inst)

@op
def stiw(cpu, tgt, src):
	inst = cpu.rget(src)
	cpu.iset(cpu.rget(tgt) * 2, inst)


def send_listeners(fn):
	def wrapper(cpu, *args, **kwargs):
		listener_call(cpu, fn.__name__, True, None, args, kwargs)
		res = fn(cpu, *args, **kwargs)
		listener_call(cpu, fn.__name__, False, res, args, kwargs)
		return res
	return wrapper


def listener_call(cpu, name, before, result, args, kwargs):
	empty = lambda *args, **kwargs: None
	name = ("before_" if before else "after_") + name
	for listener in cpu.listeners:
		func = getattr(listener, name, empty)
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
		self.listeners = []

	def randomize(self):
		word = lambda _: random.randint(0, 2**16-1)
		byte = lambda _: random.randint(0, 2**8-1)
		self.reg = map(word, self.reg)
		self.imem = map(byte, self.imem)
		self.dmem = map(byte, self.dmem)

	@send_listeners
	def dload(self, chunk):
		self._load(self.dmem, chunk)

	@send_listeners
	def iload(self, chunk):
		self._load(self.imem, chunk)

	def _load(self, mem, (addr, words)):
		for i, word in enumerate(words):
			high = word >> 8
			low = word & 0x00FF
			j = (addr + i) * 2
			mem[j] = high
			mem[j+1] = low

	@send_listeners
	def run(self):
		self.reg[PC] = 0
		while not self.halt:
			self.clock += 1
			self.pic.tick()
			if (self.reg[FLAGS] & IE) and self.pic.int_line:
				irq = self.pic.get_interrupt()
				self.do_interrupt(irq)
			opcode = self.fetch()
			tok = asm.encoding.decode(opcode)
			func = lookup_op(tok)
			func(self, **tok.arguments())

	@send_listeners
	def do_interrupt(self, irq):
		self.reg[EPC] = self.reg[PC]
		self.reg[PC] = self.mget((IDT_ADDR | irq) * 2)
		self.reg[FLAGS] &= ~IE

	@send_listeners
	def fetch(self):
		pc = self.reg[PC]
		self.reg[PC] = (pc + 1) & 0xFFFF
		return self.iget(pc * 2)

	@send_listeners
	def iget(self, addr):
		self._check_addr(addr)
		high = self.imem[addr]
		low = self.imem[addr + 1]
		byte = (high << 8) | low
		return byte

	@send_listeners
	def iset(self, addr, val, byte=False):
		self._check_addr(addr)
		high = (val & 0xFF) if byte else (val >> 8)
		low  = 0            if byte else (val & 0xFF)
		self.imem[addr] = high
		if not byte:
			self.imem[addr + 1] = low

	@send_listeners
	def mget(self, addr):
		self._check_addr(addr)
		high = self.dmem[addr]
		low = self.dmem[addr + 1]
		byte = (high << 8) | low
		return byte

	@send_listeners
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

	@send_listeners
	def rget(self, reg):
		return self.reg[reg]

	@send_listeners
	def rset(self, reg, value):
		if reg != 0:
			self.reg[reg] = value

	@send_listeners
	def crget(self, cr):
		val = self.reg[8 + cr]
		if cr == 0: val += 1
		return val

	@send_listeners
	def crset(self, cr, value):
		if cr != 0:
			self.reg[8 + cr] = value

	@send_listeners
	def io(self, addr, val=None):
		dev = self.dev[addr]
		if dev is not None:
			return dev.read(val)
		raise Exception("error: read to invalid io port: %02X (%s)" % (addr, val))

	def add_listener(self, listener):
		self.listeners.append(listener)


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
	def __init__(self):
		self.buffer = []
		self.pic = None # set in pic device

	def tick(self):
		ready, a, b = select.select([sys.stdin], [], [], 0)
		if ready:
			# XXX doesn't work
			self.buffer.append(ord(ready[0].read(1)))
		if self.buffer:
			self.pic.interrupt(self)

	def read(self, val=None):
		if val is not None:
			show("keyboard error: tried to write value:", val, "\n")
			sys.exit(1)
		return self.buffer.pop() if self.buffer else 0


class DebugKeyboardDevice(KeyboardDevice):
	def tick(self):
		if self.buffer:
			self.pic.interrupt(self)

	def read(self, val=None):
		if val is not None:
			self.buffer.append(val)
			return 0
		return self.buffer.pop(0) if self.buffer else 0


class ScreenDevice(Device):
	def read(self, val=None):
		if val is not None:
			sys.stdout.write(chr(val))


def load_devices(cpu, debugger=False):
	pic = PICDevice(cpu)
	timer = TimerDevice(TIMER_PERIOD)
	if debugger:
		kb = DebugKeyboardDevice()
	else:
		kb = KeyboardDevice()
	scr = ScreenDevice()
	pic.register(timer, 7)
	pic.register(kb, 2)
	cpu.pic = pic
	cpu.dev[PIC_ADDR] = pic
	cpu.dev[SCR_ADDR] = scr
	cpu.dev[KB_ADDR]  = kb


def parse_file(stream):
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

	if read(stream, 4) != MAGIC_HEADER:
		show("ERROR: Magic header not found\n")
		return None
	return read_chunks(stream), read_chunks(stream)


def load_args(args):
	def addr(s): return int(s, 16) # def'd so that "addr" will show in error messages
	binfile = argparse.FileType("rb")
	tracefile = argparse.FileType("w")
	p = argparse.ArgumentParser(description="Functional simulator for XXX cpu", usage="%(prog)s [exe] [options]")

	p.add_argument("exe", nargs="?", type=binfile, help="load executable into memory")
	p.add_argument("--stop-clock", metavar="CLOCK", dest="stop_clock", type=int, help="stop execution upon reaching clock CLOCK")
	p.add_argument("--randomize", dest="randomize", action="store_true", help="randomize all memory and registers before execution")
	#p.add_argument("--access-errors", dest="fail_mem", action="store_true", help="fail on memory access errors (read before write, etc)")
	#p.add_argument("--start-at", metavar="ADDR", dest="start", type=addr, help="start executing at instruction memory ADDR")
	#p.add_argument("--enable-keyboard", dest="keyboard", action="store_true", help="enable keyboard input (conflicts with debugger)")
	#p.add_argument("--clock-speed", dest="clock_speed", metavar="HZ", type=int, help="run at HZ clock speed with realistic delay")

	#g = p.add_argument_group("load-options")
	#g.add_argument("--load-rom", metavar="FILE", dest="rom", type=binfile, help="load FILE into ROM")
	#g.add_argument("--load-serial-0", metavar="FILE", dest="uarta", type=binfile, help="UART0 reads from FILE")
	#g.add_argument("--load-serial-1", metavar="FILE", dest="uartb", type=binfile, help="UART1 reads from FILE")
	#g.add_argument("--load-data", metavar="FILE", dest="data", type=binfile, help="load FILE into data memory at address 0")
	#g.add_argument("--load-inst", metavar="FILE", dest="inst", type=binfile, help="load FILE into instruction memory at address 0")

	g = p.add_argument_group("debugger-options")
	g.add_argument("--no-debugger", dest="debug", action="store_false", help="start without debugger")
	g.add_argument("--breakpoints", metavar="ADDR", dest="breakpoints", type=addr, nargs="+", help="set debugger breakpoints")
	# TODO other debugger options

	g = p.add_argument_group("output-options")
	g.add_argument("--trace", metavar="FILE", dest="trace", type=tracefile, help="trace data sent to FILE")
	#g.add_argument("--test-clock", metavar="CLOCK", dest="test_clocks", type=int, nargs="+", help="display test output at each CLOCK")
	#g.add_argument("--test-clock-intvl", metavar="COUNT", dest="test_clock_int", type=int, help="display test output every COUNT clocks")
	# TODO configure test output

	if not args:
		p.print_help()
		sys.exit(2)

	return p.parse_args(args)


def main(args):
	opts = load_args(args)
	cpu = CPU()

	if opts.randomize:
		cpu.randomize()

	if opts.debug:
		dbg = debugger.Debugger(cpu)
		if opts.breakpoints:
			dbg.brk_addrs = set(opts.breakpoints)
		cpu.add_listener(dbg)

	if opts.trace:
		trace = listeners.Tracer(cpu, opts.trace)
		cpu.add_listener(trace)

	if opts.stop_clock:
		stopper = listeners.StopClock(cpu, opts.stop_clock)
		cpu.add_listener(stopper)

	if opts.exe:
		chunks = parse_file(opts.exe)
		map(cpu.dload, chunks[0])
		map(cpu.iload, chunks[1])

	load_devices(cpu, opts.debug)
	try:
		cpu.run()
	except KeyboardInterrupt:
		show("\n")
	return 0


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
