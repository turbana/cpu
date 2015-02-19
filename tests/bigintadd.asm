;;
;; Test Big Integer addition
;;

; |@| 16 ($1=1000 $2=0000)

; res = op1 + op2
; op1 = 0x0FFF FFFF
; op2 = 0x0000 0001
; res = 0x1000 0000
;
; $1:$2 = res
; $3:$4 = op1
; $5:$6 = op2

	.text
	.ldi	$3, 0x0FFF
	.ldi	$4, 0xFFFF
	.ldi	$5, 0x0000
	.ldi	$6, 0x0001

	add	$2, $4, $6
	add	$1, $3, $5
	s.ulte	$6, $2
	add	$1, $1, 1

	jmp	0
