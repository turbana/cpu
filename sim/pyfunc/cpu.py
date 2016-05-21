#!/usr/bin/python

import argparse
import collections
import fcntl
import inspect
import os
import random
import select
import sys
import termios
import threading
import time

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

# registers
R_ZERO		= 0
R_PC		= 8
R_DS		= 9
R_CS		= 10
R_FLAGS		= 11
R_EPC		= 12
R_EDS		= 13
R_ECS		= 14
R_EFLAGS	= 15

# $flags register (bit masks)
FLAGS_IE	= 0x1
FLAGS_M		= 0x2


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
	fargs = inspect.getargspec(func).args[1:]
	operations[name].append((func, sorted(fargs)))
	return func

def lookup_op(tok):
	argnames = sorted(tok.arguments().keys())
	for func, fargs in operations[tok.name]:
		if fargs == argnames:
			return func
	raise Exception("Instruction not defined: %s (%s)" % (tok.name, ", ".join(argnames)))

#
# Operations
#

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
	# decrement PC as we've already incremented it in cpu.fetch()
	cpu.reg[R_PC] += offset - 1
	cpu.stall(2)

@op
def jmp(cpu, index, base, ir):
	base = cpu.rget(base)
	if not ir: index = cpu.rget(index)
	cpu.reg[R_PC] = base + index
	cpu.stall(2)

@op
def add(cpu, tgt, op1, op2, ir):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	cpu.rset(tgt, op1 + op2)

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
		cpu.reg[R_PC] += 1
		cpu.stall()

@op
def as_z(cpu, ir, op1, op2, tgt):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	res = (op1 + op2) & 0xFFFF
	cpu.rset(tgt, res)
	if res == 0:
		cpu.reg[R_PC] += 1
		cpu.stall()

@op
def as_nz(cpu, ir, op1, op2, tgt):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	res = (op1 + op2) & 0xFFFF
	cpu.rset(tgt, res)
	if res != 0:
		cpu.reg[R_PC] += 1
		cpu.stall()

@op
def lui(cpu, imm, tgt):
	imm = twoc_unsign(imm, 8)
	cpu.rset(tgt, imm << 8)

@op
def addi(cpu, imm, tgt):
	imm = twoc_unsign(imm, 8)
	if imm & 0x80:
		imm |= 0xFF00
	cpu.rset(tgt, cpu.rget(tgt) + imm)

@op
def shl(cpu, ir, op1, op2, tgt):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	cpu.rset(tgt, op1 << op2)

@op
def shr(cpu, ir, op1, op2, tgt):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	cpu.rset(tgt, op1 >> op2)

@op
def sar(cpu, ir, op1, op2, tgt):
	op1 = cpu.rget(op1)
	if not ir: op2 = cpu.rget(op2)
	res = op1 >> op2
	mask = ~(2**(16-op2) - 1) if op1 & 0x8000 else 0
	cpu.rset(tgt, res | mask)

@op
def iret(cpu):
	cpu.reg[R_PC] = cpu.reg[R_EPC]
	cpu.reg[R_CS] = cpu.reg[R_ECS]
	cpu.reg[R_DS] = cpu.reg[R_EDS]
	cpu.reg[R_FLAGS] = cpu.reg[R_EFLAGS] | (1 << FLAGS_IE)
	cpu.stall(2)				# TODO check stall value

@op
def lcr(cpu, tgt, cr):
	cpu.rset(tgt, cpu.crget(cr))

@op
def scr(cpu, cr, src):
	cpu.crset(cr, cpu.rget(src))

@op
def ldiw(cpu, tgt, src):
	inst = cpu.iget(cpu.rget(src) * 2)
	cpu.rset(tgt, inst)

@op
def stiw(cpu, tgt, src):
	inst = cpu.rget(src)
	cpu.iset(cpu.rget(tgt) * 2, inst)


# TODO add halt and trap instructions


#
# CPU
#

