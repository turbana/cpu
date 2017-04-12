""" Translate tim object files to a format understood by verilog. """

import sys


DMEM_OFFSET = 0
IMEM_OFFSET = 1 << 22
TIM_HEADER = 0xDEADF00D


def main(args):
    if len(args) != 1:
        print "USAGE: %d compiled.o" % sys.argv[0]
        return 2
    ofile = open(args[0], "rb")
    header = read(ofile, 4)
    if header != TIM_HEADER:
        sys.stderr.write(
            "Error: Tim header missing: Expected 0x%04X received: 0x%04X" % (
                TIM_HEADER, header))
        return 1
    translate(ofile, sys.stdout, DMEM_OFFSET) # data chunks
    translate(ofile, sys.stdout, IMEM_OFFSET) # instruction chunks


def translate(stream, out, offset):
    chunks = read(stream, 2)
    for _ in range(chunks):
        addr = read(stream, 2) + offset
        out.write("@%X\n" % addr)
        words = read(stream, 2)
        for _ in range(words):
            word = read(stream, 2)
            out.write("%04X\n" % word)


def read(stream, bytes):
    value = 0
    for byte in stream.read(bytes):
        value <<= 8
        value |= ord(byte)
    return value


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
