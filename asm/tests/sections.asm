;;
;; Test sections
;;
; Computes fibonacci infinitely
;
; Data Mem:
;	...
;	0x0008: 1 (b)
;	...
;	0x0010: 0 (a)
;
; Instruction Mem:
;	0x0000: jmp to 0x0010
;	...
;	0x0010: start
;	(code)
;	0x0018: stw 0($4), $1
;	0x0019: jmp to 0x0010

	.data
	.zero	1
	.align	16
a:	.dw	0		; a @ 0x0010

	.text
	jmp	start

	.org	0x0010
start:	.ldi	$3, a		; start @ 0x0010
	.ldi	$4, b
loop:	ldw	$1, 0($3)	; $1 = a
	ldw	$2, 0($4)	; $2 = b
	add	$1, $1, $2	; $1 += $2
	stw	0($3), $2	; a = $2 (old b)
	stw	0($4), $1	; b = $1
	add	$5, $5, $5	; will be overwritten with jmp loop

	.data
	.org	0x0008
b:	.dw	1		; b @ 0x0008

	.text
	.org	0x0019
	jmp	loop
