;;
;; calculates 3^9 and stores result back in memory
;;

; |@| 119 ($4=4CE3)

	.data
n:	.word	0x0003
p:	.word	0x0009
x:	.word	0x0000

	.text
start:	ldw	$1, n($0)
	ldw	$2, p($0)
	add	$4, $1, $0
	sub	$2, $2, 1
outter:	sub	$3, $1, 1
	add	$5, $4, $0
inner:	add	$4, $4, $5
	as.z	$3, $3, -1
	jmp	inner
	as.z	$2, $2, -1
	jmp	outter
	stw	x($0), $4
	jmp	0
