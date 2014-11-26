	.data
n:	.dw	0xABCD
m:	.dw	0x0000

	.text
	.ldi	$4, n			; $4 = &n
	.ldi	$6, m			; $6 = &m
	add	$5, $4, $4		; $5 = &n (byte address-able)
	add	$7, $6, $6		; $7 = &m (byte address-able)
	add	$3, $0, 2		; $3 = 2

1:	ldw	$1, 0($4)		; $1 = n
	stw	0($6), $1		;  m = n
	ldb	$2, (127/127-1)($7)	; $2 = m[15:8]
	ldb	$1, 1($7)		; $3 = m[7:0]
	stb	1($5), $2		; n[15:8] = m[7:0]
	stb	0($5), $1		; m[7:0] = m[15:0]
	as.z	$3, $3, -1		; $3 -= 1; loop until 0
	jmp	1b

	halt
