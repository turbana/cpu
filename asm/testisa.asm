;;
;; Test ISA
;;
;; After running $1 should equal 0xF00D
;;

	.data
n:	.dw	0xABCD
m:	.dw	0x0000
	.zero	32
sbp:

	.text
	.ldi	$4, n			; $4 = &n
	.ldi	$6, m			; $6 = &m
	add	$5, $0, 2		; $3 = 2

1:	ldw	$1, 0($4)		; $1 = n
	stw	0($6), $1		;  m = n
	shl	$2, $1, 8		; $2 = n << 8
	shr	$3, $1, 8		; $3 = n >> 8
	or	$1, $3, $2		; $1 = $3 | $2
	stw	0($4), $1		;  n = $1
	as.z	$5, $5, -1		; $3 -= 1; loop until 0
	jmp	1b

	ldw	$1, 0($4)		; $1 = n (0xABCD)
	ldw	$2, 0($6)		; $2 = m (0xCDBA)
	sub	$3, $0, -4		; $3 = 4
1:	shl	$1, $1, 1		; $1 <<= 1
	shr	$2, $2, 1		; $2 >>= 1
	sub	$3, $3, 1		; $3 -= 1
	s.eq	$3, $0			; loop until $3 == 0
	jmp	1b

	or	$3, $1, $2		; $3 = $1 | $2 (0xBCD0 | 0x0CDA == 0xBCDA)
	stw	$0($4), $3		;  n = $3
	ldw	$1, $0($4)		; $1 = n
	ldw	$2, $0($6)		; $2 = m
	xor	$3, $1, $2		; $3 = 0xBCDA ^ 0xCDAB = 0x7171
	shl	$2, $3, 1		; $2 = $3 << 1 = 0xE2E2
	lui	$1, 0x80		; $1 = 0x8000
	or	$1, $1, $3		; $1 = $1 | $3 = 0xF171
	xor	$3, $3, $3		; $3 = $3 ^ $3 = 0
	addi	$3, -1			; $3 = -1
	stw	0($6), $3		;  m = $3
	add	$3, $0, -1		; $3 = 0xFFFF
	shr	$3, $3, 8		; $3 >>= 8 = 0x00FF
	sext	$2, $3			; $2 = sext $3 = 0xFFFF
	and	$1, $1, $2		; $1 = $1 & $2 = 0xF171

	.ldi	$7, sbp			; setup stack
	.push	$1			; push 0xF171
	.call	count_bits, $5		; count 1 bits
	.pop	$2			; $2 = result = 9
	xor	$3, $1, $2		; $3 = $1 ^ $2 = 0xF178

	.ldi	$1, test		; $1 = &test
	lcr	$2, $cr0		; $2 = PC + 2 (&test)
	add	$0, $0, $0		; noop
test:	s.eq	$1, $2			; skip if same address
	add	$3, $3, $1		; scramble $3

	shr	$3, $3, 1		; $3 >>= 1 = 0x78BC
	lui	$5, 0x80		; $5 = 0x8000
	or	$3, $3, $5		; $3 |= $5 = 0xF8BC

	add	$3, $3, 1		; $3 += 1 (0xF8BD)
	ldw	$2, 0($6)		; $2 = m (0xFFFF)
	ldw	$1, 0($6)		; $1 = m (0xFFFF)
	.ldi	$5, 12			; $5 = 12 (shift count)
1:	shl	$1, $1, 1		; $1 <<= 1
	shr	$2, $2, 1		; $2 >>= 1
	as.z	$5, $5, -1		; dec 5, skip if zero
	jmp	1b			; loop

	or	$1, $1, $2		; $1 = $1 | $2 (0xF00F)
	and	$1, $1, $3		; $1 = $3 & $1 = 0xF00D

	add	$2, $0, 2		; $2 = 2
	add	$3, $2, 1		; $3 = 3
	add	$4, $3, 1		; $4 = 4
	add	$5, $4, 1		; $5 = 5
	add	$6, $0, -1		; $6 = -1
	add	$7, $0, 1		; $7 = 2

	s.ne	$2, $3			; test skips
	add	$1, $1, 1		; we shouldn't hit any adds
	s.gt	$7, $6
	add	$1, $1, 1
	s.gte	$2, $7
	add	$1, $1, 1
	s.lt	$4, $5
	add	$1, $1, 1
	s.lte	$6, $2
	add	$1, $1, 1
	s.ult	$7, $6
	add	$1, $1, 1
	s.ulte	$7, $2
	add	$1, $1, 1

	jmp	0

count_bits:
	.push	$1			; preserve $1
	ldw	$1, 2($7)		; $1 = argument = 0xF171
	.push	$2			; preserve $2
	.push	$3			; preserve $3
	.push	$4			; preserve $4
	add	$2, $0, $0		; $2 = 0
	.ldi	$4, 16			; $4 = 16 (bits)
1:	and	$3, $1, 1		; $3 = $1 & 1
	s.eq	$3, $0			; skip if 0
	add	$2, $2, 1		; inc $2
	shr	$1, $1, 1		; $1 = $1 >> 1
	as.z	$4, $4, -1		; dec $4, skip when done
	jmp	1b			; loop
	.pop	$4			; restore $4
	stw	4($7), $2		; result = $2 = 9
	.pop	$3			; restore $3
	.pop	$2			; restore $2
	.pop	$1			; restore $1
	.ret	$5			; return
