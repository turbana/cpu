
import asm.encoding


PC = 8


def registers(cpu, start, stop):
	return " ".join("%s=%04X" % (reg_name(r), cpu.reg[r]) for r in range(1, 11))

def reg_name(r):
	if r < 8:
		return "$" + str(r)
	return "$cr" + str(r-8)


class Tracer(object):
	def __init__(self, cpu, trace_file):
		self.cpu = cpu
		self.stream = trace_file

	def show(self, data):
		self.stream.write(data)

	def after_fetch(self, opcode):
		addr = self.cpu.reg[PC] - 1
		toks = str(asm.encoding.decode(opcode)).split("\t")
		tok = "%-8s %s" % (toks[0], toks[1])
		regs = registers(self.cpu, 1, 11)
		left = "%04X | %s" % (addr, tok)
		line = "%-32s (%s) clk=%d\n" % (left, regs, self.cpu.clock)
		self.show(line)

	def after_do_interrupt(self, _, irq):
		self.show("int %02X\n" % irq)

	def after_io(self, res, addr, val=None):
		if val is None:
			self.show("io %02X > %02X\n" % (addr, res))
		else:
			self.show("io %02X < %02X\n" % (addr, val))


class StopClock(object):
	def __init__(self, cpu, clock):
		self.cpu = cpu
		self.clock = clock

	def before_cycle(self, _):
		if self.cpu.clock >= self.clock:
			self.cpu.halt = True


class ErrorChecker(object):
	def __init__(self, cpu):
		self.cpu = cpu
		self.regs = set([0])
		self.imem = set()
		self.dmem = set()

	def after_iload(self, _, (addr, words)):
		for n in range(len(words)*2):
			self.imem.add(addr*2 + n)

	def after_dload(self, _, (addr, words)):
		for n in range(len(words)*2):
			self.dmem.add(addr + n)

	def before_iget(self, _, addr):
		if addr not in self.imem:
			raise Exception("ERROR: read from imem 0x%04X before write\n" % (addr/2))

	def before_iset(self, _, addr):
		self.imem.add(addr)

	def before_dget(self, _, addr):
		if addr not in self.dmem:
			raise Exception("ERROR: read from mem 0x%04X before write\n" % (addr/2))

	def before_dset(self, _, addr):
		self.imem.add(addr)

	def before_rget(self, _, reg):
		# only throw on read of non control register
		if reg not in self.regs and reg < 8:
			raise Exception("ERROR: read from register %s before write\n" % reg_name(reg))

	def before_rset(self, _, reg, _a):
		self.regs.add(reg)


class TestOutput(object):
	def __init__(self, cpu, clock_rate, clocks):
		self.cpu = cpu
		self.clock_rate = clock_rate
		self.clocks = set(clocks)

	def after_cycle(self, _):
		cpu_clock = self.cpu.clock
		if cpu_clock < 0: return
		clock_match = cpu_clock in self.clocks
		clock_rate = self.clock_rate is not None and cpu_clock != 0 and (cpu_clock % self.clock_rate) == 0
		clock_rate_first = cpu_clock == 0 and self.clock_rate == 1
		if clock_match or clock_rate or clock_rate_first:
			print "%d (%s)" % (cpu_clock, registers(self.cpu, 1, 11))
