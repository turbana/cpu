;;
;; Test immediates
;;

	.text
	.ldi	$1, 1		; |@|  5 ($1=0001)
	.ldi	$2, 0		; |@|  7 ($2=0000)
	.ldi	$3, 0x0180	; |@|  9 ($3=0180)
	.ldi	$4, 0xABCD	; |@| 11 ($4=ABCD)
	.ldi	$5, -1		; |@| 13 ($5=FFFF)
	.ldi	$6, 0x017F	; |@| 15 ($6=017F)
	.ldi	$7, 0x1080	; |@| 17 ($7=1080)
	jmp	0