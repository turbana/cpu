import sys

import encoding
import grammer


def main(args):
	if len(args) != 1:
		print "USAGE: dis file.o"
		return 2
	grammer.grammer() # call to build encoding formats
	bytes = map(ord, open(args[0], "rb").read())
	for i in xrange(len(bytes)/2):
		j = i * 2
		word = (bytes[j] << 8) | bytes[j+1]
		print "%04X: %s" % (i, encoding.decode(word))


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
