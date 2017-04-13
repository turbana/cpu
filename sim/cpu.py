#!/usr/bin/python

import argparse
import collections
import fcntl
import inspect
import os
import random
import sys
import termios
import threading
import time

import asm.encoding
import asm.tokens
import debugger
import listeners


MAGIC_HEADER = 0xDEADF00D
TIMER_PERIOD = 250

# device addresses (within data segment 0)
DEV_PIC   = 0xFF80
DEV_UART0 = 0xFF90
DEV_UART1 = 0xFFA0
DEV_555   = 0xFFB0
DEV_IDE   = 0xFFC0

DEV_MASK  = 0xFFF0

# IRQ assignments
IRQ_IDE   = 2
IRQ_UART0 = 3
IRQ_UART1 = 4
IRQ_555   = 6

# address bus is 23 bits: segment (6), data/instruction (1), addr (16)
ADDR_BUS_WIDTH = 23
REGISTER_COUNT = 16

# segment register width in bits
DSEG_WIDTH = 6
CSEG_WIDTH = 6
DSEG_SIZE  = 2**DSEG_WIDTH
CSEG_SIZE  = 2**CSEG_WIDTH
DSEG_POS   = 10
CSEG_POS   = 4

ADDR_TYPE_D = 0
ADDR_TYPE_I = 1

# registers
R_ZERO   = 0
R_PC     = 8
R_FLAGS  = 9
R_EPC    = 10
R_EFLAGS = 11

# $flags register (bit masks)
FLAGS_IE   = 0x0001
FLAGS_M    = 0x0002
FLAGS_CSEG = 0x03F0
FLAGS_DSEG = 0xFC00


def sbin(n, x=0):
    return bin(n)[2:].zfill(x)


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
    "eq":   lambda x, y: twoc_sign(x) == twoc_sign(y),
    "ne":   lambda x, y: twoc_sign(x) != twoc_sign(y),
    "lt":   lambda x, y: twoc_sign(x) <  twoc_sign(y),
    "lte":  lambda x, y: twoc_sign(x) <= twoc_sign(y),
    "gt":   lambda x, y: twoc_sign(x) >  twoc_sign(y),
    "gte":  lambda x, y: twoc_sign(x) >= twoc_sign(y),
    "ult":  lambda x, y: twoc_unsign(x) < twoc_unsign(y),
    "ulte": lambda x, y: twoc_unsign(x) <= twoc_unsign(y),
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
    raise Exception(
        "Instruction not defined: %s (%s)" % (tok.name, ", ".join(argnames)))


#
# Operations
#


@op
def ldw(cpu, tgt, base, offset):
    cpu.rset(tgt, cpu.mget(base + offset))


@op                             # noqa: F811
def ldw(cpu, tgt, base, index):
    cpu.rset(tgt, cpu.mget(base + index))


@op
def stw(cpu, base, src, offset):
    cpu.mset((offset + base), src)


@op                             # noqa: F811
def stw(cpu, base, src, index):
    cpu.mset(index + base, src)


@op
def jmp(cpu, offset):
    # decrement PC as we've already incremented it in cpu.fetch()
    cpu.reg[R_PC] += offset - 1
    cpu.stall(2)


@op                             # noqa: F811
def jmp(cpu, index, base):
    cpu.reg[R_PC] = base + index
    cpu.stall(2)


@op
def add(cpu, tgt, op1, op2):
    cpu.rset(tgt, op1 + op2)


@op
def sub(cpu, tgt, op1, op2):
    res = twoc_unsign(op1 - op2)
    cpu.rset(tgt, res)


@op
def and_(cpu, tgt, op1, op2):
    cpu.rset(tgt, op1 & op2)


@op
def or_(cpu, tgt, op1, op2):
    cpu.rset(tgt, op1 | op2)


@op
def xor(cpu, tgt, op1, op2):
    cpu.rset(tgt, op1 ^ op2)


@op
def s(cpu, cond, op1, op2):
    func = condition_func[cond]
    if func(op1, op2):
        cpu.reg[R_PC] += 1
        cpu.stall()


