v 20110115 2
C 40000 40000 0 0 0 title-bordered-A2.sym
C 43100 45000 1 270 0 74244-1.sym
{
T 46250 44700 5 10 0 0 270 0 1
device=74244
T 45200 44300 5 16 1 1 270 0 1
refdes=U275
T 46450 44700 5 10 0 0 270 0 1
footprint=DIP20
}
C 43500 50700 1 270 0 74244-1.sym
{
T 46650 50400 5 10 0 0 270 0 1
device=74244
T 45600 50000 5 16 1 1 270 0 1
refdes=U276
T 46850 50400 5 10 0 0 270 0 1
footprint=DIP20
}
C 48500 50700 1 270 0 74244-1.sym
{
T 51650 50400 5 10 0 0 270 0 1
device=74244
T 50600 50000 5 16 1 1 270 0 1
refdes=U277
T 51850 50400 5 10 0 0 270 0 1
footprint=DIP20
}
C 51100 50700 1 270 0 74244-1.sym
{
T 54250 50400 5 10 0 0 270 0 1
device=74244
T 53200 50000 5 16 1 1 270 0 1
refdes=U278
T 54450 50400 5 10 0 0 270 0 1
footprint=DIP20
}
C 41600 45700 1 0 0 ipad-1.sym
{
T 41684 45921 5 10 0 1 0 0 1
device=IPAD
T 41600 45800 5 10 1 1 0 1 1
netlabel=MC_Mr
}
C 41600 45200 1 0 0 ipad-1.sym
{
T 41684 45421 5 10 0 1 0 0 1
device=IPAD
T 41600 45300 5 10 1 1 0 1 1
netlabel=MC_Mw
}
C 40500 54200 1 0 0 ipad-1.sym
{
T 40584 54421 5 10 0 1 0 0 1
device=IPAD
T 40500 54300 5 10 1 1 0 1 1
netlabel=EM_Mt
}
C 47200 52100 1 0 0 ipad-2.sym
{
T 47300 52300 5 10 0 1 0 0 1
device=IPAD
T 47200 52200 5 10 1 1 0 1 1
netlabel=EM_D[15:0]
}
C 44400 47100 1 0 0 ipad-2.sym
{
T 44500 47300 5 10 0 1 0 0 1
device=IPAD
T 44400 47200 5 10 1 1 0 1 1
netlabel=EM_C[15:0]
}
C 41900 55500 1 0 0 ipad-2.sym
{
T 42000 55700 5 10 0 1 0 0 1
device=IPAD
T 41900 55600 5 10 1 1 0 1 1
netlabel=R_CS[5:0]
}
C 41900 54800 1 0 0 ipad-2.sym
{
T 42000 55000 5 10 0 1 0 0 1
device=IPAD
T 41900 54900 5 10 1 1 0 1 1
netlabel=R_DS[5:0]
}
C 62700 46600 1 270 0 opad-2.sym
{
T 62900 46400 5 10 0 1 270 0 1
device=OPAD
T 62800 46400 5 10 1 1 270 1 1
netlabel=M_D[15:0]
}
C 43900 42600 1 0 0 iopad-1.sym
{
T 44202 42818 5 10 0 1 0 0 1
device=IOPAD
T 44200 42700 5 10 1 1 0 1 1
netlabel=BUS_R
}
C 43900 42300 1 0 0 iopad-1.sym
{
T 44202 42518 5 10 0 1 0 0 1
device=IOPAD
T 44200 42400 5 10 1 1 0 1 1
netlabel=BUS_W
}
C 43400 47600 1 180 0 iopad-2.sym
{
T 43200 47400 5 10 0 1 180 0 1
device=IOPAD
T 43100 47500 5 10 1 1 180 1 1
netlabel=BUS_A[22:0]
}
C 58900 41700 1 0 0 iopad-2.sym
{
T 59100 41900 5 10 0 1 0 0 1
device=IOPAD
T 59200 41800 5 10 1 1 0 1 1
netlabel=BUS_D[15:0]
}
C 41600 50800 1 0 0 ipad-1.sym
{
T 41684 51021 5 10 0 1 0 0 1
device=IPAD
T 41600 50900 5 10 1 1 0 1 1
netlabel=CLK1
}
C 42400 53900 1 270 0 74157-2.sym
{
T 45140 53800 5 10 0 0 270 0 1
device=74157
T 44940 53800 5 10 0 0 270 0 1
footprint=SO16
T 44300 53300 5 16 1 1 270 0 1
refdes=U279
T 44740 53800 5 10 0 0 270 0 1
value=SN74HC157D
}
C 44800 53900 1 270 0 74157-2.sym
{
T 47540 53800 5 10 0 0 270 0 1
device=74157
T 47340 53800 5 10 0 0 270 0 1
footprint=SO16
T 46700 53300 5 16 1 1 270 0 1
refdes=U280
T 47140 53800 5 10 0 0 270 0 1
value=SN74HC157D
}
N 42200 53900 42200 54100 4
N 42200 54100 45000 54100 4
N 42600 54100 42600 53900 4
N 45000 54100 45000 53900 4
N 45200 53900 45200 54300 4
N 45200 54300 42000 54300 4
N 42800 53900 42800 54300 4
U 46600 54900 43400 54900 10 -1
N 46800 53900 46800 54700 4
{
T 46800 54300 6 10 1 1 0 0 1
netname=R_DS0
}
C 46800 54700 1 90 0 busripper-1.sym
{
T 46400 54700 5 8 0 0 90 0 1
device=none
}
N 46400 53900 46400 54700 4
{
T 46400 54500 6 10 1 1 0 0 1
netname=R_DS1
}
C 46400 54700 1 90 0 busripper-1.sym
{
T 46000 54700 5 8 0 0 90 0 1
device=none
}
N 46000 53900 46000 54700 4
{
T 46000 54300 6 10 1 1 0 0 1
netname=R_DS2
}
C 46000 54700 1 90 0 busripper-1.sym
{
T 45600 54700 5 8 0 0 90 0 1
device=none
}
N 45600 53900 45600 54700 4
{
T 45600 54500 6 10 1 1 0 0 1
netname=R_DS3
}
C 45600 54700 1 90 0 busripper-1.sym
{
T 45200 54700 5 8 0 0 90 0 1
device=none
}
N 44400 53900 44400 54700 4
{
T 44400 54300 6 10 1 1 0 0 1
netname=R_DS4
}
C 44400 54700 1 90 0 busripper-1.sym
{
T 44000 54700 5 8 0 0 90 0 1
device=none
}
N 44000 53900 44000 54700 4
{
T 44000 54500 6 10 1 1 0 0 1
netname=R_DS5
}
C 44000 54700 1 90 0 busripper-1.sym
{
T 43600 54700 5 8 0 0 90 0 1
device=none
}
U 46400 55600 43400 55600 10 -1
N 46600 53900 46600 55400 4
{
T 46600 55000 6 10 1 1 0 0 1
netname=R_CS0
}
C 46600 55400 1 90 0 busripper-1.sym
{
T 46200 55400 5 8 0 0 90 0 1
device=none
}
N 46200 53900 46200 55400 4
{
T 46200 55200 6 10 1 1 0 0 1
netname=R_CS1
}
C 46200 55400 1 90 0 busripper-1.sym
{
T 45800 55400 5 8 0 0 90 0 1
device=none
}
N 45800 53900 45800 55400 4
{
T 45800 55000 6 10 1 1 0 0 1
netname=R_CS2
}
C 45800 55400 1 90 0 busripper-1.sym
{
T 45400 55400 5 8 0 0 90 0 1
device=none
}
N 45400 53900 45400 55400 4
{
T 45400 55200 6 10 1 1 0 0 1
netname=R_CS3
}
C 45400 55400 1 90 0 busripper-1.sym
{
T 45000 55400 5 8 0 0 90 0 1
device=none
}
N 44200 53900 44200 55400 4
{
T 44200 55000 6 10 1 1 0 0 1
netname=R_CS4
}
N 43800 53900 43800 55400 4
{
T 43800 55200 6 10 1 1 0 0 1
netname=R_CS5
}
C 44200 55400 1 90 0 busripper-1.sym
{
T 43800 55400 5 8 0 0 90 0 1
device=none
}
C 43800 55400 1 90 0 busripper-1.sym
{
T 43400 55400 5 8 0 0 90 0 1
device=none
}
N 43100 50900 52500 50900 4
N 43700 50900 43700 50700 4
N 44900 50900 44900 50700 4
N 48700 50900 48700 50700 4
N 49900 50900 49900 50700 4
N 51300 50900 51300 50700 4
N 52500 50900 52500 50700 4
U 54400 52200 48700 52200 10 -1
N 53300 50700 53300 52000 4
{
T 53300 51200 6 10 1 1 0 0 1
netname=EM_D0
}
C 53300 52000 1 90 0 busripper-1.sym
{
T 52900 52000 5 8 0 0 90 0 1
device=none
}
N 53100 50700 53100 52000 4
{
T 53100 51400 6 10 1 1 0 0 1
netname=EM_D1
}
C 53100 52000 1 90 0 busripper-1.sym
{
T 52700 52000 5 8 0 0 90 0 1
device=none
}
N 52900 50700 52900 52000 4
{
T 52900 51600 6 10 1 1 0 0 1
netname=EM_D2
}
C 52900 52000 1 90 0 busripper-1.sym
{
T 52500 52000 5 8 0 0 90 0 1
device=none
}
N 52700 50700 52700 52000 4
{
T 52700 51800 6 10 1 1 0 0 1
netname=EM_D3
}
C 52700 52000 1 90 0 busripper-1.sym
{
T 52300 52000 5 8 0 0 90 0 1
device=none
}
N 52100 50700 52100 52000 4
{
T 52100 51200 6 10 1 1 0 0 1
netname=EM_D4
}
C 52100 52000 1 90 0 busripper-1.sym
{
T 51700 52000 5 8 0 0 90 0 1
device=none
}
N 51900 50700 51900 52000 4
{
T 51900 51400 6 10 1 1 0 0 1
netname=EM_D5
}
C 51900 52000 1 90 0 busripper-1.sym
{
T 51500 52000 5 8 0 0 90 0 1
device=none
}
N 51700 50700 51700 52000 4
{
T 51700 51600 6 10 1 1 0 0 1
netname=EM_D6
}
C 51700 52000 1 90 0 busripper-1.sym
{
T 51300 52000 5 8 0 0 90 0 1
device=none
}
N 51500 50700 51500 52000 4
{
T 51500 51800 6 10 1 1 0 0 1
netname=EM_D7
}
C 51500 52000 1 90 0 busripper-1.sym
{
T 51100 52000 5 8 0 0 90 0 1
device=none
}
N 50700 50700 50700 52000 4
{
T 50700 51200 6 10 1 1 0 0 1
netname=EM_D8
}
C 50700 52000 1 90 0 busripper-1.sym
{
T 50300 52000 5 8 0 0 90 0 1
device=none
}
N 50500 50700 50500 52000 4
{
T 50500 51400 6 10 1 1 0 0 1
netname=EM_D9
}
C 50500 52000 1 90 0 busripper-1.sym
{
T 50100 52000 5 8 0 0 90 0 1
device=none
}
N 50300 50700 50300 52000 4
{
T 50300 51600 6 10 1 1 0 0 1
netname=EM_D10
}
C 50300 52000 1 90 0 busripper-1.sym
{
T 49900 52000 5 8 0 0 90 0 1
device=none
}
N 50100 50700 50100 52000 4
{
T 50100 51800 6 10 1 1 0 0 1
netname=EM_D11
}
C 50100 52000 1 90 0 busripper-1.sym
{
T 49700 52000 5 8 0 0 90 0 1
device=none
}
N 49500 50700 49500 52000 4
{
T 49500 51200 6 10 1 1 0 0 1
netname=EM_D12
}
C 49500 52000 1 90 0 busripper-1.sym
{
T 49100 52000 5 8 0 0 90 0 1
device=none
}
N 49300 50700 49300 52000 4
{
T 49300 51400 6 10 1 1 0 0 1
netname=EM_D13
}
C 49300 52000 1 90 0 busripper-1.sym
{
T 48900 52000 5 8 0 0 90 0 1
device=none
}
N 49100 50700 49100 52000 4
{
T 49100 51600 6 10 1 1 0 0 1
netname=EM_D14
}
C 49100 52000 1 90 0 busripper-1.sym
{
T 48700 52000 5 8 0 0 90 0 1
device=none
}
N 48900 50700 48900 52000 4
{
T 48900 51800 6 10 1 1 0 0 1
netname=EM_D15
}
C 48900 52000 1 90 0 busripper-1.sym
{
T 48500 52000 5 8 0 0 90 0 1
device=none
}
N 45400 51900 45100 51900 4
N 45100 51900 45100 50700 4
N 45800 51900 45800 51700 4
N 45800 51700 45300 51700 4
N 45300 51700 45300 50700 4
N 46200 51900 46200 51500 4
N 46200 51500 45500 51500 4
N 45500 51500 45500 50700 4
N 46600 51900 46600 51300 4
N 46600 51300 45700 51300 4
N 45700 51300 45700 50700 4
N 44200 51900 44500 51900 4
N 44500 51900 44500 50700 4
N 43800 51900 43800 51700 4
N 43800 51700 44300 51700 4
N 44300 51700 44300 50700 4
N 42000 54300 42000 51500 4
N 42000 51500 44100 51500 4
N 44100 51500 44100 50700 4
N 43100 45300 43900 45300 4
N 43100 45800 43900 45800 4
N 43900 42700 43700 42700 4
N 43700 42700 43700 43000 4
N 43900 42400 43500 42400 4
N 43500 42400 43500 43000 4
N 43300 45000 43300 50900 4
U 53100 47500 43400 47500 10 -1
N 53300 48700 53300 47700 4
{
T 53300 48300 6 10 1 1 0 0 1
netname=BUS_A0
}
C 53300 47700 1 180 0 busripper-1.sym
{
T 53300 47300 5 8 0 0 180 0 1
device=none
}
N 53100 48700 53100 47700 4
{
T 53100 48100 6 10 1 1 0 0 1
netname=BUS_A1
}
C 53100 47700 1 180 0 busripper-1.sym
{
T 53100 47300 5 8 0 0 180 0 1
device=none
}
N 52900 48700 52900 47700 4
{
T 52900 47900 6 10 1 1 0 0 1
netname=BUS_A2
}
C 52900 47700 1 180 0 busripper-1.sym
{
T 52900 47300 5 8 0 0 180 0 1
device=none
}
N 52700 48700 52700 47700 4
{
T 52700 47700 6 10 1 1 0 0 1
netname=BUS_A3
}
C 52700 47700 1 180 0 busripper-1.sym
{
T 52700 47300 5 8 0 0 180 0 1
device=none
}
N 52100 48700 52100 47700 4
{
T 52100 48300 6 10 1 1 0 0 1
netname=BUS_A4
}
C 52100 47700 1 180 0 busripper-1.sym
{
T 52100 47300 5 8 0 0 180 0 1
device=none
}
N 51900 48700 51900 47700 4
{
T 51900 48100 6 10 1 1 0 0 1
netname=BUS_A5
}
C 51900 47700 1 180 0 busripper-1.sym
{
T 51900 47300 5 8 0 0 180 0 1
device=none
}
N 51700 48700 51700 47700 4
{
T 51700 47900 6 10 1 1 0 0 1
netname=BUS_A6
}
C 51700 47700 1 180 0 busripper-1.sym
{
T 51700 47300 5 8 0 0 180 0 1
device=none
}
N 51500 48700 51500 47700 4
{
T 51500 47700 6 10 1 1 0 0 1
netname=BUS_A7
}
C 51500 47700 1 180 0 busripper-1.sym
{
T 51500 47300 5 8 0 0 180 0 1
device=none
}
N 50700 48700 50700 47700 4
{
T 50700 48300 6 10 1 1 0 0 1
netname=BUS_A8
}
C 50700 47700 1 180 0 busripper-1.sym
{
T 50700 47300 5 8 0 0 180 0 1
device=none
}
N 50500 48700 50500 47700 4
{
T 50500 48100 6 10 1 1 0 0 1
netname=BUS_A9
}
C 50500 47700 1 180 0 busripper-1.sym
{
T 50500 47300 5 8 0 0 180 0 1
device=none
}
N 50300 48700 50300 47700 4
{
T 50300 47900 6 10 1 1 0 0 1
netname=BUS_A10
}
C 50300 47700 1 180 0 busripper-1.sym
{
T 50300 47300 5 8 0 0 180 0 1
device=none
}
N 50100 48700 50100 47700 4
{
T 50100 47700 6 10 1 1 0 0 1
netname=BUS_A11
}
C 50100 47700 1 180 0 busripper-1.sym
{
T 50100 47300 5 8 0 0 180 0 1
device=none
}
N 49500 48700 49500 47700 4
{
T 49500 48300 6 10 1 1 0 0 1
netname=BUS_A12
}
C 49500 47700 1 180 0 busripper-1.sym
{
T 49500 47300 5 8 0 0 180 0 1
device=none
}
N 49300 48700 49300 47700 4
{
T 49300 48100 6 10 1 1 0 0 1
netname=BUS_A13
}
C 49300 47700 1 180 0 busripper-1.sym
{
T 49300 47300 5 8 0 0 180 0 1
device=none
}
N 49100 48700 49100 47700 4
{
T 49100 47900 6 10 1 1 0 0 1
netname=BUS_A14
}
C 49100 47700 1 180 0 busripper-1.sym
{
T 49100 47300 5 8 0 0 180 0 1
device=none
}
N 48900 48700 48900 47700 4
{
T 48900 47700 6 10 1 1 0 0 1
netname=BUS_A15
}
C 48900 47700 1 180 0 busripper-1.sym
{
T 48900 47300 5 8 0 0 180 0 1
device=none
}
N 45700 48700 45700 47700 4
{
T 45700 48300 6 10 1 1 0 0 1
netname=BUS_A16
}
C 45700 47700 1 180 0 busripper-1.sym
{
T 45700 47300 5 8 0 0 180 0 1
device=none
}
N 45500 48700 45500 47700 4
{
T 45500 48100 6 10 1 1 0 0 1
netname=BUS_A17
}
C 45500 47700 1 180 0 busripper-1.sym
{
T 45500 47300 5 8 0 0 180 0 1
device=none
}
N 45300 48700 45300 47700 4
{
T 45300 47900 6 10 1 1 0 0 1
netname=BUS_A18
}
C 45300 47700 1 180 0 busripper-1.sym
{
T 45300 47300 5 8 0 0 180 0 1
device=none
}
N 45100 48700 45100 47700 4
{
T 45100 47700 6 10 1 1 0 0 1
netname=BUS_A19
}
C 45100 47700 1 180 0 busripper-1.sym
{
T 45100 47300 5 8 0 0 180 0 1
device=none
}
N 44500 48700 44500 47700 4
{
T 44500 48100 6 10 1 1 0 0 1
netname=BUS_A20
}
C 44500 47700 1 180 0 busripper-1.sym
{
T 44500 47300 5 8 0 0 180 0 1
device=none
}
N 44300 48700 44300 47700 4
{
T 44300 47900 6 10 1 1 0 0 1
netname=BUS_A21
}
C 44300 47700 1 180 0 busripper-1.sym
{
T 44300 47300 5 8 0 0 180 0 1
device=none
}
N 44100 48700 44100 47700 4
{
T 44100 47700 6 10 1 1 0 0 1
netname=BUS_A22
}
C 44100 47700 1 180 0 busripper-1.sym
{
T 44100 47300 5 8 0 0 180 0 1
device=none
}
C 45900 45000 1 270 0 74244-1.sym
{
T 49050 44700 5 10 0 0 270 0 1
device=74244
T 48000 44300 5 16 1 1 270 0 1
refdes=U281
T 49250 44700 5 10 0 0 270 0 1
footprint=DIP20
}
C 48500 45000 1 270 0 74244-1.sym
{
T 51650 44700 5 10 0 0 270 0 1
device=74244
T 50600 44300 5 16 1 1 270 0 1
refdes=U282
T 51850 44700 5 10 0 0 270 0 1
footprint=DIP20
}
N 46000 45400 49900 45400 4
N 46100 45000 46100 45400 4
N 47300 45400 47300 45000 4
N 48700 45400 48700 45000 4
N 49900 45400 49900 45000 4
C 43900 45100 1 0 0 7404-1.sym
{
T 44200 45300 5 10 1 1 0 1 1
refdes=U283A
T 44000 46100 5 10 0 0 0 0 1
device=7404
T 44000 47900 5 10 0 0 0 0 1
footprint=DIP14
T 44000 45900 5 10 0 0 0 0 1
value=74HC04BQ
T 43900 45100 5 10 0 0 0 0 1
slot=1
}
C 45100 45200 1 0 0 7432-2.sym
{
T 45200 45700 5 10 0 0 0 0 1
device=7432
T 45300 45400 5 10 1 1 0 1 1
refdes=U284A
T 45200 47100 5 10 0 0 0 0 1
footprint=DIP14
T 45100 45200 5 10 0 0 0 0 1
slot=1
}
U 50500 47200 45900 47200 10 -1
N 50700 45000 50700 47000 4
{
T 50700 46800 6 10 1 1 0 0 1
netname=EM_C0
}
C 50700 47000 1 90 0 busripper-1.sym
{
T 50300 47000 5 8 0 0 90 0 1
device=none
}
N 50500 45000 50500 47000 4
{
T 50500 46600 6 10 1 1 0 0 1
netname=EM_C1
}
C 50500 47000 1 90 0 busripper-1.sym
{
T 50100 47000 5 8 0 0 90 0 1
device=none
}
N 50300 45000 50300 47000 4
{
T 50300 46400 6 10 1 1 0 0 1
netname=EM_C2
}
C 50300 47000 1 90 0 busripper-1.sym
{
T 49900 47000 5 8 0 0 90 0 1
device=none
}
N 50100 45000 50100 47000 4
{
T 50100 46200 6 10 1 1 0 0 1
netname=EM_C3
}
C 50100 47000 1 90 0 busripper-1.sym
{
T 49700 47000 5 8 0 0 90 0 1
device=none
}
N 49500 45000 49500 47000 4
{
T 49500 46800 6 10 1 1 0 0 1
netname=EM_C4
}
C 49500 47000 1 90 0 busripper-1.sym
{
T 49100 47000 5 8 0 0 90 0 1
device=none
}
N 49300 45000 49300 47000 4
{
T 49300 46600 6 10 1 1 0 0 1
netname=EM_C5
}
C 49300 47000 1 90 0 busripper-1.sym
{
T 48900 47000 5 8 0 0 90 0 1
device=none
}
N 49100 45000 49100 47000 4
{
T 49100 46400 6 10 1 1 0 0 1
netname=EM_C6
}
C 49100 47000 1 90 0 busripper-1.sym
{
T 48700 47000 5 8 0 0 90 0 1
device=none
}
N 48900 45000 48900 47000 4
{
T 48900 46200 6 10 1 1 0 0 1
netname=EM_C7
}
C 48900 47000 1 90 0 busripper-1.sym
{
T 48500 47000 5 8 0 0 90 0 1
device=none
}
N 48100 45000 48100 47000 4
{
T 48100 46800 6 10 1 1 0 0 1
netname=EM_C8
}
C 48100 47000 1 90 0 busripper-1.sym
{
T 47700 47000 5 8 0 0 90 0 1
device=none
}
N 47900 45000 47900 47000 4
{
T 47900 46600 6 10 1 1 0 0 1
netname=EM_C9
}
C 47900 47000 1 90 0 busripper-1.sym
{
T 47500 47000 5 8 0 0 90 0 1
device=none
}
N 47700 45000 47700 47000 4
{
T 47700 46400 6 10 1 1 0 0 1
netname=EM_C10
}
C 47700 47000 1 90 0 busripper-1.sym
{
T 47300 47000 5 8 0 0 90 0 1
device=none
}
N 47500 45000 47500 47000 4
{
T 47500 46200 6 10 1 1 0 0 1
netname=EM_C11
}
C 47500 47000 1 90 0 busripper-1.sym
{
T 47100 47000 5 8 0 0 90 0 1
device=none
}
N 46900 45000 46900 47000 4
{
T 46900 46800 6 10 1 1 0 0 1
netname=EM_C12
}
C 46900 47000 1 90 0 busripper-1.sym
{
T 46500 47000 5 8 0 0 90 0 1
device=none
}
N 46700 45000 46700 47000 4
{
T 46700 46600 6 10 1 1 0 0 1
netname=EM_C13
}
C 46700 47000 1 90 0 busripper-1.sym
{
T 46300 47000 5 8 0 0 90 0 1
device=none
}
N 46500 45000 46500 47000 4
{
T 46500 46400 6 10 1 1 0 0 1
netname=EM_C14
}
C 46500 47000 1 90 0 busripper-1.sym
{
T 46100 47000 5 8 0 0 90 0 1
device=none
}
N 46300 45000 46300 47000 4
{
T 46300 46200 6 10 1 1 0 0 1
netname=EM_C15
}
C 46300 47000 1 90 0 busripper-1.sym
{
T 45900 47000 5 8 0 0 90 0 1
device=none
}
U 46500 41800 58900 41800 10 1
N 46300 43000 46300 42000 4
{
T 46300 42000 6 10 1 1 0 0 1
netname=BUS_D15
}
C 46300 42000 1 270 0 busripper-1.sym
{
T 46700 42000 5 8 0 0 270 0 1
device=none
}
N 46500 43000 46500 42000 4
{
T 46500 42200 6 10 1 1 0 0 1
netname=BUS_D14
}
C 46500 42000 1 270 0 busripper-1.sym
{
T 46900 42000 5 8 0 0 270 0 1
device=none
}
N 46700 43000 46700 42000 4
{
T 46700 42400 6 10 1 1 0 0 1
netname=BUS_D13
}
C 46700 42000 1 270 0 busripper-1.sym
{
T 47100 42000 5 8 0 0 270 0 1
device=none
}
N 46900 43000 46900 42000 4
{
T 46900 42600 6 10 1 1 0 0 1
netname=BUS_D12
}
C 46900 42000 1 270 0 busripper-1.sym
{
T 47300 42000 5 8 0 0 270 0 1
device=none
}
N 47500 43000 47500 42000 4
{
T 47500 42000 6 10 1 1 0 0 1
netname=BUS_D11
}
C 47500 42000 1 270 0 busripper-1.sym
{
T 47900 42000 5 8 0 0 270 0 1
device=none
}
N 47700 43000 47700 42000 4
{
T 47700 42200 6 10 1 1 0 0 1
netname=BUS_D10
}
C 47700 42000 1 270 0 busripper-1.sym
{
T 48100 42000 5 8 0 0 270 0 1
device=none
}
N 47900 43000 47900 42000 4
{
T 47900 42400 6 10 1 1 0 0 1
netname=BUS_D9
}
C 47900 42000 1 270 0 busripper-1.sym
{
T 48300 42000 5 8 0 0 270 0 1
device=none
}
N 48100 43000 48100 42000 4
{
T 48100 42600 6 10 1 1 0 0 1
netname=BUS_D8
}
C 48100 42000 1 270 0 busripper-1.sym
{
T 48500 42000 5 8 0 0 270 0 1
device=none
}
N 48900 43000 48900 42000 4
{
T 48900 42000 6 10 1 1 0 0 1
netname=BUS_D7
}
C 48900 42000 1 270 0 busripper-1.sym
{
T 49300 42000 5 8 0 0 270 0 1
device=none
}
N 49100 43000 49100 42000 4
{
T 49100 42200 6 10 1 1 0 0 1
netname=BUS_D6
}
C 49100 42000 1 270 0 busripper-1.sym
{
T 49500 42000 5 8 0 0 270 0 1
device=none
}
N 49300 43000 49300 42000 4
{
T 49300 42400 6 10 1 1 0 0 1
netname=BUS_D5
}
C 49300 42000 1 270 0 busripper-1.sym
{
T 49700 42000 5 8 0 0 270 0 1
device=none
}
N 49500 43000 49500 42000 4
{
T 49500 42600 6 10 1 1 0 0 1
netname=BUS_D4
}
C 49500 42000 1 270 0 busripper-1.sym
{
T 49900 42000 5 8 0 0 270 0 1
device=none
}
N 50100 43000 50100 42000 4
{
T 50100 42000 6 10 1 1 0 0 1
netname=BUS_D3
}
C 50100 42000 1 270 0 busripper-1.sym
{
T 50500 42000 5 8 0 0 270 0 1
device=none
}
N 50300 43000 50300 42000 4
{
T 50300 42200 6 10 1 1 0 0 1
netname=BUS_D2
}
C 50300 42000 1 270 0 busripper-1.sym
{
T 50700 42000 5 8 0 0 270 0 1
device=none
}
N 50500 43000 50500 42000 4
{
T 50500 42400 6 10 1 1 0 0 1
netname=BUS_D1
}
C 50500 42000 1 270 0 busripper-1.sym
{
T 50900 42000 5 8 0 0 270 0 1
device=none
}
N 50700 43000 50700 42000 4
{
T 50700 42600 6 10 1 1 0 0 1
netname=BUS_D0
}
C 50700 42000 1 270 0 busripper-1.sym
{
T 51100 42000 5 8 0 0 270 0 1
device=none
}
C 56800 43300 1 90 0 74377-1.sym
{
T 54050 43600 5 10 0 0 90 0 1
device=74377
T 54700 44000 5 16 1 1 90 0 1
refdes=U285
T 53850 43600 5 10 0 0 90 0 1
footprint=DIP20
}
C 59400 43300 1 90 0 74377-1.sym
{
T 56650 43600 5 10 0 0 90 0 1
device=74377
T 57300 44000 5 16 1 1 90 0 1
refdes=U286
T 56450 43600 5 10 0 0 90 0 1
footprint=DIP20
}
C 43900 45600 1 0 0 7404-1.sym
{
T 44200 45800 5 10 1 1 0 1 1
refdes=U283B
T 44000 46600 5 10 0 0 0 0 1
device=7404
T 44000 48400 5 10 0 0 0 0 1
footprint=DIP14
T 44000 46400 5 10 0 0 0 0 1
value=74HC04BQ
T 43900 45600 5 10 0 0 0 0 1
slot=2
}
N 44900 45800 54100 45800 4
N 56400 43100 56400 43300 4
N 59000 43100 59000 43300 4
C 52800 42800 1 0 0 ipad-1.sym
{
T 52884 43021 5 10 0 1 0 0 1
device=IPAD
T 52800 42900 5 10 1 1 0 1 1
netlabel=CLK2
}
N 54300 42900 59200 42900 4
N 56600 42900 56600 43300 4
N 59200 42900 59200 43300 4
N 54600 43300 54600 42000 4
{
T 54600 42000 6 10 1 1 0 0 1
netname=BUS_D15
}
C 54600 42000 1 270 0 busripper-1.sym
{
T 55000 42000 5 8 0 0 270 0 1
device=none
}
N 54800 43300 54800 42000 4
{
T 54800 42200 6 10 1 1 0 0 1
netname=BUS_D14
}
C 54800 42000 1 270 0 busripper-1.sym
{
T 55200 42000 5 8 0 0 270 0 1
device=none
}
N 55000 43300 55000 42000 4
{
T 55000 42400 6 10 1 1 0 0 1
netname=BUS_D13
}
C 55000 42000 1 270 0 busripper-1.sym
{
T 55400 42000 5 8 0 0 270 0 1
device=none
}
N 55200 43300 55200 42000 4
{
T 55200 42600 6 10 1 1 0 0 1
netname=BUS_D12
}
C 55200 42000 1 270 0 busripper-1.sym
{
T 55600 42000 5 8 0 0 270 0 1
device=none
}
N 55400 43300 55400 42000 4
{
T 55400 42000 6 10 1 1 0 0 1
netname=BUS_D11
}
C 55400 42000 1 270 0 busripper-1.sym
{
T 55800 42000 5 8 0 0 270 0 1
device=none
}
N 55600 43300 55600 42000 4
{
T 55600 42200 6 10 1 1 0 0 1
netname=BUS_D10
}
C 55600 42000 1 270 0 busripper-1.sym
{
T 56000 42000 5 8 0 0 270 0 1
device=none
}
N 55800 43300 55800 42000 4
{
T 55800 42400 6 10 1 1 0 0 1
netname=BUS_D9
}
C 55800 42000 1 270 0 busripper-1.sym
{
T 56200 42000 5 8 0 0 270 0 1
device=none
}
N 56000 43300 56000 42000 4
{
T 56000 42600 6 10 1 1 0 0 1
netname=BUS_D8
}
C 56000 42000 1 270 0 busripper-1.sym
{
T 56400 42000 5 8 0 0 270 0 1
device=none
}
N 57200 43300 57200 42000 4
{
T 57200 42000 6 10 1 1 0 0 1
netname=BUS_D7
}
C 57200 42000 1 270 0 busripper-1.sym
{
T 57600 42000 5 8 0 0 270 0 1
device=none
}
N 57400 43300 57400 42000 4
{
T 57400 42200 6 10 1 1 0 0 1
netname=BUS_D6
}
C 57400 42000 1 270 0 busripper-1.sym
{
T 57800 42000 5 8 0 0 270 0 1
device=none
}
N 57600 43300 57600 42000 4
{
T 57600 42400 6 10 1 1 0 0 1
netname=BUS_D5
}
C 57600 42000 1 270 0 busripper-1.sym
{
T 58000 42000 5 8 0 0 270 0 1
device=none
}
N 57800 43300 57800 42000 4
{
T 57800 42600 6 10 1 1 0 0 1
netname=BUS_D4
}
C 57800 42000 1 270 0 busripper-1.sym
{
T 58200 42000 5 8 0 0 270 0 1
device=none
}
N 58000 43300 58000 42000 4
{
T 58000 42000 6 10 1 1 0 0 1
netname=BUS_D3
}
C 58000 42000 1 270 0 busripper-1.sym
{
T 58400 42000 5 8 0 0 270 0 1
device=none
}
N 58200 43300 58200 42000 4
{
T 58200 42200 6 10 1 1 0 0 1
netname=BUS_D2
}
C 58200 42000 1 270 0 busripper-1.sym
{
T 58600 42000 5 8 0 0 270 0 1
device=none
}
N 58400 43300 58400 42000 4
{
T 58400 42400 6 10 1 1 0 0 1
netname=BUS_D1
}
C 58400 42000 1 270 0 busripper-1.sym
{
T 58800 42000 5 8 0 0 270 0 1
device=none
}
N 58600 43300 58600 42000 4
{
T 58600 42600 6 10 1 1 0 0 1
netname=BUS_D0
}
C 58600 42000 1 270 0 busripper-1.sym
{
T 59000 42000 5 8 0 0 270 0 1
device=none
}
N 44900 45300 45100 45300 4
N 45100 45500 43300 45500 4
N 43700 45000 43700 45800 4
N 43500 45000 43500 45300 4
C 55900 53800 1 0 0 74157-2.sym
{
T 56000 56540 5 10 0 0 0 0 1
device=74157
T 56000 56340 5 10 0 0 0 0 1
footprint=SO16
T 56500 55700 5 16 1 1 0 0 1
refdes=U287
T 56000 56140 5 10 0 0 0 0 1
value=SN74HC157D
}
C 55900 51400 1 0 0 74157-2.sym
{
T 56000 54140 5 10 0 0 0 0 1
device=74157
T 56000 53940 5 10 0 0 0 0 1
footprint=SO16
T 56500 53300 5 16 1 1 0 0 1
refdes=U288
T 56000 53740 5 10 0 0 0 0 1
value=SN74HC157D
}
C 42100 53600 1 0 0 gnd-1.sym
C 55900 49000 1 0 0 74157-2.sym
{
T 56000 51740 5 10 0 0 0 0 1
device=74157
T 56000 51540 5 10 0 0 0 0 1
footprint=SO16
T 56500 50900 5 16 1 1 0 0 1
refdes=U289
T 56000 51340 5 10 0 0 0 0 1
value=SN74HC157D
}
C 55900 46600 1 0 0 74157-2.sym
{
T 56000 49340 5 10 0 0 0 0 1
device=74157
T 56000 49140 5 10 0 0 0 0 1
footprint=SO16
T 56500 48500 5 16 1 1 0 0 1
refdes=U290
T 56000 48940 5 10 0 0 0 0 1
value=SN74HC157D
}
C 55600 46300 1 0 0 gnd-1.sym
N 59000 43100 54100 43100 4
N 54100 43100 54100 47000 4
N 55700 46600 55700 54000 4
N 55700 46800 55900 46800 4
N 55700 49200 55900 49200 4
N 55700 51600 55900 51600 4
N 55700 54000 55900 54000 4
U 58400 46400 54400 46400 10 -1
N 58600 45300 58600 46200 4
{
T 58600 46000 6 10 1 1 0 0 1
netname=_M_X0
}
C 58600 46200 1 90 0 busripper-1.sym
{
T 58200 46200 5 8 0 0 90 0 1
device=none
}
N 58400 45300 58400 46200 4
{
T 58400 45800 6 10 1 1 0 0 1
netname=_M_X1
}
C 58400 46200 1 90 0 busripper-1.sym
{
T 58000 46200 5 8 0 0 90 0 1
device=none
}
N 58200 45300 58200 46200 4
{
T 58200 45600 6 10 1 1 0 0 1
netname=_M_X2
}
C 58200 46200 1 90 0 busripper-1.sym
{
T 57800 46200 5 8 0 0 90 0 1
device=none
}
N 58000 45300 58000 46200 4
{
T 58000 45400 6 10 1 1 0 0 1
netname=_M_X3
}
C 58000 46200 1 90 0 busripper-1.sym
{
T 57600 46200 5 8 0 0 90 0 1
device=none
}
N 57800 45300 57800 46200 4
{
T 57800 46000 6 10 1 1 0 0 1
netname=_M_X4
}
C 57800 46200 1 90 0 busripper-1.sym
{
T 57400 46200 5 8 0 0 90 0 1
device=none
}
N 57600 45300 57600 46200 4
{
T 57600 45800 6 10 1 1 0 0 1
netname=_M_X5
}
C 57600 46200 1 90 0 busripper-1.sym
{
T 57200 46200 5 8 0 0 90 0 1
device=none
}
N 57400 45300 57400 46200 4
{
T 57400 45600 6 10 1 1 0 0 1
netname=_M_X6
}
C 57400 46200 1 90 0 busripper-1.sym
{
T 57000 46200 5 8 0 0 90 0 1
device=none
}
N 57200 45300 57200 46200 4
{
T 57200 45400 6 10 1 1 0 0 1
netname=_M_X7
}
C 57200 46200 1 90 0 busripper-1.sym
{
T 56800 46200 5 8 0 0 90 0 1
device=none
}
N 56000 45300 56000 46200 4
{
T 56000 46000 6 10 1 1 0 0 1
netname=_M_X8
}
C 56000 46200 1 90 0 busripper-1.sym
{
T 55600 46200 5 8 0 0 90 0 1
device=none
}
N 55800 45300 55800 46200 4
{
T 55800 45800 6 10 1 1 0 0 1
netname=_M_X9
}
C 55800 46200 1 90 0 busripper-1.sym
{
T 55400 46200 5 8 0 0 90 0 1
device=none
}
N 55600 45300 55600 46200 4
{
T 55600 45600 6 10 1 1 0 0 1
netname=_M_X10
}
C 55600 46200 1 90 0 busripper-1.sym
{
T 55200 46200 5 8 0 0 90 0 1
device=none
}
N 55400 45300 55400 46200 4
{
T 55400 45400 6 10 1 1 0 0 1
netname=_M_X11
}
C 55400 46200 1 90 0 busripper-1.sym
{
T 55000 46200 5 8 0 0 90 0 1
device=none
}
N 55200 45300 55200 46200 4
{
T 55200 46000 6 10 1 1 0 0 1
netname=_M_X12
}
C 55200 46200 1 90 0 busripper-1.sym
{
T 54800 46200 5 8 0 0 90 0 1
device=none
}
N 55000 45300 55000 46200 4
{
T 55000 45800 6 10 1 1 0 0 1
netname=_M_X13
}
C 55000 46200 1 90 0 busripper-1.sym
{
T 54600 46200 5 8 0 0 90 0 1
device=none
}
N 54800 45300 54800 46200 4
{
T 54800 45600 6 10 1 1 0 0 1
netname=_M_X14
}
C 54800 46200 1 90 0 busripper-1.sym
{
T 54400 46200 5 8 0 0 90 0 1
device=none
}
N 54600 45300 54600 46200 4
{
T 54600 45400 6 10 1 1 0 0 1
netname=_M_X15
}
C 54600 46200 1 90 0 busripper-1.sym
{
T 54200 46200 5 8 0 0 90 0 1
device=none
}
N 55500 47000 55500 54200 4
N 54100 47000 55900 47000 4
N 55900 49400 55500 49400 4
N 55900 51800 55500 51800 4
N 55500 54200 55900 54200 4
U 54400 55600 54400 46400 10 -1
N 55900 47200 54600 47200 4
{
T 54600 47200 6 10 1 1 0 0 1
netname=EM_D0
}
C 54600 47200 1 180 0 busripper-1.sym
{
T 54600 46800 5 8 0 0 180 0 1
device=none
}
N 55900 47600 54600 47600 4
{
T 54600 47600 6 10 1 1 0 0 1
netname=EM_D1
}
C 54600 47600 1 180 0 busripper-1.sym
{
T 54600 47200 5 8 0 0 180 0 1
device=none
}
N 55900 48000 54600 48000 4
{
T 54600 48000 6 10 1 1 0 0 1
netname=EM_D2
}
C 54600 48000 1 180 0 busripper-1.sym
{
T 54600 47600 5 8 0 0 180 0 1
device=none
}
N 55900 48400 54600 48400 4
{
T 54600 48400 6 10 1 1 0 0 1
netname=EM_D3
}
C 54600 48400 1 180 0 busripper-1.sym
{
T 54600 48000 5 8 0 0 180 0 1
device=none
}
N 55900 49600 54600 49600 4
{
T 54600 49600 6 10 1 1 0 0 1
netname=EM_D4
}
N 55900 50000 54600 50000 4
{
T 54600 50000 6 10 1 1 0 0 1
netname=EM_D5
}
C 54600 50000 1 180 0 busripper-1.sym
{
T 54600 49600 5 8 0 0 180 0 1
device=none
}
N 55900 50400 54600 50400 4
{
T 54600 50400 6 10 1 1 0 0 1
netname=EM_D6
}
C 54600 50400 1 180 0 busripper-1.sym
{
T 54600 50000 5 8 0 0 180 0 1
device=none
}
N 55900 50800 54600 50800 4
{
T 54600 50800 6 10 1 1 0 0 1
netname=EM_D7
}
C 54600 50800 1 180 0 busripper-1.sym
{
T 54600 50400 5 8 0 0 180 0 1
device=none
}
C 54600 49600 1 180 0 busripper-1.sym
{
T 54600 49200 5 8 0 0 180 0 1
device=none
}
N 55900 52000 54600 52000 4
{
T 54600 52000 6 10 1 1 0 0 1
netname=EM_D8
}
N 55900 52400 54600 52400 4
{
T 54600 52400 6 10 1 1 0 0 1
netname=EM_D9
}
C 54600 52400 1 180 0 busripper-1.sym
{
T 54600 52000 5 8 0 0 180 0 1
device=none
}
N 55900 52800 54600 52800 4
{
T 54600 52800 6 10 1 1 0 0 1
netname=EM_D10
}
C 54600 52800 1 180 0 busripper-1.sym
{
T 54600 52400 5 8 0 0 180 0 1
device=none
}
N 55900 53200 54600 53200 4
{
T 54600 53200 6 10 1 1 0 0 1
netname=EM_D11
}
C 54600 53200 1 180 0 busripper-1.sym
{
T 54600 52800 5 8 0 0 180 0 1
device=none
}
C 54600 52000 1 180 0 busripper-1.sym
{
T 54600 51600 5 8 0 0 180 0 1
device=none
}
N 55900 54400 54600 54400 4
{
T 54600 54400 6 10 1 1 0 0 1
netname=EM_D12
}
N 55900 54800 54600 54800 4
{
T 54600 54800 6 10 1 1 0 0 1
netname=EM_D13
}
C 54600 54800 1 180 0 busripper-1.sym
{
T 54600 54400 5 8 0 0 180 0 1
device=none
}
N 55900 55200 54600 55200 4
{
T 54600 55200 6 10 1 1 0 0 1
netname=EM_D14
}
C 54600 55200 1 180 0 busripper-1.sym
{
T 54600 54800 5 8 0 0 180 0 1
device=none
}
N 55900 55600 54600 55600 4
{
T 54600 55600 6 10 1 1 0 0 1
netname=EM_D15
}
C 54600 55600 1 180 0 busripper-1.sym
{
T 54600 55200 5 8 0 0 180 0 1
device=none
}
C 54600 54400 1 180 0 busripper-1.sym
{
T 54600 54000 5 8 0 0 180 0 1
device=none
}
C 54600 47400 1 180 0 busripper-1.sym
{
T 54600 47000 5 8 0 0 180 0 1
device=none
}
N 55900 47400 54600 47400 4
{
T 54600 47400 6 10 1 1 0 0 1
netname=_M_X0
}
N 55900 47800 54600 47800 4
{
T 54600 47800 6 10 1 1 0 0 1
netname=_M_X1
}
C 54600 47800 1 180 0 busripper-1.sym
{
T 54600 47400 5 8 0 0 180 0 1
device=none
}
N 55900 48200 54600 48200 4
{
T 54600 48200 6 10 1 1 0 0 1
netname=_M_X2
}
C 54600 48200 1 180 0 busripper-1.sym
{
T 54600 47800 5 8 0 0 180 0 1
device=none
}
N 55900 48600 54600 48600 4
{
T 54600 48600 6 10 1 1 0 0 1
netname=_M_X3
}
C 54600 48600 1 180 0 busripper-1.sym
{
T 54600 48200 5 8 0 0 180 0 1
device=none
}
N 55900 51000 54600 51000 4
{
T 54600 51000 6 10 1 1 0 0 1
netname=_M_X7
}
C 54600 51000 1 180 0 busripper-1.sym
{
T 54600 50600 5 8 0 0 180 0 1
device=none
}
N 55900 50600 54600 50600 4
{
T 54600 50600 6 10 1 1 0 0 1
netname=_M_X6
}
N 55900 50200 54600 50200 4
{
T 54600 50200 6 10 1 1 0 0 1
netname=_M_X5
}
N 55900 49800 54600 49800 4
{
T 54600 49800 6 10 1 1 0 0 1
netname=_M_X4
}
C 54600 49800 1 180 0 busripper-1.sym
{
T 54600 49400 5 8 0 0 180 0 1
device=none
}
C 54600 50200 1 180 0 busripper-1.sym
{
T 54600 49800 5 8 0 0 180 0 1
device=none
}
C 54600 50600 1 180 0 busripper-1.sym
{
T 54600 50200 5 8 0 0 180 0 1
device=none
}
N 55900 53400 54600 53400 4
{
T 54600 53400 6 10 1 1 0 0 1
netname=_M_X11
}
C 54600 53400 1 180 0 busripper-1.sym
{
T 54600 53000 5 8 0 0 180 0 1
device=none
}
N 55900 53000 54600 53000 4
{
T 54600 53000 6 10 1 1 0 0 1
netname=_M_X10
}
N 55900 52600 54600 52600 4
{
T 54600 52600 6 10 1 1 0 0 1
netname=_M_X9
}
N 55900 52200 54600 52200 4
{
T 54600 52200 6 10 1 1 0 0 1
netname=_M_X8
}
C 54600 52200 1 180 0 busripper-1.sym
{
T 54600 51800 5 8 0 0 180 0 1
device=none
}
C 54600 52600 1 180 0 busripper-1.sym
{
T 54600 52200 5 8 0 0 180 0 1
device=none
}
C 54600 53000 1 180 0 busripper-1.sym
{
T 54600 52600 5 8 0 0 180 0 1
device=none
}
N 55900 55800 54600 55800 4
{
T 54600 55800 6 10 1 1 0 0 1
netname=_M_X15
}
C 54600 55800 1 180 0 busripper-1.sym
{
T 54600 55400 5 8 0 0 180 0 1
device=none
}
N 55900 55400 54600 55400 4
{
T 54600 55400 6 10 1 1 0 0 1
netname=_M_X14
}
N 55900 55000 54600 55000 4
{
T 54600 55000 6 10 1 1 0 0 1
netname=_M_X13
}
N 55900 54600 54600 54600 4
{
T 54600 54600 6 10 1 1 0 0 1
netname=_M_X12
}
C 54600 54600 1 180 0 busripper-1.sym
{
T 54600 54200 5 8 0 0 180 0 1
device=none
}
C 54600 55000 1 180 0 busripper-1.sym
{
T 54600 54600 5 8 0 0 180 0 1
device=none
}
C 54600 55400 1 180 0 busripper-1.sym
{
T 54600 55000 5 8 0 0 180 0 1
device=none
}
U 62800 46600 62800 55200 10 -1
N 61800 55400 62600 55400 4
{
T 62000 55400 6 10 1 1 0 0 1
netname=M_D15
}
C 62600 55400 1 270 0 busripper-1.sym
{
T 63000 55400 5 8 0 0 270 0 1
device=none
}
N 61800 55000 62600 55000 4
{
T 62000 55000 6 10 1 1 0 0 1
netname=M_D14
}
C 62600 55000 1 270 0 busripper-1.sym
{
T 63000 55000 5 8 0 0 270 0 1
device=none
}
N 61800 54600 62600 54600 4
{
T 62000 54600 6 10 1 1 0 0 1
netname=M_D13
}
C 62600 54600 1 270 0 busripper-1.sym
{
T 63000 54600 5 8 0 0 270 0 1
device=none
}
N 61800 54200 62600 54200 4
{
T 62000 54200 6 10 1 1 0 0 1
netname=M_D12
}
C 62600 54200 1 270 0 busripper-1.sym
{
T 63000 54200 5 8 0 0 270 0 1
device=none
}
N 61800 53000 62600 53000 4
{
T 62000 53000 6 10 1 1 0 0 1
netname=M_D11
}
C 62600 53000 1 270 0 busripper-1.sym
{
T 63000 53000 5 8 0 0 270 0 1
device=none
}
N 61800 52600 62600 52600 4
{
T 62000 52600 6 10 1 1 0 0 1
netname=M_D10
}
C 62600 52600 1 270 0 busripper-1.sym
{
T 63000 52600 5 8 0 0 270 0 1
device=none
}
N 61800 52200 62600 52200 4
{
T 62000 52200 6 10 1 1 0 0 1
netname=M_D9
}
C 62600 52200 1 270 0 busripper-1.sym
{
T 63000 52200 5 8 0 0 270 0 1
device=none
}
N 61800 51800 62600 51800 4
{
T 62000 51800 6 10 1 1 0 0 1
netname=M_D8
}
C 62600 51800 1 270 0 busripper-1.sym
{
T 63000 51800 5 8 0 0 270 0 1
device=none
}
N 61800 50600 62600 50600 4
{
T 62000 50600 6 10 1 1 0 0 1
netname=M_D7
}
C 62600 50600 1 270 0 busripper-1.sym
{
T 63000 50600 5 8 0 0 270 0 1
device=none
}
N 61800 50200 62600 50200 4
{
T 62000 50200 6 10 1 1 0 0 1
netname=M_D6
}
C 62600 50200 1 270 0 busripper-1.sym
{
T 63000 50200 5 8 0 0 270 0 1
device=none
}
N 61800 49800 62600 49800 4
{
T 62000 49800 6 10 1 1 0 0 1
netname=M_D5
}
C 62600 49800 1 270 0 busripper-1.sym
{
T 63000 49800 5 8 0 0 270 0 1
device=none
}
N 61800 49400 62600 49400 4
{
T 62000 49400 6 10 1 1 0 0 1
netname=M_D4
}
C 62600 49400 1 270 0 busripper-1.sym
{
T 63000 49400 5 8 0 0 270 0 1
device=none
}
N 61800 48200 62600 48200 4
{
T 62000 48200 6 10 1 1 0 0 1
netname=M_D3
}
C 62600 48200 1 270 0 busripper-1.sym
{
T 63000 48200 5 8 0 0 270 0 1
device=none
}
N 61800 47800 62600 47800 4
{
T 62000 47800 6 10 1 1 0 0 1
netname=M_D2
}
C 62600 47800 1 270 0 busripper-1.sym
{
T 63000 47800 5 8 0 0 270 0 1
device=none
}
N 61800 47400 62600 47400 4
{
T 62000 47400 6 10 1 1 0 0 1
netname=M_D1
}
C 62600 47400 1 270 0 busripper-1.sym
{
T 63000 47400 5 8 0 0 270 0 1
device=none
}
N 61800 47000 62600 47000 4
{
T 62000 47000 6 10 1 1 0 0 1
netname=M_D0
}
C 62600 47000 1 270 0 busripper-1.sym
{
T 63000 47000 5 8 0 0 270 0 1
device=none
}
C 59800 53600 1 0 0 74157-2.sym
{
T 59900 56340 5 10 0 0 0 0 1
device=74157
T 59900 56140 5 10 0 0 0 0 1
footprint=SO16
T 60400 55500 5 16 1 1 0 0 1
refdes=U337
T 59900 55940 5 10 0 0 0 0 1
value=SN74HC157D
}
C 59800 51200 1 0 0 74157-2.sym
{
T 59900 53940 5 10 0 0 0 0 1
device=74157
T 59900 53740 5 10 0 0 0 0 1
footprint=SO16
T 60400 53100 5 16 1 1 0 0 1
refdes=U338
T 59900 53540 5 10 0 0 0 0 1
value=SN74HC157D
}
C 59800 48800 1 0 0 74157-2.sym
{
T 59900 51540 5 10 0 0 0 0 1
device=74157
T 59900 51340 5 10 0 0 0 0 1
footprint=SO16
T 60400 50700 5 16 1 1 0 0 1
refdes=U339
T 59900 51140 5 10 0 0 0 0 1
value=SN74HC157D
}
C 59800 46400 1 0 0 74157-2.sym
{
T 59900 49140 5 10 0 0 0 0 1
device=74157
T 59900 48940 5 10 0 0 0 0 1
footprint=SO16
T 60400 48300 5 16 1 1 0 0 1
refdes=U340
T 59900 48740 5 10 0 0 0 0 1
value=SN74HC157D
}
C 59500 46300 1 0 0 gnd-1.sym
C 59500 45100 1 90 0 ipad-1.sym
{
T 59279 45184 5 10 0 1 90 0 1
device=IPAD
T 59400 45100 5 10 1 1 90 1 1
netlabel=MC_Ir
}
U 58400 56100 58400 47200 10 1
N 59800 47000 58600 47000 4
{
T 58600 47000 6 10 1 1 0 0 1
netname=EM_C0
}
C 58600 47000 1 90 0 busripper-1.sym
{
T 58200 47000 5 8 0 0 90 0 1
device=none
}
N 59800 47400 58600 47400 4
{
T 58600 47400 6 10 1 1 0 0 1
netname=EM_C1
}
C 58600 47400 1 90 0 busripper-1.sym
{
T 58200 47400 5 8 0 0 90 0 1
device=none
}
N 59800 47800 58600 47800 4
{
T 58600 47800 6 10 1 1 0 0 1
netname=EM_C2
}
C 58600 47800 1 90 0 busripper-1.sym
{
T 58200 47800 5 8 0 0 90 0 1
device=none
}
N 59800 48200 58600 48200 4
{
T 58600 48200 6 10 1 1 0 0 1
netname=EM_C3
}
C 58600 48200 1 90 0 busripper-1.sym
{
T 58200 48200 5 8 0 0 90 0 1
device=none
}
N 59800 50600 58600 50600 4
{
T 58600 50600 6 10 1 1 0 0 1
netname=EM_C7
}
C 58600 50600 1 90 0 busripper-1.sym
{
T 58200 50600 5 8 0 0 90 0 1
device=none
}
N 59800 50200 58600 50200 4
{
T 58600 50200 6 10 1 1 0 0 1
netname=EM_C6
}
N 59800 49800 58600 49800 4
{
T 58600 49800 6 10 1 1 0 0 1
netname=EM_C5
}
N 59800 49400 58600 49400 4
{
T 58600 49400 6 10 1 1 0 0 1
netname=EM_C4
}
C 58600 49400 1 90 0 busripper-1.sym
{
T 58200 49400 5 8 0 0 90 0 1
device=none
}
C 58600 49800 1 90 0 busripper-1.sym
{
T 58200 49800 5 8 0 0 90 0 1
device=none
}
C 58600 50200 1 90 0 busripper-1.sym
{
T 58200 50200 5 8 0 0 90 0 1
device=none
}
N 59800 53000 58600 53000 4
{
T 58600 53000 6 10 1 1 0 0 1
netname=EM_C11
}
C 58600 53000 1 90 0 busripper-1.sym
{
T 58200 53000 5 8 0 0 90 0 1
device=none
}
N 59800 52600 58600 52600 4
{
T 58600 52600 6 10 1 1 0 0 1
netname=EM_C10
}
N 59800 52200 58600 52200 4
{
T 58600 52200 6 10 1 1 0 0 1
netname=EM_C9
}
N 59800 51800 58600 51800 4
{
T 58600 51800 6 10 1 1 0 0 1
netname=EM_C8
}
C 58600 51800 1 90 0 busripper-1.sym
{
T 58200 51800 5 8 0 0 90 0 1
device=none
}
C 58600 52200 1 90 0 busripper-1.sym
{
T 58200 52200 5 8 0 0 90 0 1
device=none
}
C 58600 52600 1 90 0 busripper-1.sym
{
T 58200 52600 5 8 0 0 90 0 1
device=none
}
N 59800 55400 58600 55400 4
{
T 58600 55400 6 10 1 1 0 0 1
netname=EM_C15
}
C 58600 55400 1 90 0 busripper-1.sym
{
T 58200 55400 5 8 0 0 90 0 1
device=none
}
N 59800 55000 58600 55000 4
{
T 58600 55000 6 10 1 1 0 0 1
netname=EM_C14
}
N 59800 54600 58600 54600 4
{
T 58600 54600 6 10 1 1 0 0 1
netname=EM_C13
}
N 59800 54200 58600 54200 4
{
T 58600 54200 6 10 1 1 0 0 1
netname=EM_C12
}
C 58600 54200 1 90 0 busripper-1.sym
{
T 58200 54200 5 8 0 0 90 0 1
device=none
}
C 58600 54600 1 90 0 busripper-1.sym
{
T 58200 54600 5 8 0 0 90 0 1
device=none
}
C 58600 55000 1 90 0 busripper-1.sym
{
T 58200 55000 5 8 0 0 90 0 1
device=none
}
C 52600 56000 1 0 0 ipad-2.sym
{
T 52700 56200 5 10 0 1 0 0 1
device=IPAD
T 52600 56100 5 10 1 1 0 1 1
netlabel=EM_C[15:0]
}
N 59800 55600 57900 55600 4
N 59800 55200 57900 55200 4
N 59800 54800 57900 54800 4
N 59800 54400 57900 54400 4
N 59800 53200 57900 53200 4
N 59800 52800 57900 52800 4
N 59800 52400 57900 52400 4
N 59800 52000 57900 52000 4
N 59800 50800 57900 50800 4
N 59800 50400 57900 50400 4
N 59800 50000 57900 50000 4
N 59800 49600 57900 49600 4
N 59800 48400 57900 48400 4
N 59800 48000 57900 48000 4
N 59800 47600 57900 47600 4
N 59800 47200 57900 47200 4
N 59600 46600 59800 46600 4
N 59600 46600 59600 53800 4
N 59600 49000 59800 49000 4
N 59600 51400 59800 51400 4
N 59600 53800 59800 53800 4
N 59400 46600 59400 54000 4
N 59400 46800 59800 46800 4
N 59400 49200 59800 49200 4
N 59400 51600 59800 51600 4
N 59400 54000 59800 54000 4
U 54100 56100 58400 56100 10 0
