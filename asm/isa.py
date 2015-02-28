
encodings = []

def _arg_sort_cmp(left, right):
	# ensure epc and ir come first in the argument list (helps decoding)
	if left[0] in ("epc", "ir"):
		return -1
	if right[0] in ("epc", "ir"):
		return 1
	return cmp(left[0], right[0])


def add(syntax, prelude, prelude_end, *args):
	name = syntax.split(" ")[0]
	if name.startswith("s."):
		name = "s"
	encodings.append({
		"name": name,
		"ast": None,
		"format": None,
		"syntax": syntax,
		"prelude": prelude,
		"prelude_end": prelude_end,
		"args": sorted(args, cmp=_arg_sort_cmp),
		"types": None,
	})


def parse_format(ast):
	inst = ast[0]
	if isinstance(inst, str):
		format = inst + "\t"
	for arg in ast[1:]:
		if not isinstance(arg, str):
			arg = "{%s}" % arg[0]
		format += arg
	return format.replace(",", ", ").replace("s\t.{cond}", "s.{cond}\t")



add("add tgt:reg, op1:reg, op2:ireg",
	0x00, 11, ("op2", 10, 7), ("ir", 6, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("sub tgt:reg, op1:reg, op2:ireg",
	0x01, 11, ("op2", 10, 7), ("ir", 6, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("and tgt:reg, op1:reg, op2:ireg",
	0x02, 11, ("op2", 10, 7), ("ir", 6, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("or tgt:reg, op1:reg, op2:ireg",
	0x03, 11, ("op2", 10, 7), ("ir", 6, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("s.cond:cond op1:reg, op2:ireg",
	0x04, 11, ("op2", 10, 7), ("ir", 6, 6), ("op1", 5, 3), ("cond", 2, 0))

add("as.z tgt:reg, op1:reg, op2:ireg",
	0x05, 11, ("op2", 10, 7), ("ir", 6, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("as.nz tgt:reg, op1:reg, op2:ireg",
	0x06, 11, ("op2", 10, 7), ("ir", 6, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("xor tgt:reg, op1:reg, op2:ireg",
	0x07, 11, ("op2", 10, 7), ("ir", 6, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("shl tgt:reg, op1:reg, op2:ireg",
	0x08, 11, ("op2", 10, 7), ("ir", 6, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("shr tgt:reg, op1:reg, op2:ireg",
	0x09, 11, ("op2", 10, 7), ("ir", 6, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("ldw tgt:reg, index:ireg(base:reg)",
	0x0A, 11, ("index", 10, 7), ("ir", 6, 6), ("base", 5, 3), ("tgt", 2, 0))

add("stw index:ireg(base:reg), src:reg",
	0x0B, 11, ("index", 10, 7), ("ir", 6, 6), ("base", 5, 3), ("src", 2, 0))

add("inb tgt:reg, src:reg",
	0x0C, 11, ("src", 5, 3), ("tgt", 2, 0))

add("outb tgt:reg, src:reg",
	0x0D, 11, ("src", 5, 3), ("tgt", 2, 0))

add("ldiw tgt:reg, src:reg",
	0x0E, 11, ("src", 5, 3), ("tgt", 2, 0))

add("stiw tgt:reg, src:reg",
	0x0F, 11, ("src", 5, 3), ("tgt", 2, 0))

add("lcr tgt:reg, cr:creg",
	0x10, 11, ("cr", 5, 3), ("tgt", 2, 0))

add("scr cr:creg, src:reg",
	0x11, 11, ("src", 5, 3), ("cr", 2, 0))

add("jal tgt:reg, index:ireg(base:reg)",
	0x12, 11, ("index", 10, 7), ("ir", 6, 6), ("base", 5, 3), ("tgt", 2, 0))

add("sar tgt:reg, op1:reg, op2:ireg",
	0x13, 11, ("op2", 10, 7), ("ir", 6, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("lui tgt:reg, imm:s8",
	0x14, 11, ("imm", 10, 3), ("tgt", 2, 0))

add("addi tgt:reg, imm:s8",
	0x15, 11, ("imm", 10, 3), ("tgt", 2, 0))

add("iret",
	0x16, 11)

add("jmp offset:s11",
	0x17, 11, ("offset", 10, 0))

add("ldw tgt:reg, offset:s7(base:reg)",
	0x6, 13, ("offset", 12, 6), ("base", 5, 3), ("tgt", 2, 0))

add("stw offset:s7(base:reg), src:reg",
	0x7, 13, ("offset", 12, 6), ("base", 5, 3), ("src", 2, 0))




conditions = {"eq": 0, "ne": 1, "gt": 2, "gte": 3, "lt": 4, "lte":5, "ult": 6, "ulte": 7}
conditions_rev = dict(zip(conditions.values(), conditions.keys()))
# positive special immediates are decremented by one before being encoded
imm_val = lambda n: 16+n if n < 0 else n-1
immediates = dict((n, imm_val(n)) for n in range(-8, 9) if n != 0)
immediates_rev = dict(zip(immediates.values(), immediates.keys()))
