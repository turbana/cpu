import readline
import sys

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

def show(*strs):
	sys.stdout.write(" ".join(map(str, strs)))


def dump(mem, mstart=None, mend=None):
	if mstart is not None and mend is not None:
		for i, addr in enumerate(range(mstart*2, mend*2, 2)):
			if (i % 8) == 0:
				if i > 0:
					show("\n")
				show("%04X | " % (addr/2))
			word = (mem[addr] << 8) | mem[addr+1]
			show("%04X" % word)
		show("\n")


def reg_dump(cpu, top_reg):
	for r in range(1, top_reg+1):
		v = cpu.reg[r]
		name = ("  $%d" % r) if r < 8 else ("$cr%d" % (r-8))
		show("%s:  %s  |  %s  =  %5s\n" % (name, bin_word(v), hex_word(v), v))


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
		show(" "*40 + "clock:", self.cpu.clock, "\n")
		reg_dump(self.cpu, 7)
		if sum(self.drange):
			show("\n")
			dump(self.cpu.dmem, *self.drange)
		show("\n")
		if opcode is not None:
			inst = asm.encoding.decode(opcode)
			show("%04X> %s\n" % (self.cpu.reg[PC]-1, str(inst).replace("\t", " ")))
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
							show("@%04X\n" % brk)
						for opcode in sorted(self.brk_opcodes):
							show("$%04X\n" % opcode)
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
					show("\n")
					reg_dump(self.cpu, REGISTER_COUNT)
					show("\n")
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
						show("%04X> %s\n" % (addr/2, inst))
				elif cmd[0] in ("?", "h", "help"):
					show("s|step            step\n")
					show("r|run             run\n")
					show("b [addr]          show breakpoints / add breakpoint (addr)\n")
					show("bo op             add breakpoint (opcode)\n")
					show("rb addr           remove breakpoint (addr)\n")
					show("rbo op            remove breakpoint (opcode\n")
					show("mem addr [addr]   dump data memory between addrs\n")
					show("imem addr [addr]  dump instruction memory between addrs\n")
					show("memr addr addr    set memory dump range\n")
					show("regs              show all registers\n")
					show("mem! addr val     set data mem @addr to val\n")
					show("imem! addr val    set instruction mem @addr to val\n")
					#show("reg! reg val      set register to val\n")
					#show("io addr           read io port @addr\n")
					#show("io! addr val      set io port @addr to val\n")
					show("dis addr [addr]   disassemble imem\n")
				else:
					show("unknown command:", " ".join(cmd))
			except EOFError:
				self.cpu.halt = True
				done = True
				show("\n")
			except Exception, e:
				show("error:", e, "\n")
