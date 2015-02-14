#!/usr/bin/python

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
		dchunks = read_chunks(in_stream)
		ichunks = read_chunks(in_stream)
	show_chunks(dchunks, out_stream, decode=False)
	show_chunks(ichunks, out_stream, decode=True)


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


def show_chunks(chunks, stream, decode):
	for addr, words in chunks:
		if decode:
			stream.write("\n")
		for i,word in enumerate(words):
			if decode:
				stream.write("%04X | (%04X)   %s\n" % (addr+i, word, encoding.decode(word)))
			else:
				if i % 8 == 0:
					stream.write("\n%04X:" % (addr+i))
				stream.write(" %04X" % word)
		if not decode:
			stream.write("\n")


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
