
`timescale 1 ns / 100 ps

module tb_devices;
   reg         BUS_W;
   reg         BUS_R;
   reg  [22:0] BUS_A;
   wire [15:0] BUS_D;
   reg  [15:0] _BUS_D;
   reg         _BUS_D_en;

   devices DUT (
                .BUS_D (BUS_D),
                .BUS_A (BUS_A),
                .BUS_R (BUS_R),
                .BUS_W (BUS_W)
                );

   assign BUS_D = (_BUS_D_en) ? _BUS_D : 16'bZ;

   task read;
      input [22:0] addr;
      begin
         _BUS_D_en = 0;
         BUS_W = 0;
         BUS_R = 1;
         BUS_A = addr;
         #50 BUS_R = 0;
         #50 BUS_R = 0;
      end
   endtask

   task write;
      input [22:0] addr;
      input [15:0] data;
      begin
         BUS_R = 0;
         BUS_A = addr;
         _BUS_D = data;
         _BUS_D_en = 1;
         BUS_W = 1;
         #50 BUS_W = 0;
         #50 BUS_W = 0;
      end
   endtask

   initial
     begin
        $dumpfile("tb_devices.vcd");
        $dumpvars;
        $readmemh("data.bin", DUT.mem);
        _BUS_D_en = 0;

        read(23'h000000);
        read(23'h000001);
        read(23'h000002);
        read(23'h000003);

        write(23'h000000, 16'h4321);
        write(23'h000001, 16'hDCBA);
        write(23'h000002, 16'h9876);

        read(23'h000000);
        read(23'h000001);
        read(23'h000002);
        read(23'h000003);
        read(23'h000004);
        read(23'h000005);

        $finish;
     end
endmodule
