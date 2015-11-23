/* 74157 Quad 2x1 Mux
 * worse case delay of 27ns
 */
`timescale 1 ns / 100 ps
module \74157 (\1 , \2 , \3 , \4 , \5 , \6 , \7 , \8 , \9 , \10 , \11 , \12 , \13 , \14 , \15 , \16 );
   input \1 , \2 , \3 , \5 , \6 , \8 , \10 , \11 , \13 , \14 , \15 , \16 ;
   output \4 , \7 , \9 , \12 ;

   assign #27  \4 = \15 ? 0 : \1 ?  \3 :  \2 ;
   assign #27  \7 = \15 ? 0 : \1 ?  \6 :  \5 ;
   assign #27  \9 = \15 ? 0 : \1 ? \10 : \11 ;
   assign #27 \12 = \15 ? 0 : \1 ? \13 : \14 ;

endmodule