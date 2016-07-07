;;
;; calculates the Nth fibonacci number
;;

; |@| 15000 ($1=0090 $2=0080 $3=0081 $7=0080)

	.data
	.zero	128			; stack
stack:
n:	.word	0x000C			; n-th fibonacci number
x:	.word	0x0000			; store result in x

	.text
	.ldi	$7, stack		; setup stack
	.ldi	$2, n
	.ldi	$3, x
	ldw	$1, 0($2)		; load n
	.call	fib			; call fib(n)
	stw	0($3), $1		; x = fib(n)
	jmp	0

fib:	.enter	2
	stw	2($7), $2		; save $2
	s.ne	$1, $0			; check for 0
	jmp	done			; fib(0) = 0
	as.nz	$2, $1, -1		; check for 1; $2 = n-1
	jmp	done			; fib(1) = 1
	add	$1, $0, $2		; n-1
	.call	fib			; fib(n-1)
	stw	1($7), $1		; save fib(n-1)
	sub	$1, $2, 1		; n-2
	.call	fib			; fib(n-2)
	ldw	$2, 1($7)		; restore fib(n-1)
	add	$1, $1, $2		; sum
done:	ldw	$2, 2($7)		; restore $2
	.leave
