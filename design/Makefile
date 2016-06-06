
BUILD=build
SCHEM=schem
DOC=../doc
WF=waveforms

SCHEMS = $(SCHEM)/*.sch
FAILON = ./failon.sh
GNETLIST = /usr/bin/gnetlist


# generate dependencies
Makefile.deps: $(SCHEMS) makedeps.py
	@python makedeps.py $(SCHEMS) > $@
-include Makefile.deps


# build commands
FIX_SCH = @echo "Fix Sch : $(@F)"; \
	python fix_schematic.py $< $@

NETLIST = @echo "Netlist : $(@F) ($(^F))"; \
	$(GEN_NETLIST); \
	$(CHK_NETLIST); \
	echo "Fix Net : $(@F)"; \
	$(FIX_NETLIST)
GEN_NETLIST = $(GNETLIST) -g verilog $^ -o $@ 2>&1 | \
	grep -v "^Loading schematic" | \
	grep -v "is not likely a valid Verilog identifier" | \
	$(FAILON) '.*'
CHK_NETLIST = grep unconnected_pin $@ | cut -f2 -d' ' | $(FAILON) '.*'
FIX_NETLIST = python fix_netlist.py $@ $^

GEN_TB = @echo "Build TB: $(@F)"; \
	python testmod.py $< > $@
CMP_TB = @echo "Cmpl TB : $(@F)"; \
	iverilog $^ -o $@ 2>&1 | $(FAILON) "error\|\(was already declared here\)"
EXE_TB = @echo "Run TB  : $(@F)"; \
	$< 2>&1 | grep -v "^VCD info" | tee $(WF)/$(@F).log | $(FAILON) "FAILURE"
GAF_PNG = @gaf export --size=auto --color --output=$@ $^ 2>&1 | grep -v "^\*\* Message:"
GEN_GATE = @echo "Gen Gate: $(@F)"; \
	python gengate.py $(basename $(@F)) > $@


# build rules
.PHONY: clean help netlist testbench test testall protopcb doc
.PRECIOUS: $(BUILD)/%.v $(BUILD)/tb_%.v $(BUILD)/%.sch $(BUILD)/test_%

help:
	@echo "make TARGET=foo test       -- run full netlist and testbench for foo"
	@echo "make TARGET=foo netlist    -- generate netlist for foo"
	@echo "make TARGET=foo testbench  -- generate testbench for foo"
	@echo "make testall               -- run full test against all schematics"
	@echo "make doc                   -- generate documentation"

$(BUILD):
	@mkdir $(BUILD)

$(WF):
	@mkdir $(WF)

$(BUILD)/%.sch: $(SCHEM)/%.sch
	$(FIX_SCH)

$(BUILD)/74%.v: gengate.py 74HCxxx.json
	$(GEN_GATE)

$(BUILD)/tb_%.v: $(BUILD)/%.v tests.json
	$(GEN_TB)

$(BUILD)/%.v: $(wildcard $(BUILD)/%.sch)
	$(NETLIST)

$(BUILD)/test_%: $(BUILD)/%.v $(BUILD)/tb_%.v
	$(CMP_TB)

$(WF)/%.vcd: $(BUILD)/test_%
	$(EXE_TB)

$(DOC)/%.png: %.sch
	$(GAF_PNG)

protopcb: project
	gsch2pcb project
	pcb proto.pcb

netlist:	$(BUILD) $(BUILD)/$(TARGET).v
testbench:	$(BUILD) $(BUILD)/tb_$(TARGET).v
test: 		$(BUILD) $(WF) $(WF)/$(TARGET).vcd
testall:	$(BUILD) $(WF) $(ALL_TESTS)
doc:		$(DOC)/block_diagram.png

clean:
	@rm -rf -- $(BUILD)/* $(WF)/* proto.cmd proto.net proto.pcb- Makefile.deps