@op
def as_z(cpu, op1, op2, tgt):
    res = (op1 + op2) & 0xFFFF
    cpu.rset(tgt, res)
    if res == 0:
        cpu.reg[R_PC] += 1
        cpu.stall()


@op
def as_nz(cpu, op1, op2, tgt):
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
def shl(cpu, op1, op2, tgt):
    cpu.rset(tgt, op1 << op2)


@op
def shr(cpu, op1, op2, tgt):
    cpu.rset(tgt, op1 >> op2)


@op
def sar(cpu, op1, op2, tgt):
    res = op1 >> op2
    mask = ~(2**(16 - op2) - 1) if op1 & 0x8000 else 0
    cpu.rset(tgt, res | mask)


@op
def iret(cpu):
    cpu.reg[R_PC] = cpu.reg[R_EPC]
    cpu.reg[R_FLAGS] = cpu.reg[R_EFLAGS] | FLAGS_IE
    cpu.stall(3)


@op
def lcr(cpu, tgt, cr):
    cpu.rset(tgt, cpu.crget(cr))


@op
def scr(cpu, cr, src):
    def update():
        cpu.crset(cr, src)
        cpu._load_segment(cpu.dsegment)
        cpu._load_segment(cpu.csegment)
    # if we're setting $flags, we need to wait one cycle before it takes effect
    if cr + 8 == R_FLAGS:
        cpu.after(1, update)
    else:
        update()


@op
def ldiw(cpu, tgt, base, index):
    cpu.rset(tgt, cpu.iget(base + index))


@op
def stiw(cpu, base, src, index):
    cpu.iset(index + base, cpu.rget(src))


@op
def sex(cpu, tgt, src):
    val = src & 0x00FF
    high = 0xFF00 if (val & 0x0080) else 0
    cpu.rset(tgt, high | val)


