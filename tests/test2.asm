; test stack pushes/pops
; also test lui/addi for 16 bit immediates

;;; TODO add tests

	.data
	.align	2
	.zero	16
sbp:

	.text
	addi	$6, sbp
	lui	$1, 0xFF
	addi	$1, 0xFF
	add	$1, $1, 1
	addi	$2, 0x10
	add	$5, $6, $0

1:	add	$1, $1, 1
	stw	-1($6), $1
	sub	$6, $6, 1
	as.z	$2, $2, -1
	jmp	1b

1:	ldw	$1, 0($6)
	stw	0($6), $0
	add	$6, $6, 1
	s.eq	$1, $0
	jmp	1b

	halt
