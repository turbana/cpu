;;
;; Echo keyboard input to screen
;;
; KB interrupt handler reads from the KB and stores keys in a shared circular
; buffer. The main loop checks for a non-empty buffer and prints any printable
; characters found.
;
; Notes:
;  - KB IRQ is 2
;  - IDT is at 0x0100
;  - KB data port is 0x30
;  - Does not handle key release scancodes


	.set	PIC_PORT, 0x10
	.set	SCR_PORT, 0x20
	.set	KB_PORT,  0x30
	.set	EOI,      0xAB


	.data
	.align	4
buf:	.zero	4		; 4 word input buffer
bstart:	.word	buf
bend:	.word	buf
	.zero	64
sbp:


	.text
	.ldi	$7, sbp		; setup stack

	add	$2, $0, $0	; shut up the simulator's error checker

	lcr	$1, $cr1	; enable interrupts
	or	$1, $1, 1
	scr	$cr1, $1

	.ldi	$6, bend
	.ldi	$5, bstart

loop:	ldw	$4, 0($6)
	ldw	$3, 0($5)
	s.ne	$3, $4
	jmp	loop

	ldw	$1, 0($3)	; load character

	add	$3, $3, 1	; increment and wrap bstart
	and	$3, $3, 3
	stw	0($5), $3

	.ldi	$2, SCR_PORT	; screen port
	outb	$2, $1		; send character to screen

	jmp	loop		; repeat


	;; IDT
	.org	0x0100
	jmp	empty		; IRQ 0
	jmp	empty		; IRQ 1
	jmp	keyboard	; IRQ 2
	jmp	empty		; IRQ 3
	jmp	empty		; IRQ 4
	jmp	empty		; IRQ 5
	jmp	empty		; IRQ 6
empty:	sub	$7, $7, 2	; IRQ 7 (empty handler)
	stw	1($7), $2
	stw	0($7), $1
	.ldi	$1, EOI		; ack IRQ
	.ldi	$2, PIC_PORT
	outb	$2, $1
	ldw	$1, 0($7)	; restore registers
	ldw	$2, 1($7)
	add	$7, $7, 2
	iret


	;; Keyboard IRQ Handler
keyboard:
	sub	$7, $7, 3	; save registers
	stw	2($7), $3
	stw	1($7), $2
	stw	0($7), $1

	.ldi	$2, KB_PORT	; read scancode
	inb	$1, $2

	.ldi	$3, bend	; load bend
	ldw	$2, 0($3)

	stw	0($2), $1	; store scancode in buffer

	add	$2, $2, 1	; increment and wrap bend
	and	$2, $2, 3
	stw	0($3), $2

	.ldi	$1, EOI		; ack IRQ
	.ldi	$2, PIC_PORT
	outb	$2, $1

	ldw	$1, 0($7)	; restore registers
	ldw	$2, 1($7)
	ldw	$3, 2($7)
	add	$7, $7, 3
	iret