def send_listeners(fn):
	def wrapper(cpu, *args, **kwargs):
		for lis in cpu.listeners["before_" + fn.__name__]:
			lis(*args, **kwargs)
		res = fn(cpu, *args, **kwargs)
		for lis in cpu.listeners["after_" + fn.__name__]:
			lis(res, *args, **kwargs)
		return res
	return wrapper


class CPU(object):
	def __init__(self, real_clock):
		self.reg  = [0] * 16
		self.imem = [0] * 2**17 # memory is 2**16 words therefore 2**17 bytes
		self.dmem = [0] * 2**17 # ...
		self.dev = [None] * 2**16
		self.pic = None
		self.halt = False
		self.real_clock = real_clock
		self.clock = (4 if real_clock else 0) - 1
		self.listeners = collections.defaultdict(list)
		self.mem_write_reg = None
		self.stalls = 0

	def randomize(self):
		word = lambda _: random.randint(0, 2**16-1)
		byte = lambda _: random.randint(0, 2**8-1)
		for r in range(1, 8): self.reg[r] = word(0)
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
		self.reset()
		while not self.halt:
			self.cycle()

	@send_listeners
	def reset(self):
		self.reg[R_PC] = 0
		self.reg[R_CS] = 0
		self.reg[R_DS] = 0
		self.reg[R_FLAGS] = 0

	@send_listeners
	def cycle(self):
		self.pic.tick()
		if (self.reg[R_FLAGS] & FLAGS_IE) and self.pic.int_line:
			self.do_interrupt()
		if self.stalls:
			self.stalls -= 1
			tok = None
		else:
			opcode = self.fetch()
			tok = asm.encoding.decode(opcode)
		self.update_clock(tok)
		if tok is not None:
			self.execute(tok)

	@send_listeners
	def execute(self, tok):
		func = lookup_op(tok)
		func(self, **tok.arguments())

	def stall(self, count=1):
		self.stalls += count

	def update_clock(self, token):
		self.clock += 1
		if not self.real_clock or token is None: return
		# stall this instruction on register read after memory fetch
		read_args = [str(arg) for arg in token.args if not arg.dest]
		if self.mem_write_reg in read_args:
			self.clock += 1
		self.mem_write_reg = str(token.tgt) if token.name in ("ldw", "ldiw") else None

	@send_listeners
	def do_interrupt(self, irq):
		# save state
		self.reg[R_EPC] = self.reg[R_PC]
		self.reg[R_EDS] = self.reg[R_DS]
		self.reg[R_ECS] = self.reg[R_CS]
		self.reg[R_EFLAGS] = self.reg[R_FLAGS]
		# disable interrupts
		self.reg[FLAGS] &= ~FLAGS_IE
		# jump to isr
		self.reg[PC] = self.pic.read(DEV_PIC_DATA)

	@send_listeners
	def fetch(self):
		pc = self.reg[R_PC]
		self.reg[R_PC] = (pc + 1) & 0xFFFF
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
		# ignore writes to $0 and (when in user mode) writes to control registers
		if reg == R_ZERO or (reg >= 8 and self.reg[R_FLAGS] & FLAGS_M):
			return
		self.reg[reg] = (value & 0xFFFF)

	@send_listeners
	def crget(self, cr):
		val = self.reg[8 + cr]
		# decrement when reading PC as we've already incremented in fetch()
		if cr == 0: val -= 1
		return val

	@send_listeners
	def crset(self, cr, value):
		if cr != 0:
			self.reg[8 + cr] = (value & 0xFFFF)

	@send_listeners
	def io(self, addr, val=None):
		dev = self.dev[addr]
		if dev is not None:
			return dev.read(val)
		raise Exception("error: read to invalid io port: %02X (%s)" % (addr, val))

	def add_listener(self, listener):
		for attr in dir(listener):
			if attr.startswith("before_") or attr.startswith("after_"):
				self.listeners[attr].append(getattr(listener, attr))


def dump_short(cpu):
	for r in xrange(1, 10):
		v = cpu.reg[r]
		name = ("$%d" % r) if r < 8 else ("$cr%d" % (r-8))
		# print to stdout for runtest.sh
		print "%s 0x%04X" % (name, v)


