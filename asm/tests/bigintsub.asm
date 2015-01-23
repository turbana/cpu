;;
;; Test Big Integer subtraction
;;
;@; stop(13)
;@; assert($1 = 0x0FFF)
;@; assert($2 = 0xFFFF)

; res = op1 - op2
; op1 = 0x1000 0000
; op2 = 0x0000 0001
; res = 0x0FFF FFFF
;
; $1:$2 = res
; $3:$4 = op1
; $5:$6 = op2

	.text
	.ldi	$3, 0x1000
	.ldi	$4, 0x0000
	.ldi	$5, 0x0000
	.ldi	$6, 0x0001

	; alow = blow - clow
	; ahigh = bhigh - chigh

	sub	$2, $4, $6
	sub	$1, $3, $5
	s.ulte	$6, $4
	sub	$1, $1, 1

	; borrow if blow < clow
	; skip borrow if blow >= clow
	; skip if clow <= blow

	;add	$2, $4, $6
	;add	$1, $3, $5
	;s.ulte	$6, $2
	;add	$1, $1, 1

	jmp	0
