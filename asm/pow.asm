; calculates 3^9 and stores result back in memory
; note: hand coded loads/stores as labels aren't working yet
; also have to jump over the data section

;	.data
	jmp	start
n:	.dw	0x0003
p:	.dw	0x0009
x:	.dw	0x0000

;	.text
start:	ldw	$1, 1($0)
	ldw	$2, 2($0)
	add	$4, $1, $0
	sub	$2, $2, 1
outter:	sub	$3, $1, 1
	add	$5, $4, $0
inner:	add	$4, $4, $5
	sub	$3, $3, 1
	s.eq	$3, $0
	jmp	inner
	sub	$2, $2, 1
	s.eq	$2, $0
	jmp	outter
	stw	3($0), $4
	halt
