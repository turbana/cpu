;;
;; Test macros in seperate file
;;
;@; stop(55)
;@; assert($1 = 0x00FF)
;@; assert($2 = 0x0023)

	.data
	.zero	32
sbp:

	.text
	.ldi	$7, sbp
	.call	main, $5
	jmp	0

	.test	a, 0xAB
	.test	b, 0xBC
	.test	c, 0xDE
	.test	d, 0xFF

	.text
main:	.call	load_a, $6
	.call	load_b, $6
	.call	load_c, $6
	.call	load_d, $6
	.ret	$6
