`timescale 1 ns / 100 ps

module tb_tim;

   reg _CLK;

   tim TIM (
      ._CLK (_CLK)
   );

   always #125 _CLK = ~_CLK;

   initial
     begin
        $dumpfile("build/waveforms/tim.vcd");
        $dumpvars;
        // load "bootloader" into ROM
        // 0x5800 = jmp $0($0)
        TIM.DEVICES.mem[23'h40E000] = 16'h5800;
        TIM.DEVICES.mem[23'h40E001] = 16'h5800;
        $readmemh("build/tim.bin", TIM.DEVICES.mem);
        _CLK = 0;

        #1000000 $finish;
     end
endmodule
