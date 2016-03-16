
BUILD=build
SCHEM=schem
SYMBOLS=symbols

SCHEMS=$(SCHEM)/*.sch

.PHONY: test clean

test:
	echo $(SCHEMS)

$(BUILD):
	mkdir $(BUILD)

$(BUILD)/%.sch: $(SCHEM)/%.sch $(BUILD)
	python fix_schematic.py $< $@

$(BUILD)/%.v: $(BUILD)/%.sch
	gnetlist -g verilog $< -o $@

clean:
	rm -rf $(BUILD)
