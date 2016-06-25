
BUILD		= build
SCHEM		= schem
DOC			= ../doc
WF			= $(BUILD)/waveforms
FAILON		= ./failon.sh
GNETLIST	= /usr/bin/gnetlist

ALL_SCHEMS = $(SCHEM)/*.sch
SCHEMS = $(filter-out $(wildcard $(SCHEM)/_*.sch),$(wildcard $(ALL_SCHEMS)))
DOC_SCHEMS = $(sort $(subst $(SCHEM),$(BUILD),$(SCHEMS)))


.PHONY: clean help netlist testbench test testall protopcb doc wave
.PRECIOUS: $(BUILD)/%.v $(BUILD)/tb_%.v $(BUILD)/%.sch $(BUILD)/test_% $(WF)/%.vcd


help:
	@echo "make target=foo test       -- run full netlist and testbench for foo"
	@echo "make target=foo netlist    -- generate netlist for foo"
	@echo "make target=foo testbench  -- generate testbench for foo"
	@echo "make testall               -- run full test against all schematics"
	@echo "make doc                   -- generate documentation"


# generate dependencies
Makefile.deps: $(ALL_SCHEMS) makedeps.py
	@python makedeps.py $(ALL_SCHEMS) > $@
-include Makefile.deps


$(BUILD):
	@mkdir $(BUILD)


$(WF):
	@mkdir $(WF)


$(BUILD)/%.sch: $(SCHEM)/%.sch
	@echo "Fix Sch : $(@F)"
	@python fix_schematic.py $< $@


$(BUILD)/74%.v: gengate.py 74HCxxx.json
	@echo "Gen Gate: $(@F)"
	@python gengate.py $(basename $(@F)) > $@


$(BUILD)/tb_%.v: $(BUILD)/%.v tests.json
	@echo "Build TB: $(@F)"
	@python testmod.py $< > $@


$(BUILD)/%.v: $(wildcard $(BUILD)/%.sch)
	@echo "Netlist : $(@F) ($(^F))"
	@$(GNETLIST) -g verilog $^ -o $@ 2>&1 | grep -v "^Loading schematic" | grep -v "is not likely a valid Verilog identifier" | $(FAILON) '.*'
	@grep unconnected_pin $@ | cut -f2 -d' ' | $(FAILON) '.*'
	@echo "Fix Net : $(@F)"
	@python fix_netlist.py $@ $^


$(BUILD)/test_%: $(BUILD)/%.v $(BUILD)/tb_%.v $(BUILD)/clock.v
	@echo "Cmpl TB : $(@F)"
	@iverilog $^ -o $@ 2>&1 | $(FAILON) "error\|\(was already declared here\)"


$(WF)/%.vcd: $(BUILD)/test_%
	@echo "Run TB  : $(@F)"
	@$< 2>&1 | grep -v "^VCD info" | tee $(WF)/$(@F).log | $(FAILON) "FAILURE"


$(DOC)/%.png: %.sch
	@echo "PNG     : $(@F)"
	@gaf export --size=auto --color --output=$@ $^ 2>&1 | grep -v "^\*\* Message:" | sed '/^$$/d'


$(DOC)/schematics.pdf: $(DOC_SCHEMS)
	@echo "PDF     : $(@F)"
	@gaf export --color --output=$@ $^ 2>&1 | grep -v "^\*\* Message:" | sed '/^$$/d'


wave: $(BUILD) $(WF) $(WF)/$(TARGET).vcd
	@gtkwave $(WF)/$(TARGET).vcd


netlist:	$(BUILD) $(BUILD)/$(target).v
testbench:	$(BUILD) $(BUILD)/tb_$(target).v
test: 		$(BUILD) $(WF) $(WF)/$(target).vcd
testall:	$(BUILD) $(WF) $(ALL_TESTS)
doc:		$(DOC)/block_diagram.png $(DOC)/schematics.pdf

clean:
	@rm -rf -- $(BUILD)/* Makefile.deps $(DOC)/block_diagram.png $(DOC)/schematics.pdf
