
module tb_reg_file;
reg clk0, a_read, b_read;
reg [2:0] a, b;
wire [15:0] a_data, b_data;
reg [15:0] a_data_reg, b_data_reg;

reg_file U0 (
	.clk0	(clk0),
	.a		(a),
	.a_read(a_read),
	.a_data	(a_data),
	.b		(b),
	.b_read(b_read),
	.b_data	(b_data)
);


assign a_data = a_data_reg;
assign b_data = b_data_reg;


always
	#1 clk0 = ~clk0;

initial
begin
	clk0 = 1;
	$dumpfile("wf_reg_file.vcd");
	$dumpvars;
	$display("\t\ttime\tclk0\ta\ta_read\ta_data\tb\tb_read\tb_data");
	$monitor("%d\t%b\t%d\t%b\t%2X\t%d\t%b\t%2X",
		$time, clk0, a, a_read, a_data, b, b_read, b_data);

	// @0 $0=ABCD; $1=1234
	a = 3'b000;
	a_read = 1'b0;
	a_data_reg = 16'hABCD;
	b = 3'b001;
	b_read = 1'b0;
	b_data_reg = 16'h1234;

	// @2 read $1; read $0
	#2
	a = 3'b001;
	a_read = 1'b1;
	a_data_reg = 16'bZ;
	b = 3'b000;
	b_read = 1'b1;
	b_data_reg = 16'bZ;
end

initial
	#10 $finish;

endmodule
