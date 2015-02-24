;;
;; Test screen output
;;

	.data
str:	.ascii	"Hello World!\n"
strlen:	.word	@-str


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
