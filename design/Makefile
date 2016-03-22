
BUILD=build
SCHEM=schem
WF=waveforms

FAILON = ./failon.sh

SCHEMS=$(SCHEM)/*.sch
SYMBOLS=symbols/**/*.v


# multi page schematics
$(BUILD)/execute_alu.v: $(BUILD)/execute_alu.sch $(BUILD)/execute_barrel_shifter.sch


# build commands
FIX_SCH = @echo "Fix Sch : $(@F)"; \
	python fix_schematic.py $< $@

NETLIST = @echo "Netlist : $(@F) ($(^F))"; \
	$(GEN_NETLIST); \
	$(CHK_NETLIST); \
	echo "Fix Net : $(@F)"; \
	$(FIX_NETLIST)
GEN_NETLIST = gnetlist -g verilog $^ -o $@ 2>&1 | \
	grep -v "^Loading schematic" | \
	grep -v "is not likely a valid Verilog identifier" | \
	$(FAILON) '.*'
CHK_NETLIST = grep unconnected_pin $@ | cut -f2 -d' ' | $(FAILON) '.*'
FIX_NETLIST = python fixnetlist.py $@ $<

GEN_TB = @echo "Build TB: $(@F)"; \
	python testmod.py $< > $@
CMP_TB = @echo "Cmpl TB : $(@F)"; \
	iverilog $^ $(SYMBOLS) -o $@ 2>&1 | $(FAILON) "error\|\(was already declared here\)"
EXE_TB = @echo "Run TB  : $(@F)"; \
	$< 2>&1 | grep -v "^VCD info" | tee $(WF)/$(@F).log | $(FAILON) "FAILURE"


# build rules
.PHONY: clean help netlist testbench test testall
.PRECIOUS: $(BUILD)/%.v $(BUILD)/tb_%.v $(BUILD)/%.sch $(BUILD)/test_%

help:
	@echo "make TARGET=foo test       -- run full netlist and testbench for foo"
	@echo "make TARGET=foo netlist    -- generate netlist for foo"
	@echo "make TARGET=foo testbench  -- generate testbench for foo"
	@echo "make testall               -- run full test against all schematics"

$(BUILD):
	@mkdir $(BUILD)

$(WF):
	@mkdir $(WF)

$(BUILD)/%.sch: $(SCHEM)/%.sch
	$(FIX_SCH)

$(BUILD)/%.v: $(BUILD)/%.sch
	$(NETLIST)

$(BUILD)/tb_%.v: $(BUILD)/%.v tests.json
	$(GEN_TB)

$(BUILD)/test_%: $(BUILD)/tb_%.v $(BUILD)/%.v
	$(CMP_TB)

$(WF)/%.vcd: $(BUILD)/test_%
	$(EXE_TB)

netlist:	$(BUILD) $(BUILD)/$(TARGET).v
testbench:	$(BUILD) $(BUILD)/tb_$(TARGET).v
test: 		$(BUILD) $(WF) $(WF)/$(TARGET).vcd
testall:	$(BUILD) $(WF) $(subst .sch,.vcd,$(subst $(SCHEM),$(WF),$(shell echo $(SCHEMS))))

clean:
	@rm -rf $(BUILD) $(WF)
