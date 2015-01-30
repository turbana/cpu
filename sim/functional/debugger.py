import readline

import asm.encoding

PC    = 8 # register
FLAGS = 9
EPC   = 10
REGISTER_COUNT = 10


def hex_word(n):
	h = hex(n)[2:].upper().zfill(4)
	return h

def hex_byte(n):
	return hex(n)[2:].upper().zfill(2)

def bin_word(n):
	b = bin(n)[2:].zfill(16)
	return "%s %s  %s %s" % (b[0:4], b[4:8], b[8:12], b[12:16])


def dump(mem, mstart=None, mend=None):
	if mstart is not None and mend is not None:
		for i, addr in enumerate(range(mstart*2, mend*2, 2)):
			if (i % 8) == 0:
				if i > 0:
					print
				print "%04X | " % (addr/2),
			word = (mem[addr] << 8) | mem[addr+1]
			print "%04X" % word,
		print


def reg_dump(cpu, top_reg):
	for r in range(1, top_reg+1):
		v = cpu.reg[r]
		name = ("  $%d" % r) if r < 8 else ("$cr%d" % (r-8))
		print "%s:  %s  |  %s  =  %5s" % (name, bin_word(v), hex_word(v), v)


class Debugger(object):
	def __init__(self, cpu):
		self.cpu = cpu
		self.step = False
		self.drange = [0, 0]
		self.irange = [0, 0]
		self.brk_addrs = set()
		self.brk_opcodes = set()

	def before_dload(self, _, bytes):
		self.drange[1] = len(bytes) / 2

	def before_run(self, *args):
		self.normal_dump()
		self.command()

	def before_fetch(self, _):
		if self.cpu.reg[PC] in self.brk_addrs:
			self.step = True

	def after_fetch(self, opcode):
		if self.step:
			self.normal_dump(opcode)

	def normal_dump(self, opcode=None):
		print " "*40 + "clock:", self.cpu.clock
		reg_dump(self.cpu, 7)
		if sum(self.drange):
			print
			dump(self.cpu.dmem, *self.drange)
		print
		if opcode is not None:
			inst = asm.encoding.decode(opcode)
			print "%04X> %s" % (self.cpu.reg[PC]-1, str(inst).replace("\t", " "))
			print
		self.command()

	def command(self):
		done = False
		while not done:
			try:
				cmd = raw_input("> ").lower().split()
				if not cmd:
					if self.step:
						done = True
				elif cmd[0] in ("s", "step"):
					self.step = True
					done = True
				elif cmd[0] in ("r", "run"):
					self.step = False
					done = True
				elif cmd[0] == "b":
					if len(cmd) == 1:
						for brk in sorted(self.brk_addrs):
							print "@%04X" % brk
						for opcode in sorted(self.brk_opcodes):
							print "$%04X" % opcode
					else:
						addr = int(cmd[1], 16)
						self.brk_addrs.add(addr)
				elif cmd[0] == "bo":
					opcode = int(cmd[1], 16)
					self.brk_opcodes.add(opcode)
				elif cmd[0] == "rb":
					val = int(cmd[1], 16)
					self.brk_addrs.remove(val)
				elif cmd[0] == "rbo":
					val = int(cmd[1], 16)
					self.brk_opcodes.remove(val)
				elif cmd[0] == "mem":
					addr1 = int(cmd[1], 16)
					addr2 = int(cmd[2], 16) if len(cmd) == 3 else addr1
					dump(self.cpu.dmem, addr1, addr2 + 1)
				elif cmd[0] == "imem":
					addr1 = int(cmd[1], 16)
					addr2 = int(cmd[2], 16) if len(cmd) == 3 else addr1
					dump(self.cpu.imem, addr1, addr2 + 1)
				elif cmd[0] == "memr":
					addr1 = int(cmd[1], 16)
					addr2 = int(cmd[2], 16)
					self.drange = [addr1, addr2]
				elif cmd[0] == "regs":
					print
					reg_dump(self.cpu, REGISTER_COUNT)
					print
				elif cmd[0] == "mem!":
					addr = int(cmd[1], 16)
					val = int(cmd[2], 16)
					self.cpu.mset(addr*2, val, byte=False)
				elif cmd[0] == "imem!":
					addr = int(cmd[1], 16)
					val = int(cmd[2], 16)
					self.cpu.iset(addr*2, val, byte=False)
				elif cmd[0] == "dis":
					addr1 = int(cmd[1], 16)
					addr2 = int(cmd[2], 16) if len(cmd) == 3 else addr1
					for addr in range(addr1*2, (addr2+1)*2, 2):
						inst = asm.encoding.decode(self.cpu.iget(addr))
						print "%04X> %s" % (addr/2, inst)
				elif cmd[0] in ("?", "h", "help"):
					print "s|step            step"
					print "r|run             run"
					print "b [addr]          show breakpoints / add breakpoint (addr)"
					print "bo op             add breakpoint (opcode)"
					print "rb addr           remove breakpoint (addr)"
					print "rbo op            remove breakpoint (opcode"
					print "mem addr [addr]   dump data memory between addrs"
					print "imem addr [addr]  dump instruction memory between addrs"
					print "memr addr addr    set memory dump range"
					print "regs              show all registers"
					print "mem! addr val     set data mem @addr to val"
					print "imem! addr val    set instruction mem @addr to val"
					#print "reg! reg val      set register to val"
					#print "io addr           read io port @addr"
					#print "io! addr val      set io port @addr to val"
					print "dis addr [addr]   disassemble imem"
				else:
					print "unknown command:", " ".join(cmd)
			except EOFError:
				self.cpu.halt = True
				done = True
				print
			except Exception, e:
				print "error:", e
