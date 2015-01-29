
import asm

PC    = 8 # register
FLAGS = 9
EPC   = 10


def idump(cpu, mstart=None, mend=None):
	def hex_word(n):
		h = hex(n)[2:].upper().zfill(4)
		return h
	def hex_byte(n):
		return hex(n)[2:].upper().zfill(2)
	def bin_word(n):
		b = bin(n)[2:].zfill(16)
		return "%s %s  %s %s" % (b[0:4], b[4:8], b[8:12], b[12:16])
	print
	if mstart is not None and mend is not None:
		count = 0
		for addr in xrange(mstart*2, mend*2, 2):
			if not count:
				print "\n%s | " % hex_word(addr/2),
			word = (cpu.imem[addr] << 8) | cpu.imem[addr+1]
			print hex_word(word),
			count = (count + 1) % 8
		print
		print


def dump(cpu, mstart=None, mend=None):
	def hex_word(n):
		h = hex(n)[2:].upper().zfill(4)
		return h
	def hex_byte(n):
		return hex(n)[2:].upper().zfill(2)
	def bin_word(n):
		b = bin(n)[2:].zfill(16)
		return "%s %s  %s %s" % (b[0:4], b[4:8], b[8:12], b[12:16])
	print
	print " "*40 + "clock:", cpu.clock
	for r in xrange(1, 10):
		v = cpu.reg[r]
		name = ("  $%d" % r) if r < 8 else ("$cr%d" % (r-8))
		print "%s:  %s  |  %s  =  %5s" % (name, bin_word(v), hex_word(v), v)
	if mstart is not None and mend is not None:
		count = 0
		for addr in xrange(mstart*2, mend*2, 2):
			if not count:
				print "\n%s | " % hex_word(addr/2),
			word = (cpu.dmem[addr] << 8) | cpu.dmem[addr+1]
			print hex_word(word),
			count = (count + 1) % 8
		print
		print


class Debugger(object):
	def __init__(self, cpu):
		self.cpu = cpu
		self.step = True
		self.drange = [0, 0]
	
	def before_dload(self, cpu, _, bytes):
		self.drange[1] = len(bytes) / 2

	def after_fetch(self, cpu, opcode):
		if not self.step: return
		inst = asm.encoding.decode(opcode)
		dump(cpu, *self.drange)
		print "%04X> %s" % (cpu.reg[PC]-1, str(inst)),
		raw_input()

