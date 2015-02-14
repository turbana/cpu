;;
;; Test timer interrupt
;;

;;; TODO add tests

	.data
count:	.dw	0
	.zero	32
sbp:

	.text
	.ldi	$7, sbp		; setup stack

	.ldi	$2, 0x107	; load IDT for timer
	.ldi	$1, timer	; load timer addr
	stw	0($2), $1	; set IDT for timer

	lcr	$1, $cr1	; load flags
	or	$1, $1, 1	; set IE bit
	scr	$cr1, $1	; enable interrupts

loop:	add	$1, $1, -8	; loop forever
	add	$2, $2, -4
	add	$1, $1, -2
	add	$2, $2, -1
	add	$1, $1,  1
	add	$2, $2,  2
	add	$1, $1,  4
	add	$2, $2,  8
	jmp	loop

timer:	sub	$7, $7, 2	; alloc 2 words on stack
	stw	1($7), $2	; save $2
	stw	0($7), $1	; save $1

	.ldi	$2, count	; get count addr
	ldw	$1, 0($2)	; load count
	add	$1, $1, 1	; inc count
	stw	0($2), $1	; store count

	.ldi	$1, 0x00AB	; EOI
	.ldi	$2, 0x0010	; &PIC
	outb	$2, $1		; send EOI to PIC

	lcr	$1, $cr1	; load flags
	or	$1, $1, 1	; set IE bit
	scr	$cr1, $1	; enable interrupts

	ldw	$1, 0($7)	; restore $1
	ldw	$2, 1($7)	; restore $2
	add	$7, $7, 2	; pop 2 words
	reti			; return
