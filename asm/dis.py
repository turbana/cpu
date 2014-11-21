import sys

import isa


def main(args):
	if len(args) != 1:
		print "USAGE: dis file.o"
		return 2
	bytes = map(ord, open(args[0], "rb").read())
	for i in xrange(len(bytes)/2):
		j = i * 2
		word = (bytes[j] << 8) | bytes[j+1]
		print "%04X: %s" % (i, isa.decode(word))


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
