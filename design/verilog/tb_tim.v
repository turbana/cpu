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
        $readmemh("build/tim.bin", TIM.DEVICES.mem);
        _CLK = 0;

        #1000000 $finish;
     end
endmodule
