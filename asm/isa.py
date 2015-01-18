
encodings = []

def add(syntax, prelude, prelude_end, *args):
	name = syntax.split(" ")[0]
	if name.startswith("s."):
		name = "s"
	#ast = grammer.add_instruction(syntax, tokens.Instruction)
	#print [a for a in ast[1:] if not isinstance(a, str)]
	#types = dict(a for a in ast[1:] if not isinstance(a, str))
	encodings.append({
		"name": name,
		"ast": None,
		"format": None, #parse_format(ast),
		"syntax": syntax,
		"prelude": prelude,
		"prelude_end": prelude_end,
		"args": args,
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
	0x00, 11, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("sub tgt:reg, op1:reg, op2:ireg",
	0x01, 11, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("and tgt:reg, op1:reg, op2:ireg",
	0x02, 11, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("or tgt:reg, op1:reg, op2:ireg",
	0x03, 11, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("s.cond:cond op1:reg, op2:ireg",
	0x04, 11, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("cond", 2, 0))

add("as.z tgt:reg, op1:reg, op2:ireg",
	0x05, 11, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("as.nz tgt:reg, op1:reg, op2:ireg",
	0x06, 11, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("xor tgt:reg, op1:reg, op2:ireg",
	0x07, 11, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("shl tgt:reg, op1:reg, op2:ireg",
	0x08, 11, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("shr tgt:reg, op1:reg, op2:ireg",
	0x09, 11, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("ldw tgt:reg, index:ireg(base:reg)",
	0x0A, 11, ("ir", 9, 9), ("index", 5, 3), ("base", 8, 6), ("tgt", 2, 0))

add("stw index:ireg(base:reg), src:reg",
	0x0B, 11, ("ir", 9, 9), ("index", 5, 3), ("base", 8, 6), ("src", 2, 0))

add("inb tgt:reg, src:reg",
	0x0C, 11, ("src", 8, 6), ("tgt", 2, 0))

add("outb tgt:reg, src:reg",
	0x0D, 11, ("src", 8, 6), ("tgt", 2, 0))

add("ldiw tgt:reg, src:reg",
	0x0E, 11, ("src", 8, 6), ("tgt", 2, 0))

add("stiw tgt:reg, src:reg",
	0x0F, 11, ("src", 8, 6), ("tgt", 2, 0))

add("lcr tgt:reg, cr:creg",
	0x10, 11, ("cr", 8, 6), ("tgt", 2, 0))

add("scr cr:creg, src:reg",
	0x11, 11, ("cr", 8, 6), ("src", 2, 0))

add("jmp tgt:reg",
	0x12, 11, ("tgt", 2, 0))

add("sext tgt:reg, src:reg",
	0x13, 11, ("src", 8, 6), ("tgt", 2, 0))

add("trap reg:reg",
	0x14, 11, ("reg", 2, 0))

# ...

add("lui tgt:reg, imm:s8",
	0x18, 11, ("imm", 10, 3), ("tgt", 2, 0))

add("addi tgt:reg, imm:s8",
	0x19, 11, ("imm", 10, 3), ("tgt", 2, 0))

add("ldw tgt:reg, offset:s5(base:reg)",
	0x1A, 11, ("offset", 10, 6), ("base", 5, 3), ("tgt", 2, 0))

add("stw offset:s5(base:reg), src:reg",
	0x1B, 11, ("offset", 10, 6), ("base", 5, 3), ("src", 2, 0))

# ...

add("reti",
	0x1E, 11)

add("jmp offset:s11",
	0x1F, 11, ("offset", 10, 0))




conditions = {"eq": 0, "ne": 1, "gt": 2, "gte": 3, "lt": 4, "lte":5, "ult": 6, "ulte": 7}
conditions_rev = dict(zip(conditions.values(), conditions.keys()))
immediates = {8: 0, 4: 1, 2: 2, 1: 3, -1: 4, -2: 5, -4: 6, -8: 7}
immediates_rev = dict(zip(immediates.values(), immediates.keys()))
