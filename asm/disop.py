#!/usr/bin/python

import sys

import encoding


def main_old(args):
	stream = open("trace.log", "w")
	def trace(msg):
		stream.write(msg)
		stream.flush()
	trace("start\n")
	# for line in sys.stdin:
	while True:
		line = sys.stdin.read(5).strip()
		if not line: break
		trace("line=%s\n" % line)
		try:
			opcode = int(line, 16)
			trace("opcode=%d\n" % opcode)
		except ValueError:
			trace("invalid=%s\n" % line)
			#print "ERROR: invalid hex value: %s" % line.strip()
			#return 2
			sys.stdout.write("!%s\n" % line)
			sys.stdout.flush()
			continue
		sys.stdout.write(str(encoding.decode(opcode)))
		sys.stdout.write("\n")
		sys.stdout.flush()
	trace("done\n")


def main(args):
	# for line in sys.stdin:
	while True:
		line = sys.stdin.read(5).strip()
		if not line: break
		try:
			words = int(line, 16)
			opcode = str(encoding.decode(words))
			opcode = opcode.replace("\t", " ")
		except ValueError:
			opcode = "!%s" % line
		sys.stdout.write(opcode + "\n")
		sys.stdout.flush()

if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