@op
def halt(cpu):
    cpu.halt = True


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
        self.reg = [0] * REGISTER_COUNT
        self.mem = [None] * max(DSEG_SIZE, CSEG_SIZE)
        self.devices = []
        self.pic = None
        self.halt = False
        self.real_clock = real_clock
        self.clock = (4 if real_clock else 0) - 1
        self.listeners = collections.defaultdict(list)
        self.mem_write_reg = None
        self.stalls = 0
        self._randomize = False
        self._loaded_segments = set()
        self._after = []

    def after(self, cycles, func):
        self._after.append([cycles, func])

    def randomize(self):
        self._randomize = True
        word = lambda: random.randint(0, 2**(16 - 1))
        self.reg = [word() for _ in range(REGISTER_COUNT)]

    @property
    def dsegment(self):
        seg = (self.reg[R_FLAGS] & FLAGS_DSEG) >> DSEG_POS
        self._load_segment(seg)
        return seg

    @property
    def csegment(self):
        seg = (self.reg[R_FLAGS] & FLAGS_CSEG) >> CSEG_POS
        self._load_segment(seg)
        return seg

    def _load_segment(self, seg):
        if seg not in self._loaded_segments:
            if self._randomize:
                word = lambda: random.randint(0, 2**(16 - 1))
            else:
                word = lambda: 0
            self.mem[seg] = [
                [word() for _ in range(2**16)],  # data
                [word() for _ in range(2**16)],  # instruction
            ]
            self._loaded_segments.add(seg)

    @send_listeners
    def dload(self, (addr, words)):
        seg = self.dsegment
        for i, word in enumerate(words):
            self.mem[seg][ADDR_TYPE_D][addr + i] = word

    @send_listeners
    def iload(self, (addr, words)):
        seg = self.csegment
        for i, word in enumerate(words):
            self.mem[seg][ADDR_TYPE_I][addr + i] = word

    @send_listeners
    def run(self):
        self.reset()
        while not self.halt:
            self.cycle()

    @send_listeners
    def reset(self):
        self.reg[R_PC] = 0
        self.reg[R_FLAGS] = 0

    @send_listeners
    def cycle(self):
        self.tick()
        if (self.reg[R_FLAGS] & FLAGS_IE) and self.pic.int:
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
        def _expand_arg(name, arg):
            if isinstance(arg, asm.tokens.ImmRegister):
                arg = arg.value
            lookup = name not in ("tgt", "cr")
            if isinstance(arg, asm.tokens.Register) and lookup:
                return self.rget(arg.value)
            return arg.value
        func = lookup_op(tok)
        args = {k: _expand_arg(k, v) for k, v in tok.arguments().items()}
        func(self, **args)

    def stall(self, count=1):
        self.stalls += count

    def update_clock(self, token):
        self.clock += 1
        if not self.real_clock or token is None:
            return
        # stall this instruction on register read after memory fetch
        tgt = getattr(token, "tgt", None)
        read_args = [str(arg) for arg in token.args if not arg == tgt]
        if self.mem_write_reg in read_args:
            self.clock += 1
        reg = str(tgt) if token.name in ("ldw", "ldiw") else None
        self.mem_write_reg = reg

    @send_listeners
    def do_interrupt(self):
        # save state
        self.reg[R_EPC] = self.reg[R_PC]
        self.reg[R_EFLAGS] = self.reg[R_FLAGS]
        # disable interrupts, enter supervisor mode
        self.reg[R_FLAGS] = 0
        # jump to isr
        self.reg[R_PC] = self.pic.isr
        # stall
        self.stall(6)
        return self.pic.irq

    @send_listeners
    def fetch(self):
        pc = self.reg[R_PC]
        self.reg[R_PC] = (pc + 1) & 0xFFFF
        self._check_addr(pc)
        # read from code segment when in user mode, supervisor mode is always
        # segment 0
        seg = self.csegment if (self.reg[R_FLAGS] & FLAGS_M) else 0
        return self.mem[seg][ADDR_TYPE_I][pc]

    @send_listeners
    def iget(self, addr):
        self._check_addr(addr)
        return self.mem[self.csegment][ADDR_TYPE_I][addr]

    @send_listeners
    def iset(self, addr, word):
        self._check_addr(addr)
        self.mem[self.csegment][ADDR_TYPE_I][addr] = word

    @send_listeners
    def mget(self, addr):
        self._check_addr(addr)
        value = self.device_read(addr)
        if value is None:
            value = self.mem[self.dsegment][ADDR_TYPE_D][addr]
        return value

    @send_listeners
    def mset(self, addr, word):
        self._check_addr(addr)
        if not self.device_write(addr, word):
            self.mem[self.dsegment][ADDR_TYPE_D][addr] = word

    def _check_addr(self, addr):
        if addr >= 2**16:
            raise Exception("Invalid memory access: %04X" % addr)

    @send_listeners
    def rget(self, reg):
        if reg == R_ZERO:
            return 0
        return self.reg[reg]

    @send_listeners
    def rset(self, reg, value):
        # ignore writes to $0 and (in user mode) writes to control registers
        if reg == R_ZERO or (reg >= 8 and self.reg[R_FLAGS] & FLAGS_M):
            return self.rget(reg)
        self.reg[reg] = (value & 0xFFFF)
        return self.rget(reg)

    @send_listeners
    def crget(self, cr):
        cr += 8
        val = self.reg[cr]
        # decrement when reading PC as we've already incremented in fetch()
        if cr == R_PC:
            val -= 1
        # control register reads from user mode return 0
        if self.reg[R_FLAGS] & FLAGS_M:
            return 0
        return val

    @send_listeners
    def crset(self, cr, value):
        cr += 8
        # ignore writes to $pc and (in user mode) writes to control registers
        if cr == R_PC or self.reg[R_FLAGS] & FLAGS_M:
            return self.crget(cr - 8)
        self.reg[cr] = (value & 0xFFFF)
        return self.crget(cr - 8)

    def add_listener(self, listener):
        for attr in dir(listener):
            if attr.startswith("before_") or attr.startswith("after_"):
                self.listeners[attr].append(getattr(listener, attr))

    def add_device(self, device, mask):
        self.devices.append((mask, device))

    def tick(self):
        # tick each device
        for mask, device in self.devices:
            device.tick()
        # check for upcoming tasks
        for i in range(len(self._after)):
            task = self._after[i]
            if task[0] == 0:
                self._after.remove(task)
                task[1]()
                i -= 1
            else:
                task[0] -= 1

    def device_read(self, addr):
        for dev_addr, device in self.devices:
            if (addr & DEV_MASK) == dev_addr:
                register = addr & ~DEV_MASK
                return device.read(register)
        return None

    def device_write(self, addr, value):
        for dev_addr, device in self.devices:
            if (addr & DEV_MASK) == dev_addr:
                register = addr & ~DEV_MASK
                device.write(register, value)
                return True
        return False


