
import asm.encoding


PC = 8

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
		regs = " ".join("%d=%04X" % (r, self.cpu.reg[r]) for r in range(1, 11))
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

	def before_fetch(self, _):
		if self.clock == self.cpu.clock:
			self.cpu.halt = True
