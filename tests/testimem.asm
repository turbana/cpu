;;
;; Test imem/dmem interactions
;;
;
; This will first copy itself into data memory. Then copy itself back,
; offset by `size' words, and jump into the newly copied code.

;;; TODO add tests

	.data
size:	.word	0x0020		; size of memory to move
cptr:	.word	0x0000		; code pointer
dptr:	.word	0x0003		; data pointer
data:	.zero	0x0020		; scratch data


	.text
	.ldi	$7, cptr	; $7 = &cptr
	.ldi	$6, dptr	; $6 = &dptr
	.ldi	$5, size	; $5 = &size

	ldw	$2, 0($7)	; $2 = cptr
	ldw	$3, 0($6)	; $3 = dptr
	ldw	$4, 0($5)	; $4 = size

code_to_data:
	ldiw	$1, $2		; $1 = *cptr
	stw	0($3), $1	; *dptr = $1
	add	$2, $2, 1	; cptr++
	add	$3, $3, 1	; dptr++
	as.z	$4, $4, -1	; while (--size > 0)
	jmp	code_to_data

	;; rewind dptr
	ldw	$4, 0($5)	; $4 = *size
	sub	$3, $3, $4	; *dptr -= *size

data_to_code:
	ldw	$1, 0($3)	; $1 = *dptr
	stiw	$2, $1		; *cptr = $1
	add	$2, $2, 1	; cptr++
	add	$3, $3, 1	; dptr++
	as.z	$4, $4, -1	; while (--size > 0)
	jmp	data_to_code

	;; rewind cptr
	ldw	$4, 0($5)	; $4 = *size
	sub	$2, $2, $4	; *cptr -= size

	;; save pointers
	stw	0($6), $3	; save dptr
	stw	0($7), $2	; save cptr

	jmp	$2		; goto *cptr