#
# Devices
#


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
		self.lock = threading.Lock()
		self.buffer = []
		self.pic = None # set in pic device
		t1 = threading.Thread(target=keyboard_thread, args=(self.lock, self.buffer))
		t1.daemon = True
		t1.start()

	def tick(self):
		with self.lock:
			if self.buffer:
				self.pic.interrupt(self)

	def read(self, val=None):
		if val is not None:
			show("keyboard error: tried to write value:", val, "\n")
			sys.exit(1)
		with self.lock:
			return self.buffer.pop() if self.buffer else 0


def keyboard_thread(lock, buffer):
	while True:
		c = getch()
		with lock:
			buffer.append(ord(c))


class NullKeyboardDevice(Device):
	def __init__(self):
		self.buffer = []
		self.pic = None # set in pic device

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


def load_devices(cpu, keyboard=False):
	pic = PICDevice(cpu)
	timer = TimerDevice(TIMER_PERIOD)
	if keyboard:
		kb = KeyboardDevice()
	else:
		kb = NullKeyboardDevice()
	scr = ScreenDevice()
	pic.register(timer, 7)
	pic.register(kb, 2)
	cpu.pic = pic
	cpu.dev[PIC_ADDR] = pic
	cpu.dev[SCR_ADDR] = scr
	cpu.dev[KB_ADDR]  = kb


# following three functions modified from:
# http://love-python.blogspot.com/2010/03/getch-in-python-get-single-character.html
def getch():
	while True:
		try:
			return sys.stdin.read(1)
		except IOError:
			time.sleep(0.01)


def save_term():
	fd = sys.stdin.fileno()
	oldterm = termios.tcgetattr(fd)
	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
	return fd, oldterm, oldflags


def restore_term((fd, oldterm, oldflags)):
	termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)



#
# Main
#


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
	p.add_argument("--stop-clock", metavar="CLOCK", dest="stop_clock", type=int, help="stop execution upon reaching CLOCK")
	p.add_argument("--no-randomize", dest="randomize", action="store_false", help="randomize all memory and registers before execution")
	p.add_argument("--no-check-errors", dest="check_errors", action="store_false", help="don't check for errors (e.x. mem read before write)")
	p.add_argument("--no-realistic-clock", dest="real_clock", action="store_false", help="report clock count from WB stage (includes bubbles)")
	#p.add_argument("--start-at", metavar="ADDR", dest="start", type=addr, help="start executing at instruction memory ADDR")
	p.add_argument("--keyboard", dest="keyboard", action="store_true", help="enable keyboard input (conflicts with debugger)")
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
	g.add_argument("--test-clock", metavar="CLOCK", dest="test_clocks", type=int, nargs="+", default=[None], help="display test output at each CLOCK")
	g.add_argument("--test-clock-rate", metavar="COUNT", dest="test_clock_rate", type=int, help="display test output every COUNT clocks")
	# TODO configure test output

	if not args:
		p.print_help()
		sys.exit(2)

	return p.parse_args(args)


def main(args):
	opts = load_args(args)
	cpu = CPU(opts.real_clock)

	if opts.debug and opts.keyboard:
		show("ERROR: cannot have both debugger and keyboard support\n")
		return 1

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

	if opts.check_errors:
		chk = listeners.ErrorChecker(cpu)
		cpu.add_listener(chk)

	if opts.test_clocks or opts.test_clock_rate:
		tester = listeners.TestOutput(cpu, opts.test_clock_rate, opts.test_clocks)
		cpu.add_listener(tester)

	if opts.stop_clock:
		stopper = listeners.StopClock(cpu, opts.stop_clock)
		cpu.add_listener(stopper)

	if opts.exe:
		chunks = parse_file(opts.exe)
		map(cpu.dload, chunks[0])
		map(cpu.iload, chunks[1])

	if opts.keyboard:
		term = save_term()
	load_devices(cpu, opts.keyboard)
	try:
		cpu.run()
	except KeyboardInterrupt:
		show("\n")
	finally:
		if opts.keyboard:
			restore_term(term)
	return 0


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
