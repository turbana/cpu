;;
;; Echo keyboard input to screen
;;
; KB interrupt handler reads from the KB and stores keys in a shared circular
; buffer. The main loop checks for a non-empty buffer and prints any printable
; characters found.
;
; Notes:
;  - KB IRQ is 2
;  - Does not handle key release scancodes


	.set	UART0,		0xFF90
	.set	UART1,		0xFFA0
	.set	PIC_ADDR,	0xFF80
	.set	KB_ADDR,	UART0
	.set	SCR_ADDR,	UART1
	.set	ICW1,		0x0010
	.set	ICW2,		idt & 0x00F8
	.set	EOI,		0x0020


	.data
	.align	4
	;; 8 word buffer
buf:	.ascii 	"echo\n>  "
bstart:	.word 	buf
bend:	.word 	buf+7
	.zero	64
sbp:


	.text
	.ldi	$7, sbp		; setup stack

	.ldi	$1, PIC_ADDR	; load &PIC
	.ldi	$2, ICW1	; send ICW1
	stw	0($1), $2	;
	.ldi	$2, ICW2	; send ICW2
	stw	1($1), $2

	.ldi	$2, SCR_ADDR	; screen address

	lcr	$1, $cr1	; load flags
	or	$1, $1, 1	; set IE bit
	scr	$cr1, $1	; enable interrupts

	.ldi	$6, bend	; buffer pointers
	.ldi	$5, bstart

loop:	ldw	$4, 0($6)	; load buffer pointers
	ldw	$3, 0($5)
	s.ne	$3, $4
	jmp	loop		; loop if pointers are equal (empty buffer)

	ldw	$1, 0($3)	; load character
	stw	0($2), $1	; write character

	add	$3, $3, 1	; increment and wrap bstart
	and	$3, $3, 7
	stw	0($5), $3

	jmp	loop		; repeat


	;; Keyboard IRQ Handler
keyboard:
	sub	$7, $7, 3	; save registers
	stw	2($7), $3
	stw	1($7), $2
	stw	0($7), $1

	.ldi	$2, KB_ADDR	; read scancode
	ldw	$1, 0($2)

	.ldi	$3, bend	; load bend
	ldw	$2, 0($3)

	stw	0($2), $1	; store scancode in buffer

	add	$2, $2, 1	; increment and wrap bend
	and	$2, $2, 7
	stw	0($3), $2

	.ldi	$1, PIC_ADDR	; &PIC
	.ldi	$2, EOI		; EOI
	stw	0($1), $2	; send EOI

	ldw	$1, 0($7)	; restore registers
	ldw	$2, 1($7)
	ldw	$3, 2($7)
	add	$7, $7, 3
	iret


timer:	sub	$7, $7, 2	; save registers
	stw	1($7), $2
	stw	0($7), $1

	.ldi	$1, PIC_ADDR	; &PIC
	.ldi	$2, EOI		; EOI
	stw	0($1), $2	; send EOI

	ldw	$1, 0($7)	; restore registers
	ldw	$2, 1($7)
	add	$7, $7, 2
	iret


	;; IDT
	.align 8
idt:
irq0:	jmp	error
irq1:	jmp	error
irq2:	jmp	error
irq3:	jmp	keyboard
irq4:	jmp	error
irq5:	jmp	error
irq6:	jmp 	timer
irq7:
error:	jmp	0
