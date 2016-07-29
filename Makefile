
BUILD_DIR	= build
BIN_DIR		= bin
CONFIG_DIR	= etc
DESIGN_DIR	= design
SCHEM_DIR	= $(DESIGN_DIR)/schem
DOC_DIR		= doc
VERILOG_DIR	= design/verilog
WF_DIR		= $(BUILD_DIR)/waveforms
ASM_DIR		= tests

FAILON		= $(BIN_DIR)/failon.sh
GNETLIST	= gnetlist
GAF		= gaf
IVERILOG	= iverilog
GTKWAVE		= gtkwave
GSCHEM		= gschem
ASM		= asm/asm.py
SIM		= sim/cpu.py
SIM_TEST	= $(BIN_DIR)/simtest.py


ALL_BIN = test1
ALL_ASM = bigintadd bigintsub fib immediates macros pow testisa
ALL_SCHEMS = $(SCHEM_DIR)/*.sch
SCHEMS = $(filter-out $(wildcard $(SCHEM_DIR)/_*.sch),$(wildcard $(ALL_SCHEMS)))
DOC_SCHEMS = $(sort $(subst $(SCHEM_DIR),$(BUILD_DIR),$(SCHEMS)))
ALL_VERILOG = $(subst .sch,.v,$(DOC_SCHEMS))
# ALL_SCHEM_TESTS are populated in Makefile.deps
ALL_SCHEM_TESTS =
ALL_BIN_TESTS = $(addprefix $(BUILD_DIR)/,$(addsuffix .o.chk,$(ALL_BIN)))
ALL_ASM_TESTS = $(addprefix $(BUILD_DIR)/,$(addsuffix .o.test,$(ALL_ASM)))
ALL_TESTS = $(ALL_BIN_TESTS) $(ALL_ASM_TESTS) $(ALL_SCHEM_TESTS)


.PHONY: clean help netlist testbench test testall protopcb doc wave renum renumall versions decode
.PRECIOUS: $(BUILD_DIR)/%.v $(BUILD_DIR)/tb_%.v $(BUILD_DIR)/%.sch $(BUILD_DIR)/test_% $(WF_DIR)/%.vcd $(BUILD_DIR)/%.o

# show 'make help' by default
help:

# generate dependencies
Makefile.deps: $(ALL_SCHEMS) $(BIN_DIR)/make_dependencies.py
	@python $(BIN_DIR)/make_dependencies.py $(VERILOG_DIR)/*.v $(ALL_SCHEMS) > $@
-include Makefile.deps


# ##############################################################################
# MISC
# ##############################################################################

help:
	@echo "make target=foo nettest    -- run full netlist and testbench for foo"
	@echo "make target=foo netlist    -- generate netlist for foo"
	@echo "make target=foo testbench  -- generate testbench for foo"
	@echo "make nettestall            -- run full test against all schematics"
	@echo "make testall               -- run all project tests"
	@echo "make doc                   -- generate documentation"
	@echo "make renum                 -- name all unset refdes (U?)"
	@echo "make renumall              -- overwrite all refdes"
	@echo "make versions              -- print versions of required programs"
	@echo "make decode                -- run decode searcher"
	@echo "make asm=foo tim           -- full tim integration run against foo.o"

netlist:	$(BUILD_DIR) $(BUILD_DIR)/$(target).v
testbench:	$(BUILD_DIR) $(BUILD_DIR)/tb_$(target).v
nettest:	$(BUILD_DIR) $(WF_DIR) $(WF_DIR)/$(target).vcd
nettestall:	$(BUILD_DIR) $(WF_DIR) $(ALL_SCHEM_TESTS)
testall:	$(BUILD_DIR) $(WF_DIR) $(ALL_TESTS)
doc:		$(DOC_DIR) $(DOC_DIR)/block_diagram.png $(DOC_DIR)/schematics.pdf

renum:
	@python $(BIN_DIR)/refdes_renum.py $(ALL_SCHEMS)

renumall:
	@python $(BIN_DIR)/refdes_renum.py --overwrite $(ALL_SCHEMS)

versions:
	@echo "gnetlist `$(GNETLIST) --version | head -n1 | cut -f2 -d' '`"
	@echo "iverilog `$(IVERILOG) -V 2>&1 | head -n1 | cut -f4 -d' '`"
	@echo "gaf      `$(GAF) --version | head -n1 | cut -f2 -d' '`"
	@echo "gschem   `$(GSCHEM) --version | head -n1 | cut -f2 -d' '`"
	@echo "gtkwave  `$(GTKWAVE) --version | head -n1 | cut -f3 -d' '`"

clean:
	@rm -rf -- $(BUILD_DIR)/* Makefile.deps

wave: $(BUILD_DIR) $(WF_DIR) $(WF_DIR)/$(target).vcd
	@$(GTKWAVE) $(WF_DIR)/$(target).vcd $(CONFIG_DIR)/gtkwave/$(target).sav

decode:
	@python bin/decode_search.py

$(BUILD_DIR):
	@mkdir $(BUILD_DIR)

$(WF_DIR):
	@mkdir $(WF_DIR)

$(DOC_DIR):
	@mkdir $(DOC_DIR)

$(DOC_DIR)/%.png: $(DESIGN_DIR)/%.sch
	@echo "PNG     : $(@F)"
	@$(GAF) export --size=auto --color --output=$@ $^ 2>&1 | grep -v "^\*\* Message:" | sed '/^$$/d'

$(DOC_DIR)/schematics.pdf: $(DOC_SCHEMS)
	@echo "PDF     : $(@F)"
	@$(GAF) export --color --output=$@ $^ 2>&1 | grep -v "^\*\* Message:" | sed '/^$$/d'


# ##############################################################################
# SCHEMATICS SPECIAL
# ##############################################################################

$(BUILD_DIR)/tb_tim.v: $(VERILOG_DIR)/tb_tim.v
	@echo "Copy    : $(@F)"
	@cp $^ $@

$(BUILD_DIR)/decode-test-cases.json: $(CONFIG_DIR)/decode.csv $(BUILD_DIR)/decode.log
	@echo "Gen Test: $(@F)"
	@python $(BIN_DIR)/gen_decode_test_json.py $^ > $@

$(BUILD_DIR)/decode_decode.v: $(BUILD_DIR)/decode.log
	@echo "Gen Veri: $(@F)"
	@python $(BIN_DIR)/gen_decode_verilog.py $^ > $@

$(BUILD_DIR)/decode.log: $(CONFIG_DIR)/decode.csv
	@echo "Decode  : $(@F)"
	@python bin/decode_search.py --quiet --max-iterations 1

$(BUILD_DIR)/tim.bin: $(BUILD_DIR)/$(asm).o
	@echo "Gen Bin : $(asm).o"
	@python bin/to_verilog_dump.py $^ > $@

tim: $(BUILD_DIR) $(WF_DIR) $(BUILD_DIR)/test_tim $(BUILD_DIR)/tim.bin
	@echo "Run TIM :"
	@$(BUILD_DIR)/test_tim


# ##############################################################################
# SCHEMATICS
# ##############################################################################

$(BUILD_DIR)/%.sch: $(SCHEM_DIR)/%.sch
	@echo "Fix Sch : $(@F)"
	@python $(BIN_DIR)/fix_schematic.py $< $@

$(BUILD_DIR)/74%.v: $(BIN_DIR)/gen_gate.py $(CONFIG_DIR)/74-series-chips.json
	@echo "Gen Gate: $(@F)"
	@python $(BIN_DIR)/gen_gate.py $(basename $(@F)) > $@

$(BUILD_DIR)/%.v: $(VERILOG_DIR)/%.v
	@echo "Copy    : $(@F)"
	@cp $^ $@

$(BUILD_DIR)/%.v: $(wildcard $(BUILD_DIR)/%.sch)
	@echo "Netlist : $(@F) ($(^F))"
	@$(GNETLIST) -g verilog $^ -o $@ 2>&1 | grep -v "^Loading schematic" | \
		grep -v "is not likely a valid Verilog identifier" | $(FAILON) '.*'
	@grep unconnected_pin $@ | cut -f2 -d' ' | $(FAILON) '.*'
	@echo "Fix Net : $(@F)"
	@python $(BIN_DIR)/fix_netlist.py $@ $^

$(BUILD_DIR)/tb_%.v: $(BUILD_DIR)/%.v $(CONFIG_DIR)/test-cases.json
	@echo "Build TB: $(@F)"
	@python $(BIN_DIR)/gen_test_bench.py $< > $@

$(BUILD_DIR)/test_%: $(BUILD_DIR)/%.v $(BUILD_DIR)/tb_%.v $(BUILD_DIR)/clock.v
	@echo "Cmpl TB : $(@F)"
	@$(IVERILOG) $^ -o $@ 2>&1 | $(FAILON) "error\|\(was already declared here\)"

$(WF_DIR)/%.vcd: $(BUILD_DIR)/test_%
	@echo "Run TB  : $(@F)"
	@$< 2>&1 | grep -v "^VCD info" | tee $(WF_DIR)/$(@F).log | $(FAILON) "FAILURE"


# ##############################################################################
# ASSEMBLER TESTS
# ##############################################################################

$(BUILD_DIR)/%.o: $(ASM_DIR)/%.asm
	@echo "Asm     : $(*F)"
	@$(ASM) $^ $@

$(BUILD_DIR)/%.o.chk: $(ASM_DIR)/%.asm $(BUILD_DIR)/%.o
	@echo "Test Bin: $(@F)"
	@cat $< | egrep -o '; [ 01]* \|' | tr -d ' ;|' > $@.good
	@xxd -b -c 1 $(BUILD_DIR)/$*.o | cut -f2 -d' ' | sed 'N;s/\n//' > $@.check
	@diff -y $@.good $@.check | tr '\t' ' ' | grep -n ' | ' | sed 's/  */ /'
	@diff -q $@.good $@.check > /dev/null
	@touch $@

$(BUILD_DIR)/%.o.test: $(ASM_DIR)/%.asm $(BUILD_DIR)/%.o
	@echo "Test Asm: $(*F)"
	@$(SIM_TEST) $^
	@touch $@


# ##############################################################################
# STATIC DEPENDENCIES
# ##############################################################################

$(WF_DIR)/tim.vcd: $(BUILD_DIR)/tim.bin
$(BUILD_DIR)/tb_decode_decode.v: $(BUILD_DIR)/decode-test-cases.json
$(BUILD_DIR)/test_decode_decode: $(BUILD_DIR)/7408.v $(BUILD_DIR)/7474.v
