;;
;; Test screen output
;;

	.data
str:	.dw	0x48		; Hello World!\n
	.dw	0x65
	.dw	0x6C
	.dw	0x6C
	.dw	0x6F
	.dw	0x20
	.dw	0x57
	.dw	0x6F
	.dw	0x72
	.dw	0x6C
	.dw	0x64
	.dw	0x21
	.dw	0x0A
strlen:	.dw	0x0D


	.text
	.ldi	$4, 0x0020	; $4 = &screen
	.ldi	$3, strlen
	ldw	$3, 0($3)	; $3 = strlen
	.ldi	$2, str		; $2 = &str

loop:	ldw	$1, 0($2)
	outb	$4, $1
	add	$2, $2, 1
	as.z	$3, $3, -1
	jmp	loop

done:	jmp	done
