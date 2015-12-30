/* 7432 Quad 2-bit OR
 * worse case delay of 10ns
 */
`timescale 1 ns / 100 ps
module \7432 (\1 , \2 , \3 , \4 , \5 , \6 , \7 , \8 , \9 , \10 , \11 , \12 , \13 , \14 );
   input \1 , \2 , \4 , \5 , \7 , \9 , \10 , \12 , \13 , \14 ;
   output \3 , \6 , \8 , \11 ;

   assign #10  \3 = \1 | \2 ;
   assign #10  \6 = \4 | \5 ;
   assign #10  \8 = \9 | \10 ;
   assign #10 \11 = \12 | \13 ;

endmodule
