; calculates the Nth fibonacci number

	.data
n:	.dw	0x000C			; n-th fibonacci number
x:	.dw	0x0000			; store result in x
	.zero	64			; stack
sbp:

	.text
	.ldi	$7, sbp			; setup stack
	ldw	$1, n($0)		; load and push n
	.push	$1
	.call	fib, $3			; call fib(n)
	.pop	$1			; store result in x
	stw	x($0), $1
	halt

fib:	ldw	$1, 1($7)		; load parameter into $1
	s.ne	$1, $0			; check for 0
	jmp	done			; fib(0) = 0
	as.nz	$1, $1, -1		; check for 1
	jmp	done			; fib(1) = 1
	.push	$1			; keep n-1
	.push	$1			; call fib(n-1)
	.call	fib, $3
	.pop	$2			; result of fib(n-1)
	.pop	$1			; n-1
	add	$1, $1, -1		; n-2
	.push	$2			; save fib(n-1)
	.push	$1			; call fib(n-2)
	.call	fib, $4
	.pop	$1			; result of fib(n-2)
	.pop	$2			; result of fib(n-1)
	add	$1, $1, $2		; sum
	stw	1($7), $1		; store in result
done:	.ret
