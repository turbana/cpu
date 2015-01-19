import sys

import encoding


MAGIC_HEADER = 0xDEADF00D


def main(args):
	if len(args) != 1:
		print "USAGE: dis file.o"
		return 2
	out_stream = sys.stdout
	with open(args[0], "rb") as in_stream:
		if MAGIC_HEADER != read(in_stream, 4):
			print "ERROR: Magic header not found"
			return 1
		show_data(in_stream, out_stream)
		show_text(in_stream, out_stream)


def read(stream, bytes):
	value = 0
	for b in stream.read(bytes):
		value <<= 8
		value |= ord(b)
	return value


def show_data(data, out):
	length = read(data, 2)
	addr = 0
	for _ in range(length):
		word = read(data, 2)
		if addr % 8 == 0:
			out.write("\n%04X:" % addr)
		out.write(" %04X" % word)
		addr += 1
	if addr % 8 != 0:
		out.write("\n")
	out.write("\n")


def show_text(data, out):
	length = read(data, 2)
	for addr in range(length):
		word = read(data, 2)
		out.write("%04X: (%04X)  %s\n" % (addr, word, encoding.decode(word)))


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
