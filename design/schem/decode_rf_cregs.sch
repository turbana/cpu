v 20110115 2
C 40000 40000 0 0 0 title-bordered-A2.sym
C 44700 42900 1 0 0 74154-1.sym
{
T 44700 46550 5 10 0 0 0 0 1
device=74154
T 45400 46000 5 16 1 1 0 0 1
refdes=U50
T 44700 46750 5 10 0 0 0 0 1
footprint=DIP24
}
C 47500 48900 1 0 0 74377-1.sym
{
T 47800 51650 5 10 0 0 0 0 1
device=74377
T 48200 51000 5 16 1 1 0 0 1
refdes=U52
T 47800 51850 5 10 0 0 0 0 1
footprint=DIP20
}
C 47500 51500 1 0 0 74377-1.sym
{
T 47800 54250 5 10 0 0 0 0 1
device=74377
T 48200 53600 5 16 1 1 0 0 1
refdes=U51
T 47800 54450 5 10 0 0 0 0 1
footprint=DIP20
}
C 55700 43500 1 0 0 74377-1.sym
{
T 56000 46250 5 10 0 0 0 0 1
device=74377
T 56400 45600 5 16 1 1 0 0 1
refdes=U56
T 56000 46450 5 10 0 0 0 0 1
footprint=DIP20
}
C 55700 46100 1 0 0 74377-1.sym
{
T 56000 48850 5 10 0 0 0 0 1
device=74377
T 56400 48200 5 16 1 1 0 0 1
refdes=U55
T 56000 49050 5 10 0 0 0 0 1
footprint=DIP20
}
C 55700 48900 1 0 0 74377-1.sym
{
T 56000 51650 5 10 0 0 0 0 1
device=74377
T 56400 51000 5 16 1 1 0 0 1
refdes=U54
T 56000 51850 5 10 0 0 0 0 1
footprint=DIP20
}
C 55700 51500 1 0 0 74377-1.sym
{
T 56000 54250 5 10 0 0 0 0 1
device=74377
T 56400 53600 5 16 1 1 0 0 1
refdes=U53
T 56000 54450 5 10 0 0 0 0 1
footprint=DIP20
}
C 45600 46600 1 0 0 ipad-1.sym
{
T 45684 46821 5 10 0 1 0 0 1
device=IPAD
T 45600 46700 5 10 1 1 0 1 1
netlabel=CLK2
}
C 42200 46400 1 0 0 ipad-2.sym
{
T 42300 46600 5 10 0 1 0 0 1
device=IPAD
T 42200 46500 5 10 1 1 0 1 1
netlabel=I_Rd[3:0]
}
C 44400 54200 1 0 0 ipad-2.sym
{
T 44500 54400 5 10 0 1 0 0 1
device=IPAD
T 44400 54300 5 10 1 1 0 1 1
netlabel=I_D[15:0]
}
C 48300 46200 1 0 0 opad-2.sym
{
T 48500 46400 5 10 0 1 0 0 1
device=OPAD
T 48500 46300 5 10 1 1 0 1 1
netlabel=_R_S[8:0]
}
N 47100 46700 55500 46700 4
N 47500 49100 47100 49100 4
N 47100 46700 47100 51700 4
N 47100 51700 47500 51700 4
N 47500 49300 47300 49300 4
N 47300 44300 47300 51900 4
N 47300 51900 47500 51900 4
N 55500 43700 55500 51700 4
N 55500 46300 55700 46300 4
N 55500 49100 55700 49100 4
N 55500 51700 55700 51700 4
N 46700 43900 55700 43900 4
N 55300 43900 55300 46500 4
N 55300 46500 55700 46500 4
N 55700 49300 55100 49300 4
N 55100 44100 55100 51900 4
N 55100 51900 55700 51900 4
N 55100 44100 46700 44100 4
N 47300 44300 46700 44300 4
C 44400 44400 1 0 0 gnd-1.sym
N 44500 44700 44500 45100 4
N 44500 44900 44700 44900 4
N 44500 45100 44700 45100 4
U 43700 45700 43700 46500 10 1
N 44700 45500 43900 45500 4
{
T 43900 45500 6 10 1 1 0 0 1
netname=I_Rd3
}
C 43900 45500 1 90 0 busripper-1.sym
{
T 43500 45500 5 8 0 0 90 0 1
device=none
}
N 44700 45700 43900 45700 4
{
T 43900 45700 6 10 1 1 0 0 1
netname=I_Rd2
}
C 43900 45700 1 90 0 busripper-1.sym
{
T 43500 45700 5 8 0 0 90 0 1
device=none
}
N 44700 45900 43900 45900 4
{
T 43900 45900 6 10 1 1 0 0 1
netname=I_Rd1
}
C 43900 45900 1 90 0 busripper-1.sym
{
T 43500 45900 5 8 0 0 90 0 1
device=none
}
N 44700 46100 43900 46100 4
{
T 43900 46100 6 10 1 1 0 0 1
netname=I_Rd0
}
C 43900 46100 1 90 0 busripper-1.sym
{
T 43500 46100 5 8 0 0 90 0 1
device=none
}
U 48300 44900 48300 46300 10 1
N 46700 44700 48100 44700 4
{
T 47500 44700 6 10 1 1 0 0 1
netname=_R_S7
}
C 48100 44700 1 0 0 busripper-1.sym
{
T 48100 45100 5 8 0 0 0 0 1
device=none
}
N 46700 44900 48100 44900 4
{
T 47500 44900 6 10 1 1 0 0 1
netname=_R_S6
}
C 48100 44900 1 0 0 busripper-1.sym
{
T 48100 45300 5 8 0 0 0 0 1
device=none
}
N 46700 45100 48100 45100 4
{
T 47500 45100 6 10 1 1 0 0 1
netname=_R_S5
}
C 48100 45100 1 0 0 busripper-1.sym
{
T 48100 45500 5 8 0 0 0 0 1
device=none
}
N 46700 45300 48100 45300 4
{
T 47500 45300 6 10 1 1 0 0 1
netname=_R_S4
}
C 48100 45300 1 0 0 busripper-1.sym
{
T 48100 45700 5 8 0 0 0 0 1
device=none
}
N 46700 45500 48100 45500 4
{
T 47500 45500 6 10 1 1 0 0 1
netname=_R_S3
}
C 48100 45500 1 0 0 busripper-1.sym
{
T 48100 45900 5 8 0 0 0 0 1
device=none
}
N 46700 45700 48100 45700 4
{
T 47500 45700 6 10 1 1 0 0 1
netname=_R_S2
}
C 48100 45700 1 0 0 busripper-1.sym
{
T 48100 46100 5 8 0 0 0 0 1
device=none
}
N 46700 45900 48100 45900 4
{
T 47500 45900 6 10 1 1 0 0 1
netname=_R_S1
}
C 48100 45900 1 0 0 busripper-1.sym
{
T 48100 46300 5 8 0 0 0 0 1
device=none
}
U 45900 49900 45900 54300 10 1
N 47500 49700 46100 49700 4
{
T 46100 49700 6 10 1 1 0 0 1
netname=I_D15
}
C 46100 49700 1 90 0 busripper-1.sym
{
T 45700 49700 5 8 0 0 90 0 1
device=none
}
N 47500 49900 46100 49900 4
{
T 46100 49900 6 10 1 1 0 0 1
netname=I_D14
}
C 46100 49900 1 90 0 busripper-1.sym
{
T 45700 49900 5 8 0 0 90 0 1
device=none
}
N 47500 50100 46100 50100 4
{
T 46100 50100 6 10 1 1 0 0 1
netname=I_D13
}
C 46100 50100 1 90 0 busripper-1.sym
{
T 45700 50100 5 8 0 0 90 0 1
device=none
}
N 47500 50300 46100 50300 4
{
T 46100 50300 6 10 1 1 0 0 1
netname=I_D12
}
C 46100 50300 1 90 0 busripper-1.sym
{
T 45700 50300 5 8 0 0 90 0 1
device=none
}
N 47500 50500 46100 50500 4
{
T 46100 50500 6 10 1 1 0 0 1
netname=I_D11
}
C 46100 50500 1 90 0 busripper-1.sym
{
T 45700 50500 5 8 0 0 90 0 1
device=none
}
N 47500 50700 46100 50700 4
{
T 46100 50700 6 10 1 1 0 0 1
netname=I_D10
}
C 46100 50700 1 90 0 busripper-1.sym
{
T 45700 50700 5 8 0 0 90 0 1
device=none
}
N 47500 50900 46100 50900 4
{
T 46100 50900 6 10 1 1 0 0 1
netname=I_D9
}
C 46100 50900 1 90 0 busripper-1.sym
{
T 45700 50900 5 8 0 0 90 0 1
device=none
}
N 47500 51100 46100 51100 4
{
T 46100 51100 6 10 1 1 0 0 1
netname=I_D8
}
C 46100 51100 1 90 0 busripper-1.sym
{
T 45700 51100 5 8 0 0 90 0 1
device=none
}
N 47500 52300 46100 52300 4
{
T 46100 52300 6 10 1 1 0 0 1
netname=I_D7
}
C 46100 52300 1 90 0 busripper-1.sym
{
T 45700 52300 5 8 0 0 90 0 1
device=none
}
N 47500 52500 46100 52500 4
{
T 46100 52500 6 10 1 1 0 0 1
netname=I_D6
}
C 46100 52500 1 90 0 busripper-1.sym
{
T 45700 52500 5 8 0 0 90 0 1
device=none
}
N 47500 52700 46100 52700 4
{
T 46100 52700 6 10 1 1 0 0 1
netname=I_D5
}
C 46100 52700 1 90 0 busripper-1.sym
{
T 45700 52700 5 8 0 0 90 0 1
device=none
}
N 47500 52900 46100 52900 4
{
T 46100 52900 6 10 1 1 0 0 1
netname=I_D4
}
C 46100 52900 1 90 0 busripper-1.sym
{
T 45700 52900 5 8 0 0 90 0 1
device=none
}
N 47500 53100 46100 53100 4
{
T 46100 53100 6 10 1 1 0 0 1
netname=I_D3
}
C 46100 53100 1 90 0 busripper-1.sym
{
T 45700 53100 5 8 0 0 90 0 1
device=none
}
N 47500 53300 46100 53300 4
{
T 46100 53300 6 10 1 1 0 0 1
netname=I_D2
}
C 46100 53300 1 90 0 busripper-1.sym
{
T 45700 53300 5 8 0 0 90 0 1
device=none
}
N 47500 53500 46100 53500 4
{
T 46100 53500 6 10 1 1 0 0 1
netname=I_D1
}
C 46100 53500 1 90 0 busripper-1.sym
{
T 45700 53500 5 8 0 0 90 0 1
device=none
}
N 47500 53700 46100 53700 4
{
T 46100 53700 6 10 1 1 0 0 1
netname=I_D0
}
C 46100 53700 1 90 0 busripper-1.sym
{
T 45700 53700 5 8 0 0 90 0 1
device=none
}
N 55700 46900 54300 46900 4
{
T 54300 46900 6 10 1 1 0 0 1
netname=I_D7
}
C 54300 46900 1 90 0 busripper-1.sym
{
T 53900 46900 5 8 0 0 90 0 1
device=none
}
N 55700 47100 54300 47100 4
{
T 54300 47100 6 10 1 1 0 0 1
netname=I_D6
}
C 54300 47100 1 90 0 busripper-1.sym
{
T 53900 47100 5 8 0 0 90 0 1
device=none
}
N 55700 47300 54300 47300 4
{
T 54300 47300 6 10 1 1 0 0 1
netname=I_D5
}
C 54300 47300 1 90 0 busripper-1.sym
{
T 53900 47300 5 8 0 0 90 0 1
device=none
}
N 55700 47500 54300 47500 4
{
T 54300 47500 6 10 1 1 0 0 1
netname=I_D4
}
C 54300 47500 1 90 0 busripper-1.sym
{
T 53900 47500 5 8 0 0 90 0 1
device=none
}
N 55700 47700 54300 47700 4
{
T 54300 47700 6 10 1 1 0 0 1
netname=I_D3
}
C 54300 47700 1 90 0 busripper-1.sym
{
T 53900 47700 5 8 0 0 90 0 1
device=none
}
N 55700 47900 54300 47900 4
{
T 54300 47900 6 10 1 1 0 0 1
netname=I_D2
}
C 54300 47900 1 90 0 busripper-1.sym
{
T 53900 47900 5 8 0 0 90 0 1
device=none
}
N 55700 48100 54300 48100 4
{
T 54300 48100 6 10 1 1 0 0 1
netname=I_D1
}
C 54300 48100 1 90 0 busripper-1.sym
{
T 53900 48100 5 8 0 0 90 0 1
device=none
}
N 55700 48300 54300 48300 4
{
T 54300 48300 6 10 1 1 0 0 1
netname=I_D0
}
C 54300 48300 1 90 0 busripper-1.sym
{
T 53900 48300 5 8 0 0 90 0 1
device=none
}
N 55700 44300 54300 44300 4
{
T 54300 44300 6 10 1 1 0 0 1
netname=I_D15
}
C 54300 44300 1 90 0 busripper-1.sym
{
T 53900 44300 5 8 0 0 90 0 1
device=none
}
N 55700 44500 54300 44500 4
{
T 54300 44500 6 10 1 1 0 0 1
netname=I_D14
}
C 54300 44500 1 90 0 busripper-1.sym
{
T 53900 44500 5 8 0 0 90 0 1
device=none
}
N 55700 44700 54300 44700 4
{
T 54300 44700 6 10 1 1 0 0 1
netname=I_D13
}
C 54300 44700 1 90 0 busripper-1.sym
{
T 53900 44700 5 8 0 0 90 0 1
device=none
}
N 55700 44900 54300 44900 4
{
T 54300 44900 6 10 1 1 0 0 1
netname=I_D12
}
C 54300 44900 1 90 0 busripper-1.sym
{
T 53900 44900 5 8 0 0 90 0 1
device=none
}
N 55700 45100 54300 45100 4
{
T 54300 45100 6 10 1 1 0 0 1
netname=I_D11
}
C 54300 45100 1 90 0 busripper-1.sym
{
T 53900 45100 5 8 0 0 90 0 1
device=none
}
N 55700 45300 54300 45300 4
{
T 54300 45300 6 10 1 1 0 0 1
netname=I_D10
}
C 54300 45300 1 90 0 busripper-1.sym
{
T 53900 45300 5 8 0 0 90 0 1
device=none
}
N 55700 45500 54300 45500 4
{
T 54300 45500 6 10 1 1 0 0 1
netname=I_D9
}
C 54300 45500 1 90 0 busripper-1.sym
{
T 53900 45500 5 8 0 0 90 0 1
device=none
}
N 55700 45700 54300 45700 4
{
T 54300 45700 6 10 1 1 0 0 1
netname=I_D8
}
C 54300 45700 1 90 0 busripper-1.sym
{
T 53900 45700 5 8 0 0 90 0 1
device=none
}
N 55700 52300 54300 52300 4
{
T 54300 52300 6 10 1 1 0 0 1
netname=I_D7
}
C 54300 52300 1 90 0 busripper-1.sym
{
T 53900 52300 5 8 0 0 90 0 1
device=none
}
N 55700 52500 54300 52500 4
{
T 54300 52500 6 10 1 1 0 0 1
netname=I_D6
}
C 54300 52500 1 90 0 busripper-1.sym
{
T 53900 52500 5 8 0 0 90 0 1
device=none
}
N 55700 52700 54300 52700 4
{
T 54300 52700 6 10 1 1 0 0 1
netname=I_D5
}
C 54300 52700 1 90 0 busripper-1.sym
{
T 53900 52700 5 8 0 0 90 0 1
device=none
}
N 55700 52900 54300 52900 4
{
T 54300 52900 6 10 1 1 0 0 1
netname=I_D4
}
C 54300 52900 1 90 0 busripper-1.sym
{
T 53900 52900 5 8 0 0 90 0 1
device=none
}
N 55700 53100 54300 53100 4
{
T 54300 53100 6 10 1 1 0 0 1
netname=I_D3
}
C 54300 53100 1 90 0 busripper-1.sym
{
T 53900 53100 5 8 0 0 90 0 1
device=none
}
N 55700 53300 54300 53300 4
{
T 54300 53300 6 10 1 1 0 0 1
netname=I_D2
}
C 54300 53300 1 90 0 busripper-1.sym
{
T 53900 53300 5 8 0 0 90 0 1
device=none
}
N 55700 53500 54300 53500 4
{
T 54300 53500 6 10 1 1 0 0 1
netname=I_D1
}
C 54300 53500 1 90 0 busripper-1.sym
{
T 53900 53500 5 8 0 0 90 0 1
device=none
}
N 55700 53700 54300 53700 4
{
T 54300 53700 6 10 1 1 0 0 1
netname=I_D0
}
C 54300 53700 1 90 0 busripper-1.sym
{
T 53900 53700 5 8 0 0 90 0 1
device=none
}
N 55700 49700 54300 49700 4
{
T 54300 49700 6 10 1 1 0 0 1
netname=I_D15
}
C 54300 49700 1 90 0 busripper-1.sym
{
T 53900 49700 5 8 0 0 90 0 1
device=none
}
N 55700 49900 54300 49900 4
{
T 54300 49900 6 10 1 1 0 0 1
netname=I_D14
}
C 54300 49900 1 90 0 busripper-1.sym
{
T 53900 49900 5 8 0 0 90 0 1
device=none
}
N 55700 50100 54300 50100 4
{
T 54300 50100 6 10 1 1 0 0 1
netname=I_D13
}
C 54300 50100 1 90 0 busripper-1.sym
{
T 53900 50100 5 8 0 0 90 0 1
device=none
}
N 55700 50300 54300 50300 4
{
T 54300 50300 6 10 1 1 0 0 1
netname=I_D12
}
C 54300 50300 1 90 0 busripper-1.sym
{
T 53900 50300 5 8 0 0 90 0 1
device=none
}
N 55700 50500 54300 50500 4
{
T 54300 50500 6 10 1 1 0 0 1
netname=I_D11
}
C 54300 50500 1 90 0 busripper-1.sym
{
T 53900 50500 5 8 0 0 90 0 1
device=none
}
N 55700 50700 54300 50700 4
{
T 54300 50700 6 10 1 1 0 0 1
netname=I_D10
}
C 54300 50700 1 90 0 busripper-1.sym
{
T 53900 50700 5 8 0 0 90 0 1
device=none
}
N 55700 50900 54300 50900 4
{
T 54300 50900 6 10 1 1 0 0 1
netname=I_D9
}
C 54300 50900 1 90 0 busripper-1.sym
{
T 53900 50900 5 8 0 0 90 0 1
device=none
}
N 55700 51100 54300 51100 4
{
T 54300 51100 6 10 1 1 0 0 1
netname=I_D8
}
C 54300 51100 1 90 0 busripper-1.sym
{
T 53900 51100 5 8 0 0 90 0 1
device=none
}
U 54100 44500 54100 54300 10 1
U 54100 54300 45900 54300 10 0
U 51700 53500 51700 49300 10 -1
N 49500 53700 51500 53700 4
{
T 50800 53700 6 10 1 1 0 0 1
netname=_9R0
}
C 51500 53700 1 270 0 busripper-1.sym
{
T 51900 53700 5 8 0 0 270 0 1
device=none
}
N 49500 53500 51500 53500 4
{
T 50800 53500 6 10 1 1 0 0 1
netname=_9R1
}
C 51500 53500 1 270 0 busripper-1.sym
{
T 51900 53500 5 8 0 0 270 0 1
device=none
}
N 49500 53300 51500 53300 4
{
T 50800 53300 6 10 1 1 0 0 1
netname=_9R2
}
C 51500 53300 1 270 0 busripper-1.sym
{
T 51900 53300 5 8 0 0 270 0 1
device=none
}
N 49500 53100 51500 53100 4
{
T 50800 53100 6 10 1 1 0 0 1
netname=_9R3
}
C 51500 53100 1 270 0 busripper-1.sym
{
T 51900 53100 5 8 0 0 270 0 1
device=none
}
N 49500 52900 51500 52900 4
{
T 50800 52900 6 10 1 1 0 0 1
netname=_9R4
}
C 51500 52900 1 270 0 busripper-1.sym
{
T 51900 52900 5 8 0 0 270 0 1
device=none
}
N 49500 52700 51500 52700 4
{
T 50800 52700 6 10 1 1 0 0 1
netname=_9R5
}
C 51500 52700 1 270 0 busripper-1.sym
{
T 51900 52700 5 8 0 0 270 0 1
device=none
}
N 49500 52500 51500 52500 4
{
T 50800 52500 6 10 1 1 0 0 1
netname=_9R6
}
C 51500 52500 1 270 0 busripper-1.sym
{
T 51900 52500 5 8 0 0 270 0 1
device=none
}
N 49500 52300 51500 52300 4
{
T 50800 52300 6 10 1 1 0 0 1
netname=_9R7
}
C 51500 52300 1 270 0 busripper-1.sym
{
T 51900 52300 5 8 0 0 270 0 1
device=none
}
N 49500 51100 51500 51100 4
{
T 50800 51100 6 10 1 1 0 0 1
netname=_9R8
}
C 51500 51100 1 270 0 busripper-1.sym
{
T 51900 51100 5 8 0 0 270 0 1
device=none
}
N 49500 50900 51500 50900 4
{
T 50800 50900 6 10 1 1 0 0 1
netname=_9R9
}
C 51500 50900 1 270 0 busripper-1.sym
{
T 51900 50900 5 8 0 0 270 0 1
device=none
}
N 49500 50700 51500 50700 4
{
T 50800 50700 6 10 1 1 0 0 1
netname=_9R10
}
C 51500 50700 1 270 0 busripper-1.sym
{
T 51900 50700 5 8 0 0 270 0 1
device=none
}
N 49500 50500 51500 50500 4
{
T 50800 50500 6 10 1 1 0 0 1
netname=_9R11
}
C 51500 50500 1 270 0 busripper-1.sym
{
T 51900 50500 5 8 0 0 270 0 1
device=none
}
N 49500 50300 51500 50300 4
{
T 50800 50300 6 10 1 1 0 0 1
netname=_9R12
}
C 51500 50300 1 270 0 busripper-1.sym
{
T 51900 50300 5 8 0 0 270 0 1
device=none
}
N 49500 50100 51500 50100 4
{
T 50800 50100 6 10 1 1 0 0 1
netname=_9R13
}
C 51500 50100 1 270 0 busripper-1.sym
{
T 51900 50100 5 8 0 0 270 0 1
device=none
}
N 49500 49900 51500 49900 4
{
T 50800 49900 6 10 1 1 0 0 1
netname=_9R14
}
C 51500 49900 1 270 0 busripper-1.sym
{
T 51900 49900 5 8 0 0 270 0 1
device=none
}
N 49500 49700 51500 49700 4
{
T 50800 49700 6 10 1 1 0 0 1
netname=_9R15
}
C 51500 49700 1 270 0 busripper-1.sym
{
T 51900 49700 5 8 0 0 270 0 1
device=none
}
U 59300 53500 59300 49300 10 -1
N 57700 53700 59100 53700 4
{
T 58300 53700 6 10 1 1 0 0 1
netname=_10R0
}
C 59100 53700 1 270 0 busripper-1.sym
{
T 59500 53700 5 8 0 0 270 0 1
device=none
}
N 57700 53500 59100 53500 4
{
T 58300 53500 6 10 1 1 0 0 1
netname=_10R1
}
C 59100 53500 1 270 0 busripper-1.sym
{
T 59500 53500 5 8 0 0 270 0 1
device=none
}
N 57700 53300 59100 53300 4
{
T 58300 53300 6 10 1 1 0 0 1
netname=_10R2
}
C 59100 53300 1 270 0 busripper-1.sym
{
T 59500 53300 5 8 0 0 270 0 1
device=none
}
N 57700 53100 59100 53100 4
{
T 58300 53100 6 10 1 1 0 0 1
netname=_10R3
}
C 59100 53100 1 270 0 busripper-1.sym
{
T 59500 53100 5 8 0 0 270 0 1
device=none
}
N 57700 52900 59100 52900 4
{
T 58300 52900 6 10 1 1 0 0 1
netname=_10R4
}
C 59100 52900 1 270 0 busripper-1.sym
{
T 59500 52900 5 8 0 0 270 0 1
device=none
}
N 57700 52700 59100 52700 4
{
T 58300 52700 6 10 1 1 0 0 1
netname=_10R5
}
C 59100 52700 1 270 0 busripper-1.sym
{
T 59500 52700 5 8 0 0 270 0 1
device=none
}
N 57700 52500 59100 52500 4
{
T 58300 52500 6 10 1 1 0 0 1
netname=_10R6
}
C 59100 52500 1 270 0 busripper-1.sym
{
T 59500 52500 5 8 0 0 270 0 1
device=none
}
N 57700 52300 59100 52300 4
{
T 58300 52300 6 10 1 1 0 0 1
netname=_10R7
}
C 59100 52300 1 270 0 busripper-1.sym
{
T 59500 52300 5 8 0 0 270 0 1
device=none
}
N 57700 51100 59100 51100 4
{
T 58300 51100 6 10 1 1 0 0 1
netname=_10R8
}
C 59100 51100 1 270 0 busripper-1.sym
{
T 59500 51100 5 8 0 0 270 0 1
device=none
}
N 57700 50900 59100 50900 4
{
T 58300 50900 6 10 1 1 0 0 1
netname=_10R9
}
C 59100 50900 1 270 0 busripper-1.sym
{
T 59500 50900 5 8 0 0 270 0 1
device=none
}
N 57700 50700 59100 50700 4
{
T 58300 50700 6 10 1 1 0 0 1
netname=_10R10
}
C 59100 50700 1 270 0 busripper-1.sym
{
T 59500 50700 5 8 0 0 270 0 1
device=none
}
N 57700 50500 59100 50500 4
{
T 58300 50500 6 10 1 1 0 0 1
netname=_10R11
}
C 59100 50500 1 270 0 busripper-1.sym
{
T 59500 50500 5 8 0 0 270 0 1
device=none
}
N 57700 50300 59100 50300 4
{
T 58300 50300 6 10 1 1 0 0 1
netname=_10R12
}
C 59100 50300 1 270 0 busripper-1.sym
{
T 59500 50300 5 8 0 0 270 0 1
device=none
}
N 57700 50100 59100 50100 4
{
T 58300 50100 6 10 1 1 0 0 1
netname=_10R13
}
C 59100 50100 1 270 0 busripper-1.sym
{
T 59500 50100 5 8 0 0 270 0 1
device=none
}
N 57700 49900 59100 49900 4
{
T 58300 49900 6 10 1 1 0 0 1
netname=_10R14
}
C 59100 49900 1 270 0 busripper-1.sym
{
T 59500 49900 5 8 0 0 270 0 1
device=none
}
N 57700 49700 59100 49700 4
{
T 58300 49700 6 10 1 1 0 0 1
netname=_10R15
}
C 59100 49700 1 270 0 busripper-1.sym
{
T 59500 49700 5 8 0 0 270 0 1
device=none
}
C 59100 48300 1 270 0 busripper-1.sym
{
T 59500 48300 5 8 0 0 270 0 1
device=none
}
N 57700 48300 59100 48300 4
{
T 58300 48300 6 10 1 1 0 0 1
netname=_11R0
}
C 59100 48100 1 270 0 busripper-1.sym
{
T 59500 48100 5 8 0 0 270 0 1
device=none
}
N 57700 48100 59100 48100 4
{
T 58300 48100 6 10 1 1 0 0 1
netname=_11R1
}
C 59100 47900 1 270 0 busripper-1.sym
{
T 59500 47900 5 8 0 0 270 0 1
device=none
}
N 57700 47900 59100 47900 4
{
T 58300 47900 6 10 1 1 0 0 1
netname=_11R2
}
C 59100 47700 1 270 0 busripper-1.sym
{
T 59500 47700 5 8 0 0 270 0 1
device=none
}
N 57700 47700 59100 47700 4
{
T 58300 47700 6 10 1 1 0 0 1
netname=_11R3
}
C 59100 47500 1 270 0 busripper-1.sym
{
T 59500 47500 5 8 0 0 270 0 1
device=none
}
N 57700 47500 59100 47500 4
{
T 58300 47500 6 10 1 1 0 0 1
netname=_11R4
}
C 59100 47300 1 270 0 busripper-1.sym
{
T 59500 47300 5 8 0 0 270 0 1
device=none
}
N 57700 47300 59100 47300 4
{
T 58300 47300 6 10 1 1 0 0 1
netname=_11R5
}
C 59100 47100 1 270 0 busripper-1.sym
{
T 59500 47100 5 8 0 0 270 0 1
device=none
}
N 57700 47100 59100 47100 4
{
T 58300 47100 6 10 1 1 0 0 1
netname=_11R6
}
C 59100 46900 1 270 0 busripper-1.sym
{
T 59500 46900 5 8 0 0 270 0 1
device=none
}
N 57700 46900 59100 46900 4
{
T 58300 46900 6 10 1 1 0 0 1
netname=_11R7
}
C 59100 45700 1 270 0 busripper-1.sym
{
T 59500 45700 5 8 0 0 270 0 1
device=none
}
N 57700 45700 59100 45700 4
{
T 58300 45700 6 10 1 1 0 0 1
netname=_11R8
}
C 59100 45500 1 270 0 busripper-1.sym
{
T 59500 45500 5 8 0 0 270 0 1
device=none
}
N 57700 45500 59100 45500 4
{
T 58300 45500 6 10 1 1 0 0 1
netname=_11R9
}
C 59100 45300 1 270 0 busripper-1.sym
{
T 59500 45300 5 8 0 0 270 0 1
device=none
}
N 57700 45300 59100 45300 4
{
T 58300 45300 6 10 1 1 0 0 1
netname=_11R10
}
C 59100 45100 1 270 0 busripper-1.sym
{
T 59500 45100 5 8 0 0 270 0 1
device=none
}
N 57700 45100 59100 45100 4
{
T 58300 45100 6 10 1 1 0 0 1
netname=_11R11
}
C 59100 44900 1 270 0 busripper-1.sym
{
T 59500 44900 5 8 0 0 270 0 1
device=none
}
N 57700 44900 59100 44900 4
{
T 58300 44900 6 10 1 1 0 0 1
netname=_11R12
}
C 59100 44700 1 270 0 busripper-1.sym
{
T 59500 44700 5 8 0 0 270 0 1
device=none
}
N 57700 44700 59100 44700 4
{
T 58300 44700 6 10 1 1 0 0 1
netname=_11R13
}
C 59100 44500 1 270 0 busripper-1.sym
{
T 59500 44500 5 8 0 0 270 0 1
device=none
}
N 57700 44500 59100 44500 4
{
T 58300 44500 6 10 1 1 0 0 1
netname=_11R14
}
C 59100 44300 1 270 0 busripper-1.sym
{
T 59500 44300 5 8 0 0 270 0 1
device=none
}
N 57700 44300 59100 44300 4
{
T 58300 44300 6 10 1 1 0 0 1
netname=_11R15
}
N 55500 43700 55700 43700 4
C 51700 49200 1 0 0 opad-2.sym
{
T 51900 49400 5 10 0 1 0 0 1
device=OPAD
T 51900 49300 5 10 1 1 0 1 1
netlabel=_9R[15:0]
}
C 59300 49200 1 0 0 opad-2.sym
{
T 59500 49400 5 10 0 1 0 0 1
device=OPAD
T 59500 49300 5 10 1 1 0 1 1
netlabel=_10R[15:0]
}
C 59300 43800 1 0 0 opad-2.sym
{
T 59500 44000 5 10 0 1 0 0 1
device=OPAD
T 59500 43900 5 10 1 1 0 1 1
netlabel=_11R[15:0]
}
U 59300 48100 59300 43900 10 -1
C 49500 55400 1 0 0 opad-1.sym
{
T 49802 55618 5 10 0 1 0 0 1
device=OPAD
T 49700 55500 5 10 1 1 0 1 1
netlabel=R_IE
}
N 49500 53700 49500 55500 4
