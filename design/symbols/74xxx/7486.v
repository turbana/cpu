/* 7486 Quad 2-bit XOR
 * worse case delay of 30ns
 */
`timescale 1 ns / 100 ps
module \74157 (\1 , \2 , \3 , \4 , \5 , \6 , \7 , \8 , \9 , \10 , \11 , \12 , \13 , \14 , \15 , \16 );
   input \1 , \2 , \3 , \4 , \5 , \6 , \7 , \8 , \9 , \10 , \11 , \12 , \13 , \14 ;
   output \3 , \6 , \8 , \11 ;

   assign #30 =  \3 = \1 ^ \2 ;
   assign #30 =  \6 = \4 ^ \5 ;
   assign #30 =  \8 = \9 ^ \10 ;
   assign #30 = \11 = \12 ^ \13 ;

endmodule
