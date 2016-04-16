v 20110115 2
C 38500 40300 0 0 0 title-bordered-A1.sym
T 64500 41300 9 24 1 0 0 0 1
Prototype
C 44800 59200 1 0 0 diode-1.sym
{
T 45200 59800 5 10 0 0 0 0 1
device=DIODE
T 45100 59700 5 10 1 1 0 0 1
refdes=D1
T 44900 59000 5 10 1 1 0 0 1
value=1N4001
T 44800 59200 5 10 0 0 0 0 1
footprint=DIODE_LAY 500
}
C 45900 59400 1 270 0 capacitor-2.sym
{
T 46600 59200 5 10 0 0 270 0 1
device=POLARIZED_CAPACITOR
T 46400 59100 5 10 1 1 0 0 1
refdes=C1
T 46800 59200 5 10 0 0 270 0 1
symversion=0.1
T 46300 58900 5 10 1 1 0 0 1
value=100uF
T 45900 59400 5 10 0 0 0 0 1
footprint=1206
T 45900 59400 5 10 0 0 0 0 1
model=C3216X5R1A107M160AC
}
C 48300 59400 1 270 0 capacitor-2.sym
{
T 49000 59200 5 10 0 0 270 0 1
device=POLARIZED_CAPACITOR
T 48800 59100 5 10 1 1 0 0 1
refdes=C2
T 49200 59200 5 10 0 0 270 0 1
symversion=0.1
T 48700 58900 5 10 1 1 0 0 1
value=10uF
T 48300 59400 5 10 0 0 0 0 1
model=C1608X5R1A106M080AC
T 48300 59400 5 10 0 0 0 0 1
footprint=0603
}
N 44800 58500 48500 58500 4
N 45700 59400 46500 59400 4
C 46500 58800 1 0 0 lm7805-1.sym
{
T 48100 60100 5 10 0 0 0 0 1
device=7805
T 47900 59800 5 10 1 1 0 6 1
refdes=U50
T 46500 58800 5 10 0 0 0 0 1
value=LM7805CT
T 46500 58800 5 10 0 0 0 0 1
footprint=TO220W
}
N 47300 58800 47300 58500 4
N 48100 59400 51700 59400 4
C 42500 58100 1 0 0 BX0033.sym
{
T 42600 60440 5 10 0 0 0 0 1
device=BX0033
T 42600 60240 5 10 0 0 0 0 1
footprint=BX0033
T 42600 59600 5 16 1 1 0 0 1
refdes=U51
T 42600 60040 5 10 0 0 0 0 1
value=BX0033
}
N 44800 59200 44800 58500 4
C 51400 55500 1 0 0 vcc-1.sym
C 51500 59400 1 0 0 vcc-1.sym
C 48400 57300 1 0 0 gnd-1.sym
C 49800 58500 1 90 0 resistor-1.sym
{
T 49400 58800 5 10 0 0 90 0 1
device=RESISTOR
T 49500 58700 5 10 1 1 90 0 1
refdes=R39
T 49800 58500 5 10 0 0 0 0 1
value=150ohm
T 49800 58500 5 10 0 0 0 0 1
footprint=0603
}
C 49500 58500 1 270 0 led-1.sym
{
T 50100 57700 5 10 0 0 270 0 1
device=LED
T 49900 57700 5 10 1 1 270 0 1
refdes=LED39
T 50300 57700 5 10 0 0 270 0 1
symversion=0.1
T 49500 58500 5 10 0 0 0 0 1
value=LG L29K-G2J1-24-Z
T 49500 58500 5 10 0 0 0 0 1
footprint=0603
}
N 48500 58500 48500 57600 4
N 48500 57600 49700 57600 4
N 44500 59400 44800 59400 4
N 43700 59400 43400 59400 4
N 43400 59200 44800 59200 4
C 43700 59400 1 0 0 switch-spst-1.sym
{
T 44100 60100 5 10 0 0 0 0 1
device=SPST
T 44000 59700 5 10 1 1 0 0 1
refdes=S4
T 43700 59400 5 10 0 0 0 0 1
footprint=TO220ACS
T 43700 59400 5 10 0 0 0 0 1
value=TS02CQE
}
C 51900 52500 1 0 0 switch-dip8-1.sym
{
T 53300 55075 5 8 0 0 0 0 1
device=SWITCH_DIP8
T 52200 55250 5 10 1 1 0 0 1
refdes=U?
T 51900 52500 5 10 0 0 0 0 1
value=A6H-8101
T 51900 52500 5 10 0 0 0 0 1
footprint=SO16
}
C 51900 49500 1 0 0 switch-dip8-1.sym
{
T 53300 52075 5 8 0 0 0 0 1
device=SWITCH_DIP8
T 52200 52250 5 10 1 1 0 0 1
refdes=U?
T 51900 49500 5 10 0 0 0 0 1
value=A6H-8101
T 51900 49500 5 10 0 0 0 0 1
footprint=SO16
}
C 53300 49200 1 270 0 resistor-1.sym
{
T 53700 48900 5 10 0 0 270 0 1
device=RESISTOR
T 53600 49000 5 10 1 1 270 0 1
refdes=R38
T 53300 49200 5 10 0 0 180 0 1
value=150ohm
T 53300 49200 5 10 0 0 180 0 1
footprint=0603
}
C 53700 49200 1 270 0 resistor-1.sym
{
T 54100 48900 5 10 0 0 270 0 1
device=RESISTOR
T 54000 49000 5 10 1 1 270 0 1
refdes=R37
T 53700 49200 5 10 0 0 180 0 1
value=150ohm
T 53700 49200 5 10 0 0 180 0 1
footprint=0603
}
N 53400 49200 53400 50200 4
N 53800 49200 53800 49900 4
N 53800 46800 53800 47400 4
N 53400 47400 53400 46800 4
C 53600 48300 1 270 0 led-1.sym
{
T 54200 47500 5 10 0 0 270 0 1
device=LED
T 54000 47500 5 10 1 1 270 0 1
refdes=LED37
T 54400 47500 5 10 0 0 270 0 1
symversion=0.1
T 53600 48300 5 10 0 0 0 0 1
value=LG L29K-G2J1-24-Z
T 53600 48300 5 10 0 0 0 0 1
footprint=0603
}
T 53600 47500 5 10 1 1 270 0 1
refdes=LED38
C 53500 55600 1 90 0 resistor-1.sym
{
T 53100 55900 5 10 0 0 90 0 1
device=RESISTOR
T 53200 55800 5 10 1 1 90 0 1
refdes=R16
T 53500 55600 5 10 0 0 0 0 1
value=150ohm
T 53500 55600 5 10 0 0 0 0 1
footprint=0603
}
C 53900 55600 1 90 0 resistor-1.sym
{
T 53500 55900 5 10 0 0 90 0 1
device=RESISTOR
T 53600 55800 5 10 1 1 90 0 1
refdes=R15
T 53900 55600 5 10 0 0 0 0 1
value=150ohm
T 53900 55600 5 10 0 0 0 0 1
footprint=0603
}
C 54300 55600 1 90 0 resistor-1.sym
{
T 53900 55900 5 10 0 0 90 0 1
device=RESISTOR
T 54000 55800 5 10 1 1 90 0 1
refdes=R14
T 54300 55600 5 10 0 0 0 0 1
value=150ohm
T 54300 55600 5 10 0 0 0 0 1
footprint=0603
}
C 54700 55600 1 90 0 resistor-1.sym
{
T 54300 55900 5 10 0 0 90 0 1
device=RESISTOR
T 54400 55800 5 10 1 1 90 0 1
refdes=R13
T 54700 55600 5 10 0 0 0 0 1
value=150ohm
T 54700 55600 5 10 0 0 0 0 1
footprint=0603
}
C 55200 55600 1 90 0 resistor-1.sym
{
T 54800 55900 5 10 0 0 90 0 1
device=RESISTOR
T 54900 55800 5 10 1 1 90 0 1
refdes=R12
T 55200 55600 5 10 0 0 0 0 1
value=150ohm
T 55200 55600 5 10 0 0 0 0 1
footprint=0603
}
C 55600 55600 1 90 0 resistor-1.sym
{
T 55200 55900 5 10 0 0 90 0 1
device=RESISTOR
T 55300 55800 5 10 1 1 90 0 1
refdes=R11
T 55600 55600 5 10 0 0 0 0 1
value=150ohm
T 55600 55600 5 10 0 0 0 0 1
footprint=0603
}
C 56000 55600 1 90 0 resistor-1.sym
{
T 55600 55900 5 10 0 0 90 0 1
device=RESISTOR
T 55700 55800 5 10 1 1 90 0 1
refdes=R10
T 56000 55600 5 10 0 0 0 0 1
value=150ohm
T 56000 55600 5 10 0 0 0 0 1
footprint=0603
}
C 56400 55600 1 90 0 resistor-1.sym
{
T 56000 55900 5 10 0 0 90 0 1
device=RESISTOR
T 56100 55800 5 10 1 1 90 0 1
refdes=R9
T 56400 55600 5 10 0 0 0 0 1
value=150ohm
T 56400 55600 5 10 0 0 0 0 1
footprint=0603
}
N 53400 57400 53400 57900 4
N 56300 57400 56300 57900 4
N 55900 57400 55900 57900 4
N 55500 57400 55500 57900 4
N 55100 57400 55100 57900 4
N 54600 57400 54600 57900 4
N 54200 57400 54200 57900 4
N 53800 57400 53800 57900 4
C 54000 56500 1 90 0 led-1.sym
{
T 53400 57300 5 10 0 0 90 0 1
device=LED
T 53600 57300 5 10 1 1 90 0 1
refdes=LED15
T 53200 57300 5 10 0 0 90 0 1
symversion=0.1
T 54000 56500 5 10 0 0 180 0 1
value=LG L29K-G2J1-24-Z
T 54000 56500 5 10 0 0 180 0 1
footprint=0603
}
C 54400 56500 1 90 0 led-1.sym
{
T 53800 57300 5 10 0 0 90 0 1
device=LED
T 54000 57300 5 10 1 1 90 0 1
refdes=LED14
T 53600 57300 5 10 0 0 90 0 1
symversion=0.1
T 54400 56500 5 10 0 0 180 0 1
value=LG L29K-G2J1-24-Z
T 54400 56500 5 10 0 0 180 0 1
footprint=0603
}
C 54800 56500 1 90 0 led-1.sym
{
T 54200 57300 5 10 0 0 90 0 1
device=LED
T 54400 57300 5 10 1 1 90 0 1
refdes=LED13
T 54000 57300 5 10 0 0 90 0 1
symversion=0.1
T 54800 56500 5 10 0 0 180 0 1
value=LG L29K-G2J1-24-Z
T 54800 56500 5 10 0 0 180 0 1
footprint=0603
}
C 55300 56500 1 90 0 led-1.sym
{
T 54700 57300 5 10 0 0 90 0 1
device=LED
T 54900 57300 5 10 1 1 90 0 1
refdes=LED12
T 54500 57300 5 10 0 0 90 0 1
symversion=0.1
T 55300 56500 5 10 0 0 180 0 1
value=LG L29K-G2J1-24-Z
T 55300 56500 5 10 0 0 180 0 1
footprint=0603
}
C 55700 56500 1 90 0 led-1.sym
{
T 55100 57300 5 10 0 0 90 0 1
device=LED
T 55300 57300 5 10 1 1 90 0 1
refdes=LED11
T 54900 57300 5 10 0 0 90 0 1
symversion=0.1
T 55700 56500 5 10 0 0 180 0 1
value=LG L29K-G2J1-24-Z
T 55700 56500 5 10 0 0 180 0 1
footprint=0603
}
C 56100 56500 1 90 0 led-1.sym
{
T 55500 57300 5 10 0 0 90 0 1
device=LED
T 55700 57300 5 10 1 1 90 0 1
refdes=LED10
T 55300 57300 5 10 0 0 90 0 1
symversion=0.1
T 56100 56500 5 10 0 0 180 0 1
value=LG L29K-G2J1-24-Z
T 56100 56500 5 10 0 0 180 0 1
footprint=0603
}
C 56500 56500 1 90 0 led-1.sym
{
T 55900 57300 5 10 0 0 90 0 1
device=LED
T 56100 57300 5 10 1 1 90 0 1
refdes=LED9
T 55700 57300 5 10 0 0 90 0 1
symversion=0.1
T 56500 56500 5 10 0 0 180 0 1
value=LG L29K-G2J1-24-Z
T 56500 56500 5 10 0 0 180 0 1
footprint=0603
}
T 56600 55800 5 10 1 1 90 0 1
refdes=R8
T 53200 57300 5 10 1 1 90 0 1
refdes=LED16
T 56600 57300 5 10 1 1 90 0 1
refdes=LED8
C 63000 55100 1 0 0 resistor-1.sym
{
T 63300 55500 5 10 0 0 0 0 1
device=RESISTOR
T 63200 55400 5 10 1 1 0 0 1
refdes=R32
T 63000 55100 5 10 0 0 270 0 1
value=150ohm
T 63000 55100 5 10 0 0 270 0 1
footprint=0603
}
C 63000 54700 1 0 0 resistor-1.sym
{
T 63300 55100 5 10 0 0 0 0 1
device=RESISTOR
T 63200 55000 5 10 1 1 0 0 1
refdes=R31
T 63000 54700 5 10 0 0 270 0 1
value=150ohm
T 63000 54700 5 10 0 0 270 0 1
footprint=0603
}
C 63000 54300 1 0 0 resistor-1.sym
{
T 63300 54700 5 10 0 0 0 0 1
device=RESISTOR
T 63200 54600 5 10 1 1 0 0 1
refdes=R30
T 63000 54300 5 10 0 0 270 0 1
value=150ohm
T 63000 54300 5 10 0 0 270 0 1
footprint=0603
}
C 63000 53900 1 0 0 resistor-1.sym
{
T 63300 54300 5 10 0 0 0 0 1
device=RESISTOR
T 63200 54200 5 10 1 1 0 0 1
refdes=R29
T 63000 53900 5 10 0 0 270 0 1
value=150ohm
T 63000 53900 5 10 0 0 270 0 1
footprint=0603
}
C 63000 53400 1 0 0 resistor-1.sym
{
T 63300 53800 5 10 0 0 0 0 1
device=RESISTOR
T 63200 53700 5 10 1 1 0 0 1
refdes=R28
T 63000 53400 5 10 0 0 270 0 1
value=150ohm
T 63000 53400 5 10 0 0 270 0 1
footprint=0603
}
C 63000 53000 1 0 0 resistor-1.sym
{
T 63300 53400 5 10 0 0 0 0 1
device=RESISTOR
T 63200 53300 5 10 1 1 0 0 1
refdes=R27
T 63000 53000 5 10 0 0 270 0 1
value=150ohm
T 63000 53000 5 10 0 0 270 0 1
footprint=0603
}
C 63000 52600 1 0 0 resistor-1.sym
{
T 63300 53000 5 10 0 0 0 0 1
device=RESISTOR
T 63200 52900 5 10 1 1 0 0 1
refdes=R26
T 63000 52600 5 10 0 0 270 0 1
value=150ohm
T 63000 52600 5 10 0 0 270 0 1
footprint=0603
}
C 63000 52200 1 0 0 resistor-1.sym
{
T 63300 52600 5 10 0 0 0 0 1
device=RESISTOR
T 63200 52500 5 10 1 1 0 0 1
refdes=R25
T 63000 52200 5 10 0 0 270 0 1
value=150ohm
T 63000 52200 5 10 0 0 270 0 1
footprint=0603
}
N 64800 55200 65300 55200 4
N 64800 52300 65300 52300 4
N 64800 52700 65300 52700 4
N 64800 53100 65300 53100 4
N 64800 53500 65300 53500 4
N 64800 54000 65300 54000 4
N 64800 54400 65300 54400 4
N 64800 54800 65300 54800 4
C 63900 55000 1 0 0 led-1.sym
{
T 64700 55600 5 10 0 0 0 0 1
device=LED
T 64700 55400 5 10 1 1 0 0 1
refdes=LED32
T 64700 55800 5 10 0 0 0 0 1
symversion=0.1
T 63900 55000 5 10 0 0 90 0 1
value=LG L29K-G2J1-24-Z
T 63900 55000 5 10 0 0 90 0 1
footprint=0603
}
C 63900 54600 1 0 0 led-1.sym
{
T 64700 55200 5 10 0 0 0 0 1
device=LED
T 64700 55000 5 10 1 1 0 0 1
refdes=LED31
T 64700 55400 5 10 0 0 0 0 1
symversion=0.1
T 63900 54600 5 10 0 0 90 0 1
value=LG L29K-G2J1-24-Z
T 63900 54600 5 10 0 0 90 0 1
footprint=0603
}
C 63900 54200 1 0 0 led-1.sym
{
T 64700 54800 5 10 0 0 0 0 1
device=LED
T 64700 54600 5 10 1 1 0 0 1
refdes=LED30
T 64700 55000 5 10 0 0 0 0 1
symversion=0.1
T 63900 54200 5 10 0 0 90 0 1
value=LG L29K-G2J1-24-Z
T 63900 54200 5 10 0 0 90 0 1
footprint=0603
}
C 63900 53800 1 0 0 led-1.sym
{
T 64700 54400 5 10 0 0 0 0 1
device=LED
T 64700 54200 5 10 1 1 0 0 1
refdes=LED29
T 64700 54600 5 10 0 0 0 0 1
symversion=0.1
T 63900 53800 5 10 0 0 90 0 1
value=LG L29K-G2J1-24-Z
T 63900 53800 5 10 0 0 90 0 1
footprint=0603
}
C 63900 53300 1 0 0 led-1.sym
{
T 64700 53900 5 10 0 0 0 0 1
device=LED
T 64700 53700 5 10 1 1 0 0 1
refdes=LED28
T 64700 54100 5 10 0 0 0 0 1
symversion=0.1
T 63900 53300 5 10 0 0 90 0 1
value=LG L29K-G2J1-24-Z
T 63900 53300 5 10 0 0 90 0 1
footprint=0603
}
C 63900 52900 1 0 0 led-1.sym
{
T 64700 53500 5 10 0 0 0 0 1
device=LED
T 64700 53300 5 10 1 1 0 0 1
refdes=LED27
T 64700 53700 5 10 0 0 0 0 1
symversion=0.1
T 63900 52900 5 10 0 0 90 0 1
value=LG L29K-G2J1-24-Z
T 63900 52900 5 10 0 0 90 0 1
footprint=0603
}
C 63900 52500 1 0 0 led-1.sym
{
T 64700 53100 5 10 0 0 0 0 1
device=LED
T 64700 52900 5 10 1 1 0 0 1
refdes=LED26
T 64700 53300 5 10 0 0 0 0 1
symversion=0.1
T 63900 52500 5 10 0 0 90 0 1
value=LG L29K-G2J1-24-Z
T 63900 52500 5 10 0 0 90 0 1
footprint=0603
}
C 63900 52100 1 0 0 led-1.sym
{
T 64700 52700 5 10 0 0 0 0 1
device=LED
T 64700 52500 5 10 1 1 0 0 1
refdes=LED25
T 64700 52900 5 10 0 0 0 0 1
symversion=0.1
T 63900 52100 5 10 0 0 90 0 1
value=LG L29K-G2J1-24-Z
T 63900 52100 5 10 0 0 90 0 1
footprint=0603
}
T 63200 52000 5 10 1 1 0 0 1
refdes=R24
T 64700 52000 5 10 1 1 0 0 1
refdes=LED24
C 53200 48300 1 270 0 led-1.sym
{
T 53800 47500 5 10 0 0 270 0 1
device=LED
T 53600 47500 5 10 1 1 270 0 1
refdes=LED37
T 54000 47500 5 10 0 0 270 0 1
symversion=0.1
T 53200 48300 5 10 0 0 0 0 1
value=LG L29K-G2J1-24-Z
T 53200 48300 5 10 0 0 0 0 1
footprint=0603
}
C 53600 56500 1 90 0 led-1.sym
{
T 53000 57300 5 10 0 0 90 0 1
device=LED
T 53200 57300 5 10 1 1 90 0 1
refdes=LED15
T 52800 57300 5 10 0 0 90 0 1
symversion=0.1
T 53600 56500 5 10 0 0 180 0 1
value=LG L29K-G2J1-24-Z
T 53600 56500 5 10 0 0 180 0 1
footprint=0603
}
U 57300 54800 57300 49600 10 -1
N 53200 55000 57100 55000 4
{
T 56800 55000 6 10 1 1 0 0 1
netname=A?
}
C 57100 55000 1 270 0 busripper-1.sym
{
T 57500 55000 6 10 0 0 270 0 1
device=none
}
N 53200 54700 57100 54700 4
{
T 56800 54700 6 10 1 1 0 0 1
netname=A?
}
C 57100 54700 1 270 0 busripper-1.sym
{
T 57500 54700 6 10 0 0 270 0 1
device=none
}
N 53200 54400 57100 54400 4
{
T 56800 54400 6 10 1 1 0 0 1
netname=A?
}
C 57100 54400 1 270 0 busripper-1.sym
{
T 57500 54400 6 10 0 0 270 0 1
device=none
}
N 53200 54100 57100 54100 4
{
T 56800 54100 6 10 1 1 0 0 1
netname=A?
}
C 57100 54100 1 270 0 busripper-1.sym
{
T 57500 54100 6 10 0 0 270 0 1
device=none
}
N 53200 53800 57100 53800 4
{
T 56800 53800 6 10 1 1 0 0 1
netname=B?
}
C 57100 53800 1 270 0 busripper-1.sym
{
T 57500 53800 6 10 0 0 270 0 1
device=none
}
C 57100 53500 1 270 0 busripper-1.sym
{
T 57500 53500 6 10 0 0 270 0 1
device=none
}
N 53200 53500 57100 53500 4
{
T 56800 53500 6 10 1 1 0 0 1
netname=B?
}
C 57100 53200 1 270 0 busripper-1.sym
{
T 57500 53200 6 10 0 0 270 0 1
device=none
}
N 53200 53200 57100 53200 4
{
T 56800 53200 6 10 1 1 0 0 1
netname=B?
}
C 57100 52900 1 270 0 busripper-1.sym
{
T 57500 52900 6 10 0 0 270 0 1
device=none
}
N 53200 52900 57100 52900 4
{
T 56800 52900 6 10 1 1 0 0 1
netname=B?
}
C 57100 50200 1 270 0 busripper-1.sym
{
T 57500 50200 5 8 0 0 270 0 1
device=none
}
N 53200 50200 57100 50200 4
{
T 56800 50200 6 10 1 1 0 0 1
netname=Op1
}
C 57100 49900 1 270 0 busripper-1.sym
{
T 57500 49900 5 8 0 0 270 0 1
device=none
}
N 53200 49900 57100 49900 4
{
T 56800 49900 6 10 1 1 0 0 1
netname=Op2
}
B 58300 51100 2200 1700 3 0 0 0 -1 -1 0 -1 -1 -1 -1 -1
T 59300 51900 9 10 1 0 0 0 1
ALU
U 58300 51900 57300 51900 10 0
U 61800 55000 61800 51900 10 -1
U 61800 51900 60500 51900 10 0
N 63000 55200 62000 55200 4
{
T 62000 55200 6 10 1 1 0 0 1
netname=A?
}
C 62000 55200 1 180 0 busripper-1.sym
{
T 62000 54800 5 8 0 0 180 0 1
device=none
}
N 63000 54800 62000 54800 4
{
T 62000 54800 6 10 1 1 0 0 1
netname=A?
}
C 62000 54800 1 180 0 busripper-1.sym
{
T 62000 54400 5 8 0 0 180 0 1
device=none
}
N 63000 54400 62000 54400 4
{
T 62000 54400 6 10 1 1 0 0 1
netname=A?
}
C 62000 54400 1 180 0 busripper-1.sym
{
T 62000 54000 5 8 0 0 180 0 1
device=none
}
N 63000 54000 62000 54000 4
{
T 62000 54000 6 10 1 1 0 0 1
netname=A?
}
C 62000 54000 1 180 0 busripper-1.sym
{
T 62000 53600 5 8 0 0 180 0 1
device=none
}
N 63000 53500 62000 53500 4
{
T 62000 53500 6 10 1 1 0 0 1
netname=B?
}
C 62000 53500 1 180 0 busripper-1.sym
{
T 62000 53100 5 8 0 0 180 0 1
device=none
}
N 63000 53100 62000 53100 4
{
T 62000 53100 6 10 1 1 0 0 1
netname=B?
}
C 62000 53100 1 180 0 busripper-1.sym
{
T 62000 52700 5 8 0 0 180 0 1
device=none
}
N 63000 52700 62000 52700 4
{
T 62000 52700 6 10 1 1 0 0 1
netname=B?
}
C 62000 52700 1 180 0 busripper-1.sym
{
T 62000 52300 5 8 0 0 180 0 1
device=none
}
N 63000 52300 62000 52300 4
{
T 62000 52300 6 10 1 1 0 0 1
netname=B?
}
C 62000 52300 1 180 0 busripper-1.sym
{
T 62000 51900 5 8 0 0 180 0 1
device=none
}
N 51900 55000 51600 55000 4
N 51600 49900 51600 55500 4
N 51900 54700 51600 54700 4
N 51600 54400 51900 54400 4
N 51900 54100 51600 54100 4
N 51900 53800 51600 53800 4
N 51900 53500 51600 53500 4
N 51900 53200 51600 53200 4
N 51900 52900 51600 52900 4
N 51900 50200 51600 50200 4
N 51900 49900 51600 49900 4
N 53400 55600 53400 55000 4
N 53800 55600 53800 54700 4
N 54200 55600 54200 54400 4
N 54600 55600 54600 54100 4
N 55100 55600 55100 53800 4
N 55500 55600 55500 53500 4
N 55900 55600 55900 53200 4
N 56300 55600 56300 52900 4
