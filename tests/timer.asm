;;
;; Test timer interrupt
;;

;;; TODO add tests

	.set	PIC_ADDR,	0xFF80
	.set	ICW1,		0x0080
	.set	ICW2,		idt & 0x00F8
	.set	EOI,		0x0020

	.data
count:	.word	0
	.zero	32
sbp:

	.text
	.ldi	$7, sbp		; setup stack

	.ldi	$1, PIC_ADDR	; load &PIC
	.ldi	$2, ICW1	; send ICW1
	stw	$0($1), $2	;
	.ldi	$2, ICW2	; send ICW2
	stw	1($1), $2

	lcr	$1, $cr1	; load flags
	or	$1, $1, 1	; set IE bit
	scr	$cr1, $1	; enable interrupts

	.ldi	$1, 0x1234
	.ldi	$2, 0xABCD

loop:	add	$1, $1, -8	; loop forever
	add	$2, $2, -4
	add	$1, $1, -2
	add	$2, $2, -1
	add	$2, $2,  1
	add	$1, $1,  2
	add	$2, $2,  4
	add	$1, $1,  8
	jmp	loop

error:	jmp	0

timer:	sub	$7, $7, 2	; alloc 2 words on stack
	stw	1($7), $2	; save $2
	stw	0($7), $1	; save $1

	.ldi	$2, count	; get count addr
	ldw	$1, 0($2)	; load count
	add	$1, $1, 1	; inc count
	stw	$0($2), $1	; store count

	.ldi	$1, PIC_ADDR	; &PIC
	.ldi	$2, EOI		; EOI
	stw	$0($1), $2	; send EOI

	ldw	$1, $0($7)	; restore $1
	ldw	$2, 1($7)	; restore $2
	add	$7, $7, 2	; pop 2 words
	iret			; return

	.align 8
idt:
irq0:	jmp	error
irq1:	jmp	error
irq2:	jmp	error
irq3:	jmp	error
irq4:	jmp	error
irq5:	jmp	error
irq6:	jmp	timer
irq7:	jmp	error
