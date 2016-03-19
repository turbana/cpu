
BUILD=build
SCHEM=schem
WF=waveforms

FAILON = ./failon.sh

SCHEMS=$(SCHEM)/*.sch
SYMBOLS=symbols/**/*.v


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
	@echo "Fix Sch : $(@F)"
	@python fix_schematic.py $< $@

$(BUILD)/%.v: $(BUILD)/%.sch
	@echo "Netlist : $(@F)"
	@gnetlist -g verilog $< -o $@ 2>&1 | \
		grep -v "^Loading schematic" | \
		grep -v "is not likely a valid Verilog identifier" | \
		$(FAILON) '.*'
	@grep unconnected_pin $@ | cut -f2 -d' '
	@echo "Fix Netl: $(@F)"
	@python fixnetlist.py $@ $<

$(BUILD)/tb_%.v: $(BUILD)/%.v
	@echo "Build TB: $(@F)"
	@python testmod.py $< > $@

$(BUILD)/test_%: $(BUILD)/tb_%.v $(BUILD)/%.v
	@echo "Cmpl TB : $(@F)"
	@iverilog $^ $(SYMBOLS) -o $@ 2>&1 | $(FAILON) "error\|\(was already declared here\)"

$(WF)/%.vcd: $(BUILD)/test_%
	@echo "Run TB  : $(@F)"
	@$< 2>&1 | grep -v "^VCD info" | tee $(WF)/$(@F).log | $(FAILON) "FAILURE"

netlist: $(BUILD) $(BUILD)/$(TARGET).v
testbench: $(BUILD) $(BUILD)/tb_$(TARGET).v
test: $(BUILD) $(WF) $(WF)/$(TARGET).vcd
testall: $(BUILD) $(WF) $(subst .sch,.vcd,$(subst $(SCHEM),$(WF),$(shell echo $(SCHEMS))))

clean:
	@rm -rf $(BUILD) $(WF)