def dump_short(cpu):
    for r in xrange(1, 10):
        v = cpu.reg[r]
        name = ("$%d" % r) if r < 8 else ("$cr%d" % (r - 8))
        # print to stdout for runtest.sh
        print "%s 0x%04X" % (name, v)


#
# Devices
#


class Device(object):
    def tick(self):
        pass

    def read(self, addr):
        return 0

    def write(self, addr, value):
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

    def read(self, addr):
        return self.count

    def write(self, addr, value):
        self.count = value


class PICDevice(Device):
    def __init__(self, cpu):
        self.devices = [None] * 8
        self.cpu = cpu
        self.pending = 0
        self.idt = None

    @property
    def int(self):
        return self.pending != 0

    @property
    def isr(self):
        if self.idt is None:
            show("pic error: interrupt serviced before programming PIC")
            sys.exit(1)
        if self.irq is None:
            show("pic error: interrupt serviced before interrupt raised")
            sys.exit(1)
        return self.idt | self.irq

    @property
    def irq(self):
        for irq in range(8):
            if self.pending & (1 << irq):
                return irq
        return None

    def register(self, dev, irq):
        self.devices[irq] = dev
        dev.pic = self

    def interrupt(self, dev):
        irq = self.devices.index(dev)
        self.pending |= 1 << irq

    def write(self, addr, value):
        value &= 0x00FF
        # ICW1
        if addr == 0 and (value & 0x10):
            self.pending = 0
        # ICW2
        elif addr == 1:
            self.idt = value & 0xF8
        # OCW2
        elif addr == 0 and (value & 0x18) == 0:
            eoi = (value & 0x20) >> 5
            sl = (value & 0x40) >> 6
            level = (value & 0x03)
            if eoi:
                level = self.irq if not sl else level
                self.pending &= ~(1 << level)
        else:
            args = (addr, value)
            show("pic error: unexpected write: reg=%d val=0x%02X" % args)
            sys.exit(1)


class KeyboardDevice(Device):
    def __init__(self):
        self.lock = threading.Lock()
        self.buffer = []
        self.pic = None # set in pic device
        t1 = threading.Thread(target=keyboard_thread,
                              args=(self.lock, self.buffer))
        t1.daemon = True
        t1.start()

    def tick(self):
        with self.lock:
            if self.buffer:
                self.pic.interrupt(self)

    def read(self, addr):
        with self.lock:
            return self.buffer.pop() if self.buffer else 0

    def write(self, addr, value):
        if value is not None:
            show("keyboard error: tried to write value:", value, "\n")
            sys.exit(1)


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

    def read(self, addr):
        return self.buffer.pop(0) if self.buffer else 0

    def write(self, addr, value):
        if value is not None:
            self.buffer.append(value)


class ScreenDevice(Device):
    def write(self, addr, value):
        sys.stdout.write(chr(value & 0x00FF))


