/* module for TC1232 CPU watchdog */
`timescale 1 ns / 100 ps
module TC1232 ( \1 , \2 , \3 , \4 , \5 , \6 , \7 , \8 ) ;
  input \1 , \2 , \3 , \4 , \7 , \8 ;
  output \5 , \6 ;
  reg reset ;

  assign \5 = reset ;
  assign \6 = ~reset ;

  initial
  begin
    reset = 1'b1 ;
    #1000
    reset = 1'b0 ;
  end
endmodule
