
BUILD=build
SCHEM=schem

FAILON = ./failon.sh

SCHEMS=$(SCHEM)/*.sch
SYMBOLS=symbols/**/*.v


.PHONY: test clean

test:
	echo $(SCHEMS)

$(BUILD):
	mkdir $(BUILD)

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

wf_%.vcd: $(BUILD)/test_%
	$< 2>&1 | grep -v "^VCD info" | $(FAILON) "FAILURE"

go: wf_execute_barrel_shifter.vcd

clean:
	rm -rf $(BUILD)
