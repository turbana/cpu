v 20110115 2
C 40000 40000 0 0 0 title-bordered-A2.sym
C 51100 49400 1 0 0 74157-2.sym
{
T 51200 52140 5 10 0 0 0 0 1
device=74157
T 51200 51940 5 10 0 0 0 0 1
footprint=SO16
T 51700 51300 5 16 1 1 0 0 1
refdes=U0
T 51200 51740 5 10 0 0 0 0 1
value=SN74HC157D
}
C 51100 45000 1 0 0 74157-2.sym
{
T 51200 47740 5 10 0 0 0 0 1
device=74157
T 51200 47540 5 10 0 0 0 0 1
footprint=SO16
T 51700 46900 5 16 1 1 0 0 1
refdes=U3
T 51200 47340 5 10 0 0 0 0 1
value=SN74HC157D
}
C 48100 51800 1 0 0 ipad-2.sym
{
T 48200 52000 5 10 0 1 0 0 1
device=IPAD
T 48100 51900 5 10 1 1 0 1 1
netlabel=EM_Rd[3:0]
}
C 46700 48500 1 0 0 ipad-1.sym
{
T 46784 48721 5 10 0 1 0 0 1
device=IPAD
T 46700 48600 5 10 1 1 0 1 1
netlabel=EM_Mr
}
C 46700 48300 1 0 0 ipad-1.sym
{
T 46784 48521 5 10 0 1 0 0 1
device=IPAD
T 46700 48400 5 10 1 1 0 1 1
netlabel=EM_Mw
}
C 48100 49700 1 0 0 ipad-1.sym
{
T 48184 49921 5 10 0 1 0 0 1
device=IPAD
T 48100 49800 5 10 1 1 0 1 1
netlabel=I_I
}
C 53500 46300 1 0 0 opad-1.sym
{
T 53802 46518 5 10 0 1 0 0 1
device=OPAD
T 53700 46400 5 10 1 1 0 1 1
netlabel=MC_Mr
}
C 53500 46700 1 0 0 opad-1.sym
{
T 53802 46918 5 10 0 1 0 0 1
device=OPAD
T 53700 46800 5 10 1 1 0 1 1
netlabel=MC_Mw
}
C 51200 48400 1 0 0 opad-1.sym
{
T 51502 48618 5 10 0 1 0 0 1
device=OPAD
T 51400 48500 5 10 1 1 0 1 1
netlabel=MC_Ir
}
C 54300 51800 1 0 0 opad-2.sym
{
T 54500 52000 5 10 0 1 0 0 1
device=OPAD
T 54500 51900 5 10 1 1 0 1 1
netlabel=MC_Rd[3:0]
}
C 50800 44500 1 0 0 gnd-1.sym
N 50900 44800 50900 51200 4
N 50900 49600 51100 49600 4
N 50900 50000 51100 50000 4
N 50900 50400 51100 50400 4
N 50900 50800 51100 50800 4
N 50900 51200 51100 51200 4
U 49600 51900 49600 50400 10 1
N 51100 50200 49800 50200 4
{
T 49800 50200 6 10 1 1 0 0 1
netname=EM_Rd0
}
C 49800 50200 1 90 0 busripper-1.sym
{
T 49400 50200 5 8 0 0 90 0 1
device=none
}
N 51100 50600 49800 50600 4
{
T 49800 50600 6 10 1 1 0 0 1
netname=EM_Rd1
}
C 49800 50600 1 90 0 busripper-1.sym
{
T 49400 50600 5 8 0 0 90 0 1
device=none
}
N 51100 51000 49800 51000 4
{
T 49800 51000 6 10 1 1 0 0 1
netname=EM_Rd2
}
C 49800 51000 1 90 0 busripper-1.sym
{
T 49400 51000 5 8 0 0 90 0 1
device=none
}
N 51100 51400 49800 51400 4
{
T 49800 51400 6 10 1 1 0 0 1
netname=EM_Rd3
}
C 49800 51400 1 90 0 busripper-1.sym
{
T 49400 51400 5 8 0 0 90 0 1
device=none
}
N 49600 49800 51100 49800 4
U 54300 50200 54300 51900 10 1
N 53100 50000 54100 50000 4
{
T 53400 50000 6 10 1 1 0 0 1
netname=MC_Rd0
}
C 54100 50000 1 0 0 busripper-1.sym
{
T 54100 50400 5 8 0 0 0 0 1
device=none
}
N 53100 50400 54100 50400 4
{
T 53400 50400 6 10 1 1 0 0 1
netname=MC_Rd1
}
C 54100 50400 1 0 0 busripper-1.sym
{
T 54100 50800 5 8 0 0 0 0 1
device=none
}
N 53100 50800 54100 50800 4
{
T 53400 50800 6 10 1 1 0 0 1
netname=MC_Rd2
}
C 54100 50800 1 0 0 busripper-1.sym
{
T 54100 51200 5 8 0 0 0 0 1
device=none
}
N 53100 51200 54100 51200 4
{
T 53400 51200 6 10 1 1 0 0 1
netname=MC_Rd3
}
C 54100 51200 1 0 0 busripper-1.sym
{
T 54100 51600 5 8 0 0 0 0 1
device=none
}
C 50100 48300 1 270 0 7432-2.sym
{
T 50600 48200 5 10 0 0 270 0 1
device=7432
T 50300 48100 5 10 1 1 270 1 1
refdes=U2
T 52000 48200 5 10 0 0 270 0 1
footprint=DIP14
T 50100 48300 5 10 0 0 0 0 1
slot=1
}
C 48800 48300 1 0 0 7408-2.sym
{
T 48900 49100 5 10 0 0 0 0 1
device=7408
T 49000 48500 5 10 1 1 0 1 1
refdes=U1
T 48900 50500 5 10 0 0 0 0 1
footprint=SO14
T 48900 48900 5 10 0 0 0 0 1
value=SN74HC08DE4
T 48800 48300 5 10 0 0 0 0 1
slot=1
}
N 48800 48600 48200 48600 4
N 48800 48400 48200 48400 4
N 51200 48500 49800 48500 4
N 50200 48300 50200 48500 4
N 50400 48300 50400 49800 4
N 48600 48400 48600 47000 4
N 48600 47000 51100 47000 4
N 48400 48600 48400 46600 4
N 48400 46600 51100 46600 4
N 51100 45200 50900 45200 4
N 51100 46400 50900 46400 4
N 51100 46800 50900 46800 4
N 50300 47400 50300 45400 4
N 50300 45400 51100 45400 4
N 53500 46400 53100 46400 4
N 53500 46800 53100 46800 4
