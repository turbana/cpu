`timescale 1 ns / 100 ps

module devices (BUS_A, BUS_D, BUS_R, BUS_W);

   inout [15:0] BUS_D ;
   input [22:0] BUS_A ;
   input        BUS_R ;
   input        BUS_W ;

   reg   [15:0] mem [0:1<<23];

   assign BUS_D = (BUS_R & !BUS_W) ? mem[BUS_A] : 16'bZ;

   always @(BUS_W)
	  #100
      if (BUS_W)
        mem[BUS_A] = BUS_D;

endmodule
