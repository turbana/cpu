
encodings = []


def _arg_sort_key(arg):
	# ensure ir come first in the argument list (helps decoding)
        name = arg[0]
        return "0"+name if name == "ir" else name


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
		"args": sorted(args, key=_arg_sort_key),
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
	0b00000, 11, ("op2", 10, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("and tgt:reg, op1:reg, op2:ireg",
	0b00001, 11, ("op2", 10, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("or tgt:reg, op1:reg, op2:ireg",
	0b00010, 11, ("op2", 10, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("xor tgt:reg, op1:reg, op2:ireg",
	0b00011, 11, ("op2", 10, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("shr tgt:reg, op1:reg, op2:ireg",
	0b00100, 11, ("op2", 10, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("sar tgt:reg, op1:reg, op2:ireg",
	0b00101, 11, ("op2", 10, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("shl tgt:reg, op1:reg, op2:ireg",
	0b00110, 11, ("op2", 10, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("sex tgt:reg, src:reg",
	0b00111, 11, ("src", 5, 3), ("tgt", 2, 0))

add("s.cond:cond op1:reg, op2:ireg",
	0b01000, 11, ("op2", 10, 6), ("op1", 5, 3), ("cond", 2, 0))

add("as.z tgt:reg, op1:reg, op2:ireg",
	0b01001, 11, ("op2", 10, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("as.nz tgt:reg, op1:reg, op2:ireg",
	0b01010, 11, ("op2", 10, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("jmp index:ireg(base:reg)",
	0b01011, 11, ("index", 10, 6), ("base", 5, 3))

add("ldw tgt:reg, index:ireg(base:reg)",
	0b01100, 11, ("index", 10, 6), ("base", 5, 3), ("tgt", 2, 0))

add("ldiw tgt:reg, index:ireg(base:reg)",
	0b01101, 11, ("index", 10, 6), ("base", 5, 3), ("tgt", 2, 0))

add("sub tgt:reg, op1:reg, op2:ireg",
	0b01110, 11, ("op2", 10, 6), ("op1", 5, 3), ("tgt", 2, 0))

add("stiw index:spec_imm(base:reg), src:reg",
	0b01111, 11, ("index", 10, 7), ("base", 5, 3), ("src", 2, 0))

add("ldw tgt:reg, offset:s7(base:reg)",
	0b100, 13, ("offset", 12, 6), ("base", 5, 3), ("tgt", 2, 0))

add("stw offset:s7(base:reg), src:reg",
	0b101, 13, ("offset", 12, 6), ("base", 5, 3), ("src", 2, 0))

add("lcr tgt:reg, cr:creg",
	0b11000, 11, ("cr", 5, 3), ("tgt", 2, 0))

add("scr cr:creg, src:reg",
	0b11001, 11, ("src", 5, 3), ("cr", 2, 0))

add("iret",
	0b11010, 11)

add("halt",
	0b11011, 11)

add("lui tgt:reg, imm:u8",
	0b11100, 11, ("imm", 10, 3), ("tgt", 2, 0))

add("addi tgt:reg, imm:s8",
	0b11101, 11, ("imm", 10, 3), ("tgt", 2, 0))

add("trap",
	0b11110, 11)

add("jmp offset:s11",
	0b11111, 11, ("offset", 10, 0))


conditions = {"eq": 0, "ne": 1, "gt": 2, "gte": 3, "lt": 4, "lte":5, "ult": 6, "ulte": 7}
conditions_rev = dict(zip(conditions.values(), conditions.keys()))
# unused code for special immediates
# positive special immediates are decremented by one before being encoded
imm_val = lambda n: 16+n if n < 0 else n-1
immediates = dict((n, imm_val(n)) for n in range(-8, 9) if n != 0)
immediates_rev = dict(zip(immediates.values(), immediates.keys()))
