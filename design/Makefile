
BUILD=build
SCHEM=schem
WF=waveforms

FAILON = ./failon.sh

SCHEMS=$(SCHEM)/*.sch
SYMBOLS=symbols/**/*.v


.PHONY: test clean
.PRECIOUS: $(BUILD)/%.v $(BUILD)/tb_%.v $(BUILD)/%.sch $(BUILD)/test_%

test:
	echo $(SCHEMS)

$(BUILD):
	mkdir $(BUILD)

$(WF):
	mkdir $(WF)

$(BUILD)/%.sch: $(SCHEM)/%.sch $(BUILD)
	python fix_schematic.py $< $@

$(BUILD)/%.v: $(BUILD)/%.sch
	gnetlist -g verilog $< -o $@ 2>&1 | \
		grep -v "^Loading schematic" | \
		grep -v "is not likely a valid Verilog identifier" | \
		$(FAILON) '.*'
	grep unconnected_pin $@ | cut -f2 -d' '
	python fixnetlist.py $@ $<

$(BUILD)/tb_%.v: $(BUILD)/%.v
	python testmod.py $< > $@

$(BUILD)/test_%: $(BUILD)/tb_%.v $(BUILD)/%.v
	iverilog $^ $(SYMBOLS) -o $@ 2>&1 | $(FAILON) "error\|(was already declared here)"

%.vcd: $(BUILD)/test_% $(WF)
	$< 2>&1 | grep -v "^VCD info" | $(FAILON) "FAILURE"

go: execute_barrel_shifter.vcd

clean:
	rm -rf $(BUILD)
