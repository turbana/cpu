; test expressions

	.data
	.zero	32
sbp:

	.text
start:	jmp	exit + 1
exit:	jmp	((end * 2) / 2)
	ldw	$6, sbp($0)
	ldw	$5, ((sbp - 4) >> 2)($0)
	ldw	$5, ~(2-1)($0)
	stw	(1-2)($0), $1
	jmp	start + 1
end:	halt