def load_devices(cpu, keyboard=False):
    pic = PICDevice(cpu)
    timer = TimerDevice(TIMER_PERIOD)
    if keyboard:
        kb = KeyboardDevice()
    else:
        kb = NullKeyboardDevice()
    scr = ScreenDevice()
    pic.register(timer, IRQ_555)
    pic.register(kb, IRQ_UART0)
    pic.register(scr, IRQ_UART1)
    cpu.add_device(pic, DEV_PIC)
    cpu.add_device(kb, DEV_UART0)
    cpu.add_device(scr, DEV_UART1)
    cpu.add_device(timer, DEV_555)
    cpu.pic = pic


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
    def addr(s):
        return int(s, 16) # def'd so that "addr" will show in error messages
    binfile = argparse.FileType("rb")
    tracefile = argparse.FileType("w")
    parser = argparse.ArgumentParser(
        description="Functional simulator for TIM-16 cpu",
        usage="%(prog)s [exe] [options]")

    add = parser.add_argument
    add("exe", nargs="?", type=binfile, help="load executable into memory")
    add("--stop-clock", metavar="CLOCK", dest="stop_clock", type=int,
        help="stop execution upon reaching CLOCK")
    add("--no-randomize", dest="randomize", action="store_false",
        help="don't randomize all memory and registers before execution")
    add("--no-check-errors", dest="check_errors", action="store_false",
        help="don't check for errors (e.x. mem read before write)")
    add("--no-realistic-clock", dest="real_clock", action="store_false",
        help="report clock count from WB stage (includes bubbles)")
    # add("--start-at", metavar="ADDR", dest="start", type=addr,
    #     help="start executing at instruction memory ADDR")
    add("--keyboard", dest="keyboard", action="store_true",
        help="enable keyboard input (conflicts with debugger)")
    # add("--clock-speed", dest="clock_speed", metavar="HZ", type=int,
    #     help="run at HZ clock speed with realistic delay")
    add("--save-replay", dest="replay", metavar="FILE",
        help="save replay to file (used to generate tests)")

    # group = parser.add_argument_group("load-options")
    # add = group.add_argument
    # add("--load-rom", metavar="FILE", dest="rom", type=binfile,
    #     help="load FILE into ROM")
    # add("--load-serial-0", metavar="FILE", dest="uarta", type=binfile,
    #     help="UART0 reads from FILE")
    # add("--load-serial-1", metavar="FILE", dest="uartb", type=binfile,
    #     help="UART1 reads from FILE")
    # add("--load-data", metavar="FILE", dest="data", type=binfile,
    #     help="load FILE into data memory at address 0")
    # add("--load-inst", metavar="FILE", dest="inst", type=binfile,
    #     help="load FILE into instruction memory at address 0")

    group = parser.add_argument_group("debugger-options")
    add = group.add_argument
    add("--no-debugger", dest="debug", action="store_false",
        help="start without debugger")
    add("--breakpoints", metavar="ADDR", dest="breakpoints", type=addr,
        nargs="+", help="set debugger breakpoints")
    # TODO other debugger options

    group = parser.add_argument_group("output-options")
    add = group.add_argument
    add("--trace", metavar="FILE", dest="trace", type=tracefile,
        help="trace data sent to FILE")
    add("--test-clock", metavar="CLOCK", dest="test_clocks", type=int,
        nargs="+", default=[None], help="display test output at each CLOCK")
    add("--test-clock-rate", metavar="COUNT", dest="test_clock_rate", type=int,
        help="display test output every COUNT clocks")
    # TODO configure test output

    if not args:
        parser.print_help()
        sys.exit(2)

    return parser.parse_args(args)


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
        tester = listeners.TestOutput(cpu, opts.test_clock_rate,
                                      opts.test_clocks)
        cpu.add_listener(tester)

    if opts.stop_clock:
        stopper = listeners.StopClock(cpu, opts.stop_clock)
        cpu.add_listener(stopper)

    if opts.replay:
        stream = open(opts.replay, "w")
        replay = listeners.ReplayGenerator(cpu, stream)
        cpu.add_listener(replay)

    if opts.exe:
        chunks = parse_file(opts.exe)
        cpu.reset()
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
