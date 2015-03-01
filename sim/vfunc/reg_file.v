

module reg_file (
	clk0,
	a,
	a_read,
	a_data,
	b,
	b_read,
	b_data
);


input         clk0;
input   [2:0] a;
input         a_read;
input   [2:0] b;
input         b_read;

inout  [15:0] a_data;
inout  [15:0] b_data;


wire          clk0;
wire    [2:0] a;
wire   [15:0] a_data;
wire    [2:0] b;
wire   [15:0] b_data;


reg    [15:0] registers [0:7];


assign a_data = (!a_read) ? 16'bZ : (a) ? registers[a] : 16'b0;
assign b_data = (!b_read) ? 16'bZ : (b) ? registers[b] : 16'b0;


always @ (posedge clk0)
begin
	if (!a_read) begin
		registers[a] <= a_data;
	end

	if (!b_read) begin
		registers[b] <= b_data;
	end
end

endmodule
