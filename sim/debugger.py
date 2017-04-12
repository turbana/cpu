import sys

import asm.encoding

PC    = 8 # register
FLAGS = 9
EPC   = 10
REGISTER_COUNT = 11

ADDR_TYPE_D = 0
ADDR_TYPE_I = 1


def hex_word(n):
    h = hex(n)[2:].upper().zfill(4)
    return h


def hex_byte(n):
    return hex(n)[2:].upper().zfill(2)


def bin_word(n):
    b = bin(n)[2:].zfill(16)
    return "%s %s  %s %s" % (b[0:4], b[4:8], b[8:12], b[12:16])


def twoc_sign(n):
    return (n - (2**16)) if n >= (2**15) else n


def show(*strs):
    sys.stdout.write(" ".join(map(str, strs)))


def dump(mem, mstart=None, mend=None):
    if mstart is not None and mend is not None:
        for i, addr in enumerate(range(mstart, mend)):
            if (i % 8) == 0:
                if i > 0:
                    show("\n")
                show("%04X | " % (addr))
            show("%04X " % mem[addr])
        show("\n")


def reg_dump(cpu, top_reg):
    for r in range(1, top_reg + 1):
        v = cpu.reg[r]
        name = ("  $%d" % r) if r < 8 else ("$cr%d" % (r - 8))
        show("%s:  %s  |  %s  =  %6s\n" % (
            name, bin_word(v), hex_word(v), twoc_sign(v)))


class segment_change(object):
    def __init__(self, cpu):
        self.cpu = cpu

    def __enter__(self):
        self.flags = self.cpu.reg[FLAGS]

    def __exit__(self, type, value, traceback):
        self.cpu.reg[FLAGS] = self.flags


class Debugger(object):
    def __init__(self, cpu):
        self.cpu = cpu
        self.step = True
        self.drange = [0, 0]
        self.irange = [0, 0]
        self.brk_addrs = set()
        self.brk_opcodes = set()
        self.segment = 0

    def before_dload(self, words):
        self.drange[1] = len(words)

    def before_iload(self, words):
        self.irange[1] = len(words)

    def before_fetch(self):
        if self.cpu.reg[PC] in self.brk_addrs:
            self.step = True

    def before_execute(self, token):
        if self.step:
            with segment_change(self.cpu):
                self.normal_dump(token)
                self.command()

    def before_crset(self, reg, value):
        if reg + 8 == FLAGS:
            self.segment = (value & 0xFC00) >> 10

    def normal_dump(self, token=None):
        show(" " * 40 + "clock:", self.cpu.clock, "\n")
        reg_dump(self.cpu, 7)
        if sum(self.drange):
            show("\n")
            mem = self.cpu.mem[self.segment][ADDR_TYPE_D]
            dump(mem, *self.drange)
        show("\n")
        if token is not None:
            words = asm.encoding.encode(token)
            opcode = (words[0] << 8 | words[1])
            show("%04X | (%04X)\t%s\n" % (self.cpu.reg[PC] - 1, opcode, token))

    def command(self):
        done = False
        while not done:
            try:
                cmd = raw_input("> ").lower().split()
                if not cmd:
                    if self.step:
                        done = True
                elif cmd[0] in ("q", "quit"):
                    self.cpu.halt = True
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
                    mem = self.cpu.mem[self.segment][ADDR_TYPE_D]
                    dump(mem, addr1, addr2 + 1)
                elif cmd[0] == "imem":
                    addr1 = int(cmd[1], 16)
                    addr2 = int(cmd[2], 16) if len(cmd) == 3 else addr1
                    mem = self.cpu.mem[self.segment][ADDR_TYPE_I]
                    dump(mem, addr1, addr2 + 1)
                elif cmd[0] == "memr":
                    addr1 = int(cmd[1], 16)
                    addr2 = int(cmd[2], 16) if len(cmd) == 3 else addr1
                    self.drange = [addr1, addr2 + 1]
                elif cmd[0] == "regs":
                    show("\n")
                    reg_dump(self.cpu, REGISTER_COUNT)
                    show("\n")
                elif cmd[0] == "mem!":
                    addr = int(cmd[1], 16)
                    val = int(cmd[2], 16)
                    self.cpu.mset(addr, val)
                elif cmd[0] == "imem!":
                    addr = int(cmd[1], 16)
                    val = int(cmd[2], 16)
                    self.cpu.iset(addr, val)
                elif cmd[0] == "dis":
                    if len(cmd) == 1:
                        addr1, addr2 = self.irange
                    else:
                        addr1 = int(cmd[1], 16)
                        addr2 = int(cmd[2], 16) if len(cmd) == 3 else addr1
                    for addr in range(addr1, addr2 + 1):
                        opcode = self.cpu.iget(addr)
                        inst = asm.encoding.decode(opcode)
                        show("%04X | (%04X)\t%s\n" % (addr, opcode, inst))
                elif cmd[0] == "reg!":
                    reg_mapping = {"$1": 1, "$2": 2, "$3": 3, "$4": 4,
                                   "$5": 5, "$6": 6, "$7": 7,
                                   "$cr0": 8, "$cr1": 9, "$cr2": 10}
                    in_mapping = cmd[1] in reg_mapping
                    reg = reg_mapping[cmd[1]] if in_mapping else int(reg[1])
                    val = int(cmd[2], 16)
                    self.cpu.rset(reg, val)
                elif cmd[0] == "seg":
                    seg = int(cmd[1], 16)
                    self.segment = seg
                    # set $flags now, will be reset after command
                    flags = self.cpu.reg[FLAGS]
                    flags = (seg << 10) | (seg << 4) | (flags & 3)
                    self.cpu.reg[FLAGS] = flags
                    # poke both memories to ensure they're loaded
                    self.cpu.mget(0)
                    self.cpu.iget(0)
                elif cmd[0] in ("?", "h", "help"):
                    show("q|quit            halts\n")
                    show("s|step            step\n")
                    show("r|run             run\n")
                    show("b [addr]          show breakpoints / add breakpoint (addr)\n") # noqa: E501
                    show("bo op             add breakpoint (opcode)\n")
                    show("rb addr           remove breakpoint (addr)\n")
                    show("rbo op            remove breakpoint (opcode)\n")
                    show("mem addr [addr]   dump data memory between addrs\n")
                    show("imem addr [addr]  dump instruction memory between addrs\n") # noqa: E501
                    show("memr addr addr    set memory dump range\n")
                    show("regs              show all registers\n")
                    show("mem! addr val     set data mem @addr to val\n")
                    show("imem! addr val    set instruction mem @addr to val\n") # noqa: E501
                    show("reg! reg val      set register to val\n")
                    show("dis addr [addr]   disassemble imem\n")
                    show("seg s             set current segment\n")
                else:
                    show("unknown command:", " ".join(cmd), "\n")
            except EOFError:
                self.cpu.halt = True
                done = True
                show("\n")
            except Exception, e:
                show("error:", e, "\n")
