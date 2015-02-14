;;
;; Test macros in seperate file
;;

;;; TODO update to new calling conventions

;@; 17 ($1=00FF $2=0023 $3=0004)

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
	.ldi	$2, latest
	ldw	$1, 0($2)
	.ret	$6

main:	.ldi	$7, sbp
	.call	latest, $6
	.ldi	$3, count
	jmp	0
