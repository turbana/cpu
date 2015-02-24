;;
;; Test macros in seperate file
;;

; |@| 111 ($1=00FF $2=0023 $3=0004)

	.set	count, 0
	.set	latest, 0

	.data
	.zero	32
sbp:

	.text
	jmp	main

	.test	a, 0xAB
	.test	b, 0xBC
	.test	c, 0xDE
	.test	d, 0xFF

load_latest:
	.enter	0
	.ldi	$2, latest
	ldw	$1, 0($2)
	.leave

main:	.ldi	$7, sbp
	add	$6, $0, $0
	.call	load_d
	.call	load_c
	.call	load_b
	.call	load_a
	.call	latest
	.ldi	$3, count
	jmp	0
