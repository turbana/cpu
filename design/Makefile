
BUILD		= build
BIN         = bin
CONFIG      = config
SCHEM		= schem
DOC			= ../doc
VERILOG     = verilog
ASM_BUILD   = ../tests/build
WF			= $(BUILD)/waveforms
FAILON		= $(BIN)/failon.sh
GNETLIST    = gnetlist
GAF			= gaf
IVERILOG	= iverilog
GTKWAVE		= gtkwave
GSCHEM		= gschem

ALL_SCHEMS = $(SCHEM)/*.sch
SCHEMS = $(filter-out $(wildcard $(SCHEM)/_*.sch),$(wildcard $(ALL_SCHEMS)))
DOC_SCHEMS = $(sort $(subst $(SCHEM),$(BUILD),$(SCHEMS)))
ALL_VERILOG = $(subst .sch,.v,$(DOC_SCHEMS))


.PHONY: clean help netlist testbench test testall protopcb doc wave renum renumall versions decode
.PRECIOUS: $(BUILD)/%.v $(BUILD)/tb_%.v $(BUILD)/%.sch $(BUILD)/test_% $(WF)/%.vcd


help:
	@echo "make target=foo test       -- run full netlist and testbench for foo"
	@echo "make target=foo netlist    -- generate netlist for foo"
	@echo "make target=foo testbench  -- generate testbench for foo"
	@echo "make testall               -- run full test against all schematics"
	@echo "make doc                   -- generate documentation"
	@echo "make renum                 -- name all unset refdes (U?)"
	@echo "make renumall              -- overwrite all refdes"
	@echo "make versions              -- print versions of required programs"
	@echo "make decode                -- run decode searcher"


# generate dependencies
Makefile.deps: $(ALL_SCHEMS) $(BIN)/make_dependencies.py
	@python $(BIN)/make_dependencies.py $(VERILOG)/*.v $(ALL_SCHEMS) > $@
-include Makefile.deps


$(BUILD):
	@mkdir $(BUILD)


$(WF):
	@mkdir $(WF)


$(DOC):
	@mkdir $(DOC)


$(BUILD)/tb_tim.v: $(VERILOG)/tb_tim.v
	@echo "Copy    : $(@F)"
	@cp $^ $@


$(BUILD)/%.v: $(VERILOG)/%.v
	@echo "Copy    : $(@F)"
	@cp $^ $@


$(BUILD)/%.sch: $(SCHEM)/%.sch
	@echo "Fix Sch : $(@F)"
	@python $(BIN)/fix_schematic.py $< $@


$(BUILD)/74%.v: $(BIN)/gen_gate.py $(CONFIG)/74-series-chips.json
	@echo "Gen Gate: $(@F)"
	@python $(BIN)/gen_gate.py $(basename $(@F)) > $@


$(BUILD)/decode-test-cases.json: $(CONFIG)/decode.csv $(BUILD)/decode.log
	@echo "Gen Test: $(@F)"
	@python $(BIN)/gen_decode_test_json.py $^ > $@


$(BUILD)/decode_decode.v: $(BUILD)/decode.log
	@echo "Gen Veri: $(@F)"
	@python $(BIN)/gen_decode_verilog.py $^ > $@


$(BUILD)/tb_%.v: $(BUILD)/%.v $(CONFIG)/test-cases.json
	@echo "Build TB: $(@F)"
	@python $(BIN)/gen_test_bench.py $< > $@


$(BUILD)/%.v: $(wildcard $(BUILD)/%.sch)
	@echo "Netlist : $(@F) ($(^F))"
	@$(GNETLIST) -g verilog $^ -o $@ 2>&1 | grep -v "^Loading schematic" | grep -v "is not likely a valid Verilog identifier" | $(FAILON) '.*'
	@grep unconnected_pin $@ | cut -f2 -d' ' | $(FAILON) '.*'
	@echo "Fix Net : $(@F)"
	@python $(BIN)/fix_netlist.py $@ $^


$(BUILD)/test_%: $(BUILD)/%.v $(BUILD)/tb_%.v $(BUILD)/clock.v
	@echo "Cmpl TB : $(@F)"
	@$(IVERILOG) $^ -o $@ 2>&1 | $(FAILON) "error\|\(was already declared here\)"


$(WF)/%.vcd: $(BUILD)/test_%
	@echo "Run TB  : $(@F)"
	@$< 2>&1 | grep -v "^VCD info" | tee $(WF)/$(@F).log | $(FAILON) "FAILURE"


$(DOC)/%.png: %.sch
	@echo "PNG     : $(@F)"
	@$(GAF) export --size=auto --color --output=$@ $^ 2>&1 | grep -v "^\*\* Message:" | sed '/^$$/d'


$(DOC)/schematics.pdf: $(DOC_SCHEMS)
	@echo "PDF     : $(@F)"
	@$(GAF) export --color --output=$@ $^ 2>&1 | grep -v "^\*\* Message:" | sed '/^$$/d'


wave: $(BUILD) $(WF) $(WF)/$(target).vcd
	@$(GTKWAVE) $(WF)/$(target).vcd


decode:
	@python bin/decode_search.py > /dev/null


$(BUILD)/%.bin: $(ASM_BUILD)/%.o
	@echo "Gen Bin : $(@F)"
	@python bin/to_verilog_dump.py $^ > $@


tim: $(BUILD) $(WF) $(BUILD)/test_tim $(BUILD)/$(target).bin
	@echo "Run TIM :"
	@cp $(BUILD)/$(target).bin $(BUILD)/tim.bin
	@$(BUILD)/test_tim


netlist:	$(BUILD) $(BUILD)/$(target).v
testbench:	$(BUILD) $(BUILD)/tb_$(target).v
test: 		$(BUILD) $(WF) $(WF)/$(target).vcd
testall:	$(BUILD) $(WF) $(ALL_TESTS)
doc:		$(DOC) $(DOC)/block_diagram.png $(DOC)/schematics.pdf

renum:
	@python $(BIN)/refdes_renum.py $(ALL_SCHEMS)

renumall:
	@python $(BIN)/refdes_renum.py --overwrite $(ALL_SCHEMS)

versions:
	@echo "gnetlist `$(GNETLIST) --version | head -n1 | cut -f2 -d' '`"
	@echo "iverilog `$(IVERILOG) -V 2>&1 | head -n1 | cut -f4 -d' '`"
	@echo "gaf      `$(GAF) --version | head -n1 | cut -f2 -d' '`"
	@echo "gschem   `$(GSCHEM) --version | head -n1 | cut -f2 -d' '`"
	@echo "gtkwave  `$(GTKWAVE) --version | head -n1 | cut -f3 -d' '`"

clean:
	@rm -rf -- $(BUILD)/* Makefile.deps
#$(DOC)/block_diagram.png $(DOC)/schematics.pdf
