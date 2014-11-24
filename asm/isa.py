
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




add("ldw tgt:reg, offset:s7(base:reg)",
	0x0, 13, ("offset", 12, 6), ("base", 5, 3), ("tgt", 2, 0))

add("ldb tgt:reg, offset:s7(base:reg)",
	0x1, 13, ("offset", 12, 6), ("base", 5, 3), ("tgt", 2, 0))

add("stw offset:s7(base:reg), src:reg",
	0x2, 13, ("offset", 12, 6), ("base", 5, 3), ("src", 2, 0))

add("stb offset:s7(base:reg), src:reg",
	0x3, 13, ("offset", 12, 6), ("base", 5, 3), ("src", 2, 0))


add("jmp offset:s13",
	0x4, 13, ("offset", 12, 0))


add("add tgt:reg, op1:reg, op2:ireg",
	0x28, 10, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("sub tgt:reg, op1:reg, op2:ireg",
	0x29, 10, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("and tgt:reg, op1:reg, op2:ireg",
	0x2A, 10, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("or tgt:reg, op1:reg, op2:ireg",
	0x2B, 10, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("s.cond:cond op1:reg, op2:ireg",
	0x2C, 10, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("cond", 2, 0))

add("as.z tgt:reg, op1:reg, op2:ireg",
	0x2D, 10, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("as.nz tgt:reg, op1:reg, op2:ireg",
	0x2E, 10, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))

add("xor tgt:reg, op1:reg, op2:ireg",
	0x2F, 10, ("ir", 9, 9), ("op1", 8, 6), ("op2", 5, 3), ("tgt", 2, 0))


add("lui tgt:reg, imm:s8",
	0x18, 11, ("imm", 10, 3), ("tgt", 2, 0))

add("addi tgt:reg, imm:s8",
	0x19, 11, ("imm", 10, 3), ("tgt", 2, 0))


add("ldw tgt:reg, index:reg(base:reg)",
	0x68,  9, ("index", 8, 6), ("base", 5, 3), ("tgt", 2, 0))

add("ldb tgt:reg, index:reg(base:reg)",
	0x69,  9, ("index", 8, 6), ("base", 5, 3), ("tgt", 2, 0))

add("stw index:reg(base:reg), src:reg",
	0x6A,  9, ("index", 8, 6), ("base", 5, 3), ("src", 2, 0))

add("stb index:reg(base:reg), src:reg",
	0x6B,  9, ("index", 8, 6), ("base", 5, 3), ("src", 2, 0))


add("shl tgt:reg, src:reg",
	0x360, 6, ("src", 5, 3), ("tgt", 2, 0))

add("shr tgt:reg, src:reg",
	0x361, 6, ("src", 5, 3), ("tgt", 2, 0))

add("sext tgt:reg, src:reg",
	0x362, 6, ("src", 5, 3), ("tgt", 2, 0))

add("sar tgt:reg, src:reg",
	0x363, 6, ("src", 5, 3), ("tgt", 2, 0))

add("inw tgt:reg, src:reg",
	0x364, 6, ("src", 5, 3), ("tgt", 2, 0))

add("inb tgt:reg, src:reg",
	0x365, 6, ("src", 5, 3), ("tgt", 2, 0))

add("outw tgt:reg, src:reg",
	0x366, 6, ("tgt", 5, 3), ("src", 2, 0))

add("outb tgt:reg, src:reg",
	0x367, 6, ("tgt", 5, 3), ("src", 2, 0))


add("halt",
	0xFEDE, 0)

add("trap sysnum:u4",
	0xFEE, 4, ("sysnum", 3, 0))

add("jmp tgt:reg",
	0x1FDF, 3, ("tgt", 2, 0))

add("lcr tgt:reg, cr:creg",
	0x3FE, 6, ("cr", 5, 3), ("tgt", 2, 0))

add("scr cr:creg, src:reg",
	0x3FF, 6, ("cr", 5, 3), ("src", 2, 0))


conditions = {"eq": 0, "ne": 1, "gt": 2, "gte": 3, "lt": 4, "lte":5, "ult": 6, "ulte": 7}
conditions_rev = dict(zip(conditions.values(), conditions.keys()))
immediates = {8: 0, 4: 1, 2: 2, 1: 3, -1: 4, -2: 5, -4: 6, -8: 7}
immediates_rev = dict(zip(immediates.values(), immediates.keys()))
