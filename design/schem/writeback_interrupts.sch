v 20110115 2
C 40000 40000 0 0 0 title-bordered-A2.sym
C 44300 53200 1 0 0 ipad-1.sym
{
T 44384 53421 5 10 0 1 0 0 1
device=IPAD
T 44300 53300 5 10 1 1 0 1 1
netlabel=MW_T
}
C 44300 52400 1 0 0 ipad-1.sym
{
T 44384 52621 5 10 0 1 0 0 1
device=IPAD
T 44300 52500 5 10 1 1 0 1 1
netlabel=MW_I
}
C 44300 52800 1 0 0 ipad-1.sym
{
T 44384 53021 5 10 0 1 0 0 1
device=IPAD
T 44300 52900 5 10 1 1 0 1 1
netlabel=MW_IE
}
C 49600 52000 1 0 0 ipad-2.sym
{
T 49700 52200 5 10 0 1 0 0 1
device=IPAD
T 49600 52100 5 10 1 1 0 1 1
netlabel=MW_PC[15:0]
}
C 50700 54800 1 0 0 ipad-2.sym
{
T 50800 55000 5 10 0 1 0 0 1
device=IPAD
T 50700 54900 5 10 1 1 0 1 1
netlabel=MW_Rd[3:0]
}
C 50700 52400 1 0 0 ipad-2.sym
{
T 50800 52600 5 10 0 1 0 0 1
device=IPAD
T 50700 52500 5 10 1 1 0 1 1
netlabel=MW_D[15:0]
}
C 47700 53300 1 0 0 opad-1.sym
{
T 48002 53518 5 10 0 1 0 0 1
device=OPAD
T 47900 53400 5 10 1 1 0 1 1
netlabel=I_T
}
C 57000 52000 1 0 0 opad-2.sym
{
T 57200 52200 5 10 0 1 0 0 1
device=OPAD
T 57200 52100 5 10 1 1 0 1 1
netlabel=I_D[15:0]
}
C 57000 54600 1 0 0 opad-2.sym
{
T 57200 54800 5 10 0 1 0 0 1
device=OPAD
T 57200 54700 5 10 1 1 0 1 1
netlabel=I_Rd[3:0]
}
C 46400 53000 1 0 0 7408-2.sym
{
T 46500 53800 5 10 0 0 0 0 1
device=7408
T 46600 53200 5 10 1 1 0 1 1
refdes=U323A
T 46500 55200 5 10 0 0 0 0 1
footprint=SO14
T 46500 53600 5 10 0 0 0 0 1
value=SN74HC08DE4
T 46400 53000 5 10 0 0 0 0 1
slot=1
}
C 46400 52400 1 0 0 7408-2.sym
{
T 46500 53200 5 10 0 0 0 0 1
device=7408
T 46600 52600 5 10 1 1 0 1 1
refdes=U323B
T 46500 54600 5 10 0 0 0 0 1
footprint=SO14
T 46500 53000 5 10 0 0 0 0 1
value=SN74HC08DE4
T 46400 52400 5 10 0 0 0 0 1
slot=2
}
C 48000 52700 1 0 0 7432-2.sym
{
T 48100 53200 5 10 0 0 0 0 1
device=7432
T 48200 52900 5 10 1 1 0 1 1
refdes=U324A
T 48100 54600 5 10 0 0 0 0 1
footprint=DIP14
T 48000 52700 5 10 0 0 0 0 1
slot=1
}
N 46100 52700 46400 52700 4
N 45800 52500 46400 52500 4
N 45800 53300 46400 53300 4
N 46100 52700 46100 53100 4
N 46100 53100 46400 53100 4
C 53500 42200 1 0 0 gnd-1.sym
C 53200 55000 1 0 0 vcc-1.sym
C 53800 52500 1 0 0 74157-2.sym
{
T 53900 55240 5 10 0 0 0 0 1
device=74157
T 53900 55040 5 10 0 0 0 0 1
footprint=SO16
T 54400 54400 5 16 1 1 0 0 1
refdes=U325
T 53900 54840 5 10 0 0 0 0 1
value=SN74HC157D
}
C 53800 49900 1 0 0 74157-2.sym
{
T 53900 52640 5 10 0 0 0 0 1
device=74157
T 53900 52440 5 10 0 0 0 0 1
footprint=SO16
T 54400 51800 5 16 1 1 0 0 1
refdes=U326
T 53900 52240 5 10 0 0 0 0 1
value=SN74HC157D
}
C 53800 47500 1 0 0 74157-2.sym
{
T 53900 50240 5 10 0 0 0 0 1
device=74157
T 53900 50040 5 10 0 0 0 0 1
footprint=SO16
T 54400 49400 5 16 1 1 0 0 1
refdes=U327
T 53900 49840 5 10 0 0 0 0 1
value=SN74HC157D
}
C 53800 45100 1 0 0 74157-2.sym
{
T 53900 47840 5 10 0 0 0 0 1
device=74157
T 53900 47640 5 10 0 0 0 0 1
footprint=SO16
T 54400 47000 5 16 1 1 0 0 1
refdes=U328
T 53900 47440 5 10 0 0 0 0 1
value=SN74HC157D
}
C 53800 42700 1 0 0 74157-2.sym
{
T 53900 45440 5 10 0 0 0 0 1
device=74157
T 53900 45240 5 10 0 0 0 0 1
footprint=SO16
T 54400 44600 5 16 1 1 0 0 1
refdes=U329
T 53900 45040 5 10 0 0 0 0 1
value=SN74HC157D
}
N 47400 53200 47700 53200 4
N 47700 53000 47700 53400 4
N 47700 53000 48000 53000 4
N 47400 52600 47700 52600 4
N 47700 52600 47700 52800 4
N 47700 52800 48000 52800 4
N 53800 52700 53600 52700 4
N 53600 42500 53600 53900 4
N 53800 42900 53600 42900 4
N 53800 45300 53600 45300 4
N 53800 47700 53600 47700 4
N 53800 50100 53600 50100 4
N 53800 52900 48900 52900 4
N 53400 43100 53400 52900 4
N 53400 50300 53800 50300 4
N 53400 47900 53800 47900 4
N 53400 45500 53800 45500 4
N 53400 43100 53800 43100 4
U 52200 54900 52200 53500 10 1
N 53800 53300 52400 53300 4
{
T 52400 53300 6 10 1 1 0 0 1
netname=MW_Rd0
}
C 52400 53300 1 90 0 busripper-1.sym
{
T 52000 53300 5 8 0 0 90 0 1
device=none
}
N 53800 53700 52400 53700 4
{
T 52400 53700 6 10 1 1 0 0 1
netname=MW_Rd1
}
C 52400 53700 1 90 0 busripper-1.sym
{
T 52000 53700 5 8 0 0 90 0 1
device=none
}
N 53800 54100 52400 54100 4
{
T 52400 54100 6 10 1 1 0 0 1
netname=MW_Rd2
}
C 52400 54100 1 90 0 busripper-1.sym
{
T 52000 54100 5 8 0 0 90 0 1
device=none
}
N 53800 54500 52400 54500 4
{
T 52400 54500 6 10 1 1 0 0 1
netname=MW_Rd3
}
C 52400 54500 1 90 0 busripper-1.sym
{
T 52000 54500 5 8 0 0 90 0 1
device=none
}
N 53800 51900 52400 51900 4
{
T 52400 51900 6 10 1 1 0 0 1
netname=MW_D15
}
C 52400 51900 1 90 0 busripper-1.sym
{
T 52000 51900 5 8 0 0 90 0 1
device=none
}
U 52200 52500 52200 43700 10 0
N 53800 51500 52400 51500 4
{
T 52400 51500 6 10 1 1 0 0 1
netname=MW_D14
}
C 52400 51500 1 90 0 busripper-1.sym
{
T 52000 51500 5 8 0 0 90 0 1
device=none
}
N 53800 51100 52400 51100 4
{
T 52400 51100 6 10 1 1 0 0 1
netname=MW_D13
}
C 52400 51100 1 90 0 busripper-1.sym
{
T 52000 51100 5 8 0 0 90 0 1
device=none
}
N 53800 50700 52400 50700 4
{
T 52400 50700 6 10 1 1 0 0 1
netname=MW_D12
}
C 52400 50700 1 90 0 busripper-1.sym
{
T 52000 50700 5 8 0 0 90 0 1
device=none
}
N 53800 49500 52400 49500 4
{
T 52400 49500 6 10 1 1 0 0 1
netname=MW_D11
}
N 53800 49100 52400 49100 4
{
T 52400 49100 6 10 1 1 0 0 1
netname=MW_D10
}
C 52400 49100 1 90 0 busripper-1.sym
{
T 52000 49100 5 8 0 0 90 0 1
device=none
}
N 53800 48700 52400 48700 4
{
T 52400 48700 6 10 1 1 0 0 1
netname=MW_D9
}
C 52400 48700 1 90 0 busripper-1.sym
{
T 52000 48700 5 8 0 0 90 0 1
device=none
}
N 53800 48300 52400 48300 4
{
T 52400 48300 6 10 1 1 0 0 1
netname=MW_D8
}
C 52400 48300 1 90 0 busripper-1.sym
{
T 52000 48300 5 8 0 0 90 0 1
device=none
}
C 52400 49500 1 90 0 busripper-1.sym
{
T 52000 49500 5 8 0 0 90 0 1
device=none
}
N 53800 47100 52400 47100 4
{
T 52400 47100 6 10 1 1 0 0 1
netname=MW_D7
}
N 53800 46700 52400 46700 4
{
T 52400 46700 6 10 1 1 0 0 1
netname=MW_D6
}
C 52400 46700 1 90 0 busripper-1.sym
{
T 52000 46700 5 8 0 0 90 0 1
device=none
}
N 53800 46300 52400 46300 4
{
T 52400 46300 6 10 1 1 0 0 1
netname=MW_D5
}
C 52400 46300 1 90 0 busripper-1.sym
{
T 52000 46300 5 8 0 0 90 0 1
device=none
}
N 53800 45900 52400 45900 4
{
T 52400 45900 6 10 1 1 0 0 1
netname=MW_D4
}
C 52400 45900 1 90 0 busripper-1.sym
{
T 52000 45900 5 8 0 0 90 0 1
device=none
}
C 52400 47100 1 90 0 busripper-1.sym
{
T 52000 47100 5 8 0 0 90 0 1
device=none
}
N 53800 44700 52400 44700 4
{
T 52400 44700 6 10 1 1 0 0 1
netname=MW_D3
}
N 53800 44300 52400 44300 4
{
T 52400 44300 6 10 1 1 0 0 1
netname=MW_D2
}
C 52400 44300 1 90 0 busripper-1.sym
{
T 52000 44300 5 8 0 0 90 0 1
device=none
}
N 53800 43900 52400 43900 4
{
T 52400 43900 6 10 1 1 0 0 1
netname=MW_D1
}
C 52400 43900 1 90 0 busripper-1.sym
{
T 52000 43900 5 8 0 0 90 0 1
device=none
}
N 53800 43500 52400 43500 4
{
T 52400 43500 6 10 1 1 0 0 1
netname=MW_D0
}
C 52400 43500 1 90 0 busripper-1.sym
{
T 52000 43500 5 8 0 0 90 0 1
device=none
}
C 52400 44700 1 90 0 busripper-1.sym
{
T 52000 44700 5 8 0 0 90 0 1
device=none
}
U 51100 52100 51100 43500 10 0
N 53800 50500 51300 50500 4
{
T 51300 50500 6 10 1 1 0 0 1
netname=MW_PC12
}
C 51300 50500 1 90 0 busripper-1.sym
{
T 50900 50500 5 8 0 0 90 0 1
device=none
}
C 51300 50900 1 90 0 busripper-1.sym
{
T 50900 50900 5 8 0 0 90 0 1
device=none
}
N 53800 50900 51300 50900 4
{
T 51300 50900 6 10 1 1 0 0 1
netname=MW_PC13
}
N 53800 51300 51300 51300 4
{
T 51300 51300 6 10 1 1 0 0 1
netname=MW_PC14
}
N 53800 51700 51300 51700 4
{
T 51300 51700 6 10 1 1 0 0 1
netname=MW_PC15
}
C 51300 51700 1 90 0 busripper-1.sym
{
T 50900 51700 5 8 0 0 90 0 1
device=none
}
C 51300 51300 1 90 0 busripper-1.sym
{
T 50900 51300 5 8 0 0 90 0 1
device=none
}
N 53800 48100 51300 48100 4
{
T 51300 48100 6 10 1 1 0 0 1
netname=MW_PC8
}
C 51300 48100 1 90 0 busripper-1.sym
{
T 50900 48100 5 8 0 0 90 0 1
device=none
}
C 51300 48500 1 90 0 busripper-1.sym
{
T 50900 48500 5 8 0 0 90 0 1
device=none
}
N 53800 48500 51300 48500 4
{
T 51300 48500 6 10 1 1 0 0 1
netname=MW_PC9
}
N 53800 48900 51300 48900 4
{
T 51300 48900 6 10 1 1 0 0 1
netname=MW_PC10
}
N 53800 49300 51300 49300 4
{
T 51300 49300 6 10 1 1 0 0 1
netname=MW_PC11
}
C 51300 49300 1 90 0 busripper-1.sym
{
T 50900 49300 5 8 0 0 90 0 1
device=none
}
C 51300 48900 1 90 0 busripper-1.sym
{
T 50900 48900 5 8 0 0 90 0 1
device=none
}
N 53800 45700 51300 45700 4
{
T 51300 45700 6 10 1 1 0 0 1
netname=MW_PC4
}
C 51300 45700 1 90 0 busripper-1.sym
{
T 50900 45700 5 8 0 0 90 0 1
device=none
}
C 51300 46100 1 90 0 busripper-1.sym
{
T 50900 46100 5 8 0 0 90 0 1
device=none
}
N 53800 46100 51300 46100 4
{
T 51300 46100 6 10 1 1 0 0 1
netname=MW_PC5
}
N 53800 46500 51300 46500 4
{
T 51300 46500 6 10 1 1 0 0 1
netname=MW_PC6
}
N 53800 46900 51300 46900 4
{
T 51300 46900 6 10 1 1 0 0 1
netname=MW_PC7
}
C 51300 46900 1 90 0 busripper-1.sym
{
T 50900 46900 5 8 0 0 90 0 1
device=none
}
C 51300 46500 1 90 0 busripper-1.sym
{
T 50900 46500 5 8 0 0 90 0 1
device=none
}
N 53800 43300 51300 43300 4
{
T 51300 43300 6 10 1 1 0 0 1
netname=MW_PC0
}
C 51300 43300 1 90 0 busripper-1.sym
{
T 50900 43300 5 8 0 0 90 0 1
device=none
}
C 51300 43700 1 90 0 busripper-1.sym
{
T 50900 43700 5 8 0 0 90 0 1
device=none
}
N 53800 43700 51300 43700 4
{
T 51300 43700 6 10 1 1 0 0 1
netname=MW_PC1
}
N 53800 44100 51300 44100 4
{
T 51300 44100 6 10 1 1 0 0 1
netname=MW_PC2
}
N 53800 44500 51300 44500 4
{
T 51300 44500 6 10 1 1 0 0 1
netname=MW_PC3
}
C 51300 44500 1 90 0 busripper-1.sym
{
T 50900 44500 5 8 0 0 90 0 1
device=none
}
C 51300 44100 1 90 0 busripper-1.sym
{
T 50900 44100 5 8 0 0 90 0 1
device=none
}
N 53400 53500 53400 55000 4
N 53400 54300 53800 54300 4
N 53400 53500 53800 53500 4
N 53600 53100 53800 53100 4
N 53600 53900 53800 53900 4
U 57000 54700 57000 53300 10 1
N 55800 53100 56800 53100 4
{
T 56300 53100 6 10 1 1 0 0 1
netname=I_Rd0
}
C 56800 53100 1 0 0 busripper-1.sym
{
T 56800 53500 5 8 0 0 0 0 1
device=none
}
N 55800 53500 56800 53500 4
{
T 56300 53500 6 10 1 1 0 0 1
netname=I_Rd1
}
C 56800 53500 1 0 0 busripper-1.sym
{
T 56800 53900 5 8 0 0 0 0 1
device=none
}
N 55800 53900 56800 53900 4
{
T 56300 53900 6 10 1 1 0 0 1
netname=I_Rd2
}
C 56800 53900 1 0 0 busripper-1.sym
{
T 56800 54300 5 8 0 0 0 0 1
device=none
}
N 55800 54300 56800 54300 4
{
T 56300 54300 6 10 1 1 0 0 1
netname=I_Rd3
}
C 56800 54300 1 0 0 busripper-1.sym
{
T 56800 54700 5 8 0 0 0 0 1
device=none
}
U 57000 52100 57000 43500 10 1
N 55800 50500 56800 50500 4
{
T 56300 50500 6 10 1 1 0 0 1
netname=I_D12
}
C 56800 50500 1 0 0 busripper-1.sym
{
T 56800 50900 5 8 0 0 0 0 1
device=none
}
C 56800 50900 1 0 0 busripper-1.sym
{
T 56800 51300 5 8 0 0 0 0 1
device=none
}
N 55800 50900 56800 50900 4
{
T 56300 50900 6 10 1 1 0 0 1
netname=I_D13
}
C 56800 51300 1 0 0 busripper-1.sym
{
T 56800 51700 5 8 0 0 0 0 1
device=none
}
N 55800 51300 56800 51300 4
{
T 56300 51300 6 10 1 1 0 0 1
netname=I_D14
}
C 56800 51700 1 0 0 busripper-1.sym
{
T 56800 52100 5 8 0 0 0 0 1
device=none
}
N 55800 51700 56800 51700 4
{
T 56300 51700 6 10 1 1 0 0 1
netname=I_D15
}
N 55800 48100 56800 48100 4
{
T 56300 48100 6 10 1 1 0 0 1
netname=I_D8
}
C 56800 48100 1 0 0 busripper-1.sym
{
T 56800 48500 5 8 0 0 0 0 1
device=none
}
C 56800 48500 1 0 0 busripper-1.sym
{
T 56800 48900 5 8 0 0 0 0 1
device=none
}
N 55800 48500 56800 48500 4
{
T 56300 48500 6 10 1 1 0 0 1
netname=I_D9
}
C 56800 48900 1 0 0 busripper-1.sym
{
T 56800 49300 5 8 0 0 0 0 1
device=none
}
N 55800 48900 56800 48900 4
{
T 56300 48900 6 10 1 1 0 0 1
netname=I_D10
}
C 56800 49300 1 0 0 busripper-1.sym
{
T 56800 49700 5 8 0 0 0 0 1
device=none
}
N 55800 49300 56800 49300 4
{
T 56300 49300 6 10 1 1 0 0 1
netname=I_D11
}
N 55800 45700 56800 45700 4
{
T 56300 45700 6 10 1 1 0 0 1
netname=I_D4
}
C 56800 45700 1 0 0 busripper-1.sym
{
T 56800 46100 5 8 0 0 0 0 1
device=none
}
C 56800 46100 1 0 0 busripper-1.sym
{
T 56800 46500 5 8 0 0 0 0 1
device=none
}
N 55800 46100 56800 46100 4
{
T 56300 46100 6 10 1 1 0 0 1
netname=I_D5
}
C 56800 46500 1 0 0 busripper-1.sym
{
T 56800 46900 5 8 0 0 0 0 1
device=none
}
N 55800 46500 56800 46500 4
{
T 56300 46500 6 10 1 1 0 0 1
netname=I_D6
}
C 56800 46900 1 0 0 busripper-1.sym
{
T 56800 47300 5 8 0 0 0 0 1
device=none
}
N 55800 46900 56800 46900 4
{
T 56300 46900 6 10 1 1 0 0 1
netname=I_D7
}
N 55800 43300 56800 43300 4
{
T 56300 43300 6 10 1 1 0 0 1
netname=I_D0
}
C 56800 43300 1 0 0 busripper-1.sym
{
T 56800 43700 5 8 0 0 0 0 1
device=none
}
C 56800 43700 1 0 0 busripper-1.sym
{
T 56800 44100 5 8 0 0 0 0 1
device=none
}
N 55800 43700 56800 43700 4
{
T 56300 43700 6 10 1 1 0 0 1
netname=I_D1
}
C 56800 44100 1 0 0 busripper-1.sym
{
T 56800 44500 5 8 0 0 0 0 1
device=none
}
N 55800 44100 56800 44100 4
{
T 56300 44100 6 10 1 1 0 0 1
netname=I_D2
}
C 56800 44500 1 0 0 busripper-1.sym
{
T 56800 44900 5 8 0 0 0 0 1
device=none
}
N 55800 44500 56800 44500 4
{
T 56300 44500 6 10 1 1 0 0 1
netname=I_D3
}
N 45800 52900 46100 52900 4
C 49700 53300 1 0 0 opad-1.sym
{
T 50002 53518 5 10 0 1 0 0 1
device=OPAD
T 49900 53400 5 10 1 1 0 1 1
netlabel=I_I
}
N 49700 53400 49700 52900 4
