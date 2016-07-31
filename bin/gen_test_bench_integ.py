""" generate integration test for TIM-16 """


import sys

import simtest


CLOCK_TICK = 1000
CLOCK_RUNOFF = 100
REGISTERS = {
	# reg: High, Low
	"$1": ("U119", "U118"),
	"$2": ("U121", "U120"),
	"$3": ("U123", "U122"),
	"$4": ("U125", "U124"),
	"$5": ("U127", "U126"),
	"$6": ("U129", "U128"),
	"$7": ("U131", "U130"),
}
# output wires from a 74377 (high to low)
WIRES = (19, 16, 15, 12, 9, 6, 5, 2)


def main(args):
	if len(args) != 1:
		print "USAGE: %s replay.file" % sys.argv[0]
		return 2
	replay = open(args[0])
	checks = simtest.parse(replay)
	emit_test_bench(sys.stdout, checks)


def emit_test_bench(stream, all_checks):
	last_clock = -1
	all_checks = sorted(all_checks.values(), key=lambda tup: tup[0])
	e = stream.write
	e("`timescale 1 ns / 100 ps\n\n")
	e("module tb_tim;\n\n")
	e("  reg _CLK;\n\n")
	e("  tim TIM(\n    ._CLK (_CLK)\n  );\n\n")
	e("  reg [15:0] _TB_VALUE;\n")
	e("  reg [3:0] _TB_REGISTER;\n")
	e("  integer _TB_ERRORS;\n")
	e("  integer _TB_CLOCK;\n")
	for n in range(1, 8):
		e("  wire [15:0] R%d;\n" % n)
	e("\n")
	for n in range(1, 8):
		refdes_high = REGISTERS["$" + str(n)][0]
		wires_high = " , ".join("TIM.DECODE_RF.%s.\\%d" % (refdes_high, wire) for wire in WIRES)
		refdes_low = REGISTERS["$" + str(n)][1]
		wires_low = " , ".join("TIM.DECODE_RF.%s.\\%d" % (refdes_low, wire) for wire in WIRES)
		wires = "{ %s , %s }" % (wires_high, wires_low)
		e("  assign R%d = %s;\n" % (n, wires))
	e("\n")
	e("  always #%s _CLK = ~_CLK;\n" % (CLOCK_TICK/8))
	e("  always @ (posedge TIM.CLOCK.CLK0) _TB_CLOCK = _TB_CLOCK + 1;\n\n")
	e("  initial\n    begin\n")
	e('      $dumpfile("build/waveforms/tim.vcd");\n')
	e("      $dumpvars;\n")
	e('      $readmemh("build/tim.bin", TIM.DEVICES.mem);\n')
	e("      _CLK = 0;\n")
	e("      _TB_CLOCK = -1; /* warmup */\n")
	e("      _TB_ERRORS = 0;\n")
	e('      _TB_REGISTER = 0;\n')
	e("      _TB_VALUE = 0;\n")
	e("      @(posedge TIM.CLOCK.CLK0)  /* warmup */\n\n")
	e("      /* test cases */\n")
	for clock, (reg_name, value) in all_checks:
		delta = clock - last_clock
		last_clock = clock
		reg = reg_name.replace("$", "R")
		expected = bin(value)[2:].zfill(16)
		e("\n")
		e("      /* @%d (%s=%04X) */\n" % (clock, reg_name, value))
		e("      #%d\n" % (delta * CLOCK_TICK))
		e('      _TB_REGISTER = %s;\n' % reg_name[1])
		e("      _TB_VALUE = %d;\n" % value)
		e("      if (%s !== %d) begin\n" % (reg, value))
		e("        _TB_ERRORS = _TB_ERRORS + 1;\n")
		# e('        $display("\\nFAIL @%d");\n'  % clock)
		# e('        $display("%8s=%%16b\\nExpected=%s", %s);\n' % (reg_name, expected, reg))
		e("      end\n")
	e("      /* end test bench */\n")
	e("      if (_TB_ERRORS > 0)\n")
	e("      begin\n")
	e('        $display("\\nFAILURE %d error(s) testing tim", _TB_ERRORS);\n')
	e("      end\n")
	e("      #%d\n" % (CLOCK_TICK * CLOCK_RUNOFF))
	e("      $finish;\n")
	e("    end\n")
	e("endmodule\n")


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
