;;
;; Test imem/dmem interactions
;;
;
; This will copy itself into higher memory then jump into the copied code

;;; TODO add tests

	.data
size:	.dw	0x0008		; size of memory to move
src:	.dw	0x0008		; code source
dest:	.dw	0x0010		; code destination


	.text
	.ldi	$7, size
	.ldi	$6, dest
	.ldi	$5, src

	ldw	$3, 0($6)
	ldw	$2, 0($5)

	;;
	.align	8
start:	ldw	$4, 0($7)
loop:	ldiw	$1, $2
	stiw	$3, $1
	add	$2, $2, 1
	add	$3, $3, 1
	as.z	$4, $4, -1
	jmp	loop
	add	$0, $0, $0
