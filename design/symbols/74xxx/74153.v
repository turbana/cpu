/* 74153 Dual 4x1 Mux
 * worse case delay of 34ns
 * NOTE: does not currently account for chip select
 */
`timescale 1 ns / 100 ps
module \74153 (\1 , \2 , \3 , \4 , \5 , \6 , \7 , \8 , \9 , \10 , \11 , \12 , \13 , \14 , \15 , \16 );
   input \1 , \2 , \3 , \4 , \5 , \6 , \8 , \10 , \11 , \12 , \13 , \14 , \15 , \16 ;
   output \7 , \9 ;

   assign #34 \7 = \2 ? ( \14 ?  \3 :  \4 ) : ( \14 ?  \5 :  \6 ) ;
   assign #34 \9 = \2 ? ( \14 ? \13 : \12 ) : ( \14 ? \11 : \10 ) ;

endmodule
