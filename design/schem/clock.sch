v 20110115 2
C 40000 40000 0 0 0 title-bordered-A2.sym
C 52000 48600 1 0 0 7474-1.sym
{
T 52300 51550 5 10 0 0 0 0 1
device=7474
T 52800 49200 5 16 1 1 0 0 1
refdes=U1A
T 52300 51750 5 10 0 0 0 0 1
footprint=DIP16
T 52000 48600 5 10 0 0 0 0 1
slot=1
}
C 49200 48600 1 0 0 7474-1.sym
{
T 49500 51550 5 10 0 0 0 0 1
device=7474
T 50000 49200 5 16 1 1 0 0 1
refdes=U1B
T 49500 51750 5 10 0 0 0 0 1
footprint=DIP16
T 49200 48600 5 10 0 0 0 0 1
slot=2
}
C 48800 50400 1 0 0 vcc-1.sym
N 49000 50400 49000 49400 4
N 49000 49400 49200 49400 4
N 49000 50000 54200 50000 4
N 54200 50000 54200 49400 4
N 51200 49400 52000 49400 4
N 51600 49400 51600 50000 4
N 51200 49200 52000 49200 4
N 54000 49200 54400 49200 4
N 54000 49000 54600 49000 4
N 54400 48400 54400 49000 4
N 48800 48400 48800 49200 4
N 48800 49200 49200 49200 4
C 47300 47900 1 0 0 ipad-1.sym
{
T 47384 48121 5 10 0 1 0 0 1
device=IPAD
T 47300 48000 5 10 1 1 0 1 1
netlabel=_CLK
T 47384 48121 5 10 0 1 0 0 1
refdes=_CLK0
T 47384 48121 5 10 0 1 0 0 1
net=_CLK:1
}
C 55800 48200 1 0 0 opad-1.sym
{
T 56102 48418 5 10 0 1 0 0 1
device=OPAD
T 56000 48300 5 10 1 1 0 1 1
netlabel=CLK2
T 56102 48418 5 10 0 1 0 0 1
refdes=CLK12
T 56102 48418 5 10 0 1 0 0 1
net=CLK1:1
}
N 51600 48200 51600 49200 4
N 52000 49000 51800 49000 4
N 51800 49000 51800 48000 4
N 48800 48000 51800 48000 4
N 49200 49000 49000 49000 4
N 49000 49000 49000 48000 4
N 54000 49400 54200 49400 4
L 57800 54000 58200 54000 3 0 0 0 -1 -1
L 58200 54000 58200 53800 3 0 0 0 -1 -1
L 58200 53800 58600 53800 3 0 0 0 -1 -1
L 58600 53800 58600 54000 3 0 0 0 -1 -1
L 58600 54000 59000 54000 3 0 0 0 -1 -1
L 59000 54000 59000 53800 3 0 0 0 -1 -1
L 59000 53800 59400 53800 3 0 0 0 -1 -1
L 57800 53500 58200 53500 3 0 0 0 -1 -1
L 58200 53500 58200 53700 3 0 0 0 -1 -1
L 58200 53700 58600 53700 3 0 0 0 -1 -1
L 58600 53700 58600 53500 3 0 0 0 -1 -1
L 58600 53500 59000 53500 3 0 0 0 -1 -1
L 59000 53500 59000 53700 3 0 0 0 -1 -1
L 59000 53700 59400 53700 3 0 0 0 -1 -1
T 57200 53800 9 10 1 0 0 0 1
CLK0
T 57200 53500 9 10 1 0 0 0 1
CLK1
T 57200 53200 9 10 1 0 0 0 1
CLK2
T 57200 52900 9 10 1 0 0 0 1
CLK3
L 58000 53200 58000 53400 3 0 0 0 -1 -1
L 58000 53400 58200 53400 3 0 0 0 -1 -1
L 58200 53400 58200 53200 3 0 0 0 -1 -1
L 58200 53200 58800 53200 3 0 0 0 -1 -1
L 58800 53200 58800 53400 3 0 0 0 -1 -1
L 58800 53400 59000 53400 3 0 0 0 -1 -1
L 59000 53400 59000 53200 3 0 0 0 -1 -1
L 59000 53200 59600 53200 3 0 0 0 -1 -1
L 57800 52900 58400 52900 3 0 0 0 -1 -1
L 58400 52900 58400 53100 3 0 0 0 -1 -1
L 58400 53100 58600 53100 3 0 0 0 -1 -1
L 58600 53100 58600 52900 3 0 0 0 -1 -1
L 58600 52900 59200 52900 3 0 0 0 -1 -1
L 59200 52900 59200 53100 3 0 0 0 -1 -1
L 59200 53100 59400 53100 3 0 0 0 -1 -1
L 59400 53100 59400 52900 3 0 0 0 -1 -1
L 59400 52900 59600 52900 3 0 0 0 -1 -1
L 59400 53800 59400 54000 3 0 0 0 -1 -1
L 59400 54000 59800 54000 3 0 0 0 -1 -1
L 59800 54000 59800 53800 3 0 0 0 -1 -1
L 59800 53800 60200 53800 3 0 0 0 -1 -1
L 59400 53700 59400 53500 3 0 0 0 -1 -1
L 59400 53500 59800 53500 3 0 0 0 -1 -1
L 59800 53500 59800 53700 3 0 0 0 -1 -1
L 59800 53700 60200 53700 3 0 0 0 -1 -1
L 59600 53200 59600 53400 3 0 0 0 -1 -1
L 59600 53400 59800 53400 3 0 0 0 -1 -1
L 59800 53400 59800 53200 3 0 0 0 -1 -1
L 59800 53200 60200 53200 3 0 0 0 -1 -1
L 59600 52900 60000 52900 3 0 0 0 -1 -1
L 60000 52900 60000 53100 3 0 0 0 -1 -1
L 60000 53100 60200 53100 3 0 0 0 -1 -1
L 60200 53100 60200 52900 3 0 0 0 -1 -1
C 54600 48100 1 0 0 7408-2.sym
{
T 54700 48900 5 10 0 0 0 0 1
device=7408
T 54800 48300 5 10 1 1 0 1 1
refdes=U2A
T 54700 50300 5 10 0 0 0 0 1
footprint=SO14
T 54700 48700 5 10 0 0 0 0 1
value=SN74HC08DE4
T 54600 48100 5 10 0 0 0 0 1
slot=1
}
C 54600 49900 1 0 0 7408-2.sym
{
T 54700 50700 5 10 0 0 0 0 1
device=7408
T 54800 50100 5 10 1 1 0 1 1
refdes=U2B
T 54700 52100 5 10 0 0 0 0 1
footprint=SO14
T 54700 50500 5 10 0 0 0 0 1
value=SN74HC08DE4
T 54600 49900 5 10 0 0 0 0 1
slot=2
}
N 48800 48400 54600 48400 4
N 54600 48200 51600 48200 4
N 55800 48300 55600 48300 4
C 55800 50000 1 0 0 opad-1.sym
{
T 56102 50218 5 10 0 1 0 0 1
device=OPAD
T 56000 50100 5 10 1 1 0 1 1
netlabel=CLK3
T 56102 50218 5 10 0 1 0 0 1
refdes=CLK01
T 56102 50218 5 10 0 1 0 0 1
net=CLK0:1
}
N 51400 50200 54600 50200 4
N 54400 49200 54400 50000 4
N 54400 50000 54600 50000 4
N 55800 50100 55600 50100 4
C 55800 49400 1 0 0 opad-1.sym
{
T 56102 49618 5 10 0 1 0 0 1
device=OPAD
T 56000 49500 5 10 1 1 0 1 1
netlabel=CLK1
T 56102 49618 5 10 0 1 0 0 1
refdes=CLK01
T 56102 49618 5 10 0 1 0 0 1
net=CLK0:1
}
C 55800 48800 1 0 0 opad-1.sym
{
T 56102 49018 5 10 0 1 0 0 1
device=OPAD
T 56000 48900 5 10 1 1 0 1 1
netlabel=CLK0
T 56102 49018 5 10 0 1 0 0 1
refdes=CLK01
T 56102 49018 5 10 0 1 0 0 1
net=CLK0:1
}
C 54600 49300 1 0 0 7408-2.sym
{
T 54700 50100 5 10 0 0 0 0 1
device=7408
T 54800 49500 5 10 1 1 0 1 1
refdes=U2C
T 54700 51500 5 10 0 0 0 0 1
footprint=SO14
T 54700 49900 5 10 0 0 0 0 1
value=SN74HC08DE4
T 54600 49300 5 10 0 0 0 0 1
slot=3
}
C 54600 48700 1 0 0 7408-2.sym
{
T 54700 49500 5 10 0 0 0 0 1
device=7408
T 54800 48900 5 10 1 1 0 1 1
refdes=U2D
T 54700 50900 5 10 0 0 0 0 1
footprint=SO14
T 54700 49300 5 10 0 0 0 0 1
value=SN74HC08DE4
T 54600 48700 5 10 0 0 0 0 1
slot=4
}
N 54400 49000 54400 48800 4
N 54400 48800 54600 48800 4
N 54600 49400 54400 49400 4
N 54400 49600 54600 49600 4
N 55600 49500 55800 49500 4
N 55600 48900 55800 48900 4
L 57800 54200 57800 54300 3 0 0 0 -1 -1
L 57800 54300 60200 54300 3 0 0 0 -1 -1
L 58600 54200 58600 54300 3 0 0 0 -1 -1
L 59400 54200 59400 54300 3 0 0 0 -1 -1
L 60200 54200 60200 54300 3 0 0 0 -1 -1
L 58000 53200 57800 53200 3 0 0 0 -1 -1
N 51200 49000 51400 49000 4
N 51400 49000 51400 50200 4
L 57800 53800 57800 54000 3 0 0 0 -1 -1
L 57800 53700 57800 53500 3 0 0 0 -1 -1
L 60200 53700 60200 53500 3 0 0 0 -1 -1
L 60200 53800 60200 54000 3 0 0 0 -1 -1
