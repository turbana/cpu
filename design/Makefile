
BUILD=build
SCHEM=schem
WF=waveforms

FAILON = ./failon.sh

SCHEMS=$(SCHEM)/*.sch
SYMBOLS=symbols/**/*.v


.PHONY: clean run
.PRECIOUS: $(BUILD)/%.v $(BUILD)/tb_%.v $(BUILD)/%.sch $(BUILD)/test_%

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
	@iverilog $^ $(SYMBOLS) -o $@ 2>&1 | $(FAILON) "error\|(was already declared here)"

$(WF)/%.vcd: $(BUILD)/test_%
	@echo "Run TB  : $(@F)"
	@$< 2>&1 | grep -v "^VCD info" | tee $(WF)/$(@F).log | $(FAILON) "FAILURE"

run: $(BUILD) $(WF) $(WF)/$(TARGET).vcd

clean:
	@rm -rf $(BUILD) $(WF)
