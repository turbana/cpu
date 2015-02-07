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


	.data
	.align	4
buf:	.zero	4		; 4 word input buffer
bstart:	.dw	buf
bend:	.dw	buf
	.zero	64
sbp:

	;; IDT
	.org	0x0100
	.dw	empty		; IRQ 0
	.dw	empty		; IRQ 1
	.dw	keyboard	; IRQ 2
	.dw	empty		; IRQ 3
	.dw	empty		; IRQ 4
	.dw	empty		; IRQ 5
	.dw	empty		; IRQ 6
	.dw	empty		; IRQ 7


	.text
	.ldi	$7, sbp		; setup stack

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
	and	$4, $3, -4	; $4 = $3 & 1..1100
	xor	$3, $3, $4	; clear high bits of $3
	stw	0($5), $3	; TODO above should really be 'and $3, $3, 3'

	.ldi	$2, 0x0020	; ascii space
	s.gte	$1, $2		; if chr non-printable
	jmp	loop		; then read another

	.ldi	$2, 0x0020	; screen port
	outb	$2, $1		; send character to screen

	.ldi	$1, 0x000a	; send newline
	outb	$2, $1

	jmp	loop		; repeat


	;; Keyboard IRQ Handler
keyboard:
	sub	$7, $7, 8	; save registers
	stw	3($7), $4
	stw	2($7), $3
	stw	1($7), $2
	stw	0($7), $1
	lcr	$1, $cr2	; save EPC
	stw	4($7), $1

	.ldi	$2, 0x0030	; read scancode
	inb	$1, $2

	.ldi	$3, bend	; load bend
	ldw	$2, 0($3)

	stw	0($2), $1	; store scancode in buffer

	add	$2, $2, 1	; increment and wrap bend
	and	$1, $2, -4	; $1 = $2 & 1..1100
	xor	$2, $2, $1	; clear high bits of $2
	stw	0($3), $2	; TODO above should really be 'and $2, $2, 3'

	.ldi	$1, 0x00AB	; ack IRQ
	.ldi	$2, 0x0010
	outb	$2, $1

	lcr	$1, $cr1	; re-enable interrupts
	or	$1, $1, 1
	scr	$cr1, $1

	ldw	$1, 4($7)	; restore EPC
	scr	$cr2, $1
	ldw	$1, 0($7)	; restore registers
	ldw	$2, 1($7)
	ldw	$3, 2($7)
	ldw	$4, 3($7)
	add	$7, $7, 8
	reti


	;; Empty IRQ Handler
empty:	sub	$7, $7, 4	; save registers
	stw	1($7), $2
	stw	0($7), $1
	lcr	$1, $cr2	; save EPC
	stw	2($7), $1

	.ldi	$1, 0x00AB	; ack IRQ
	.ldi	$2, 0x0010
	outb	$2, $1

	lcr	$1, $cr1	; re-enable interrupts
	or	$1, $1, 1
	scr	$cr1, $1

	ldw	$1, 2($7)	; restore EPC
	scr	$cr2, $1
	ldw	$1, 0($7)	; restore registers
	ldw	$2, 1($7)
	add	$7, $7, 4
	reti
