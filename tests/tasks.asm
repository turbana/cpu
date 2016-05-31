;;; test multiple tasks running concurrently

	.set	PIC_ADDR,	0xFF80
	.set	ICW1,		0x0010
	.set	ICW2,		idt
	.set	EOI,		0x20
	.set	USER_MODE,	0x0002

	.set	T1_START,	0x0010
	.set	T1_SEGMENT,	1
	.set	T1_PC,		T1_START
	.set	T1_FLAGS,	((T1_SEGMENT << 4) | (T1_SEGMENT << 10)) | USER_MODE
	.set	T1_R1,		0x0011
	.set	T1_R2,		0x0012
	.set	T1_R3,		0x0013
	.set	T1_R4,		0x0014
	.set	T1_R5,		0x0015
	.set	T1_R6,		0x0016
	.set	T1_R7,		0x0017

	.set	T2_START,	0x0020
	.set	T2_SEGMENT,	2
	.set	T2_PC,		T2_START
	.set	T2_FLAGS,	((T2_SEGMENT << 4) | (T2_SEGMENT << 10)) | USER_MODE
	.set	T2_R1,		0x0021
	.set	T2_R2,		0x0022
	.set	T2_R3,		0x0023
	.set	T2_R4,		0x0024
	.set	T2_R5,		0x0025
	.set	T2_R6,		0x0026
	.set	T2_R7,		0x0027


	.data
	;; first 2 words are scratch space for task_switch
	.word	0		; supervisor stack
	.word	0		; temp task stack
	.zero	32
stack:	.word	T2_PC		; push T2 onto stack so T1 will be switched in first
	.word	T2_FLAGS
	.word	T2_R1
	.word	T2_R2
	.word	T2_R3
	.word	T2_R4
	.word	T2_R5
	.word	T2_R6
	.word	T2_R7

	.set	TASK_LEN, 9
tasks:	.word	T1_PC
	.word	T1_FLAGS
	.word	T1_R1
	.word	T1_R2
	.word	T1_R3
	.word	T1_R4
	.word	T1_R5
	.word	T1_R6
	.word	T1_R7
	.word	T2_PC
	.word	T2_FLAGS
	.word	T2_R1
	.word	T2_R2
	.word	T2_R3
	.word	T2_R4
	.word	T2_R5
	.word	T2_R6
	.word	T2_R7


	.text
	.ldi	$7, stack

	;;  copy T1 code
	.ldi	$1, T1_START
	.ldi	$2, t1code
	.ldi	$3, t1code_end - t1code
	.ldi	$4, T1_SEGMENT
	.call	copy

	;;  copy T2 code
	.ldi	$1, T2_START
	.ldi	$2, t2code
	.ldi	$3, t2code_end - t2code
	.ldi	$4, T2_SEGMENT
	.call	copy

	;; setup interrupts
	.ldi	$1, PIC_ADDR	; load &PIC
	.ldi	$2, ICW1	; send ICW1
	stw	$0($1), $2	;
	.ldi	$2, ICW2	; send ICW2
	stw	1($1), $2

	;; jump into middle of irq6 (we already have T1 on stack)
	jmp	__load_task


irq6:
	;; save current task
	stw	1($0), $7	; save $7
	ldw	$7, $0($0)	; load supervisor stack
	addi	$7, -7
	stw	$0($7), $1	; save $1
	stw	1($7), $2	; save $2
	stw	2($7), $3	; save $3
	stw	3($7), $4	; save $4
	stw	4($7), $5	; save $5
	stw	5($7), $6	; save $6
	ldw	$1, 1($0)	; load temp $7
	stw	6($7), $1	; save $7
	sub	$7, $7, 2
	lcr	$1, $cr2	; load $epc
	lcr	$2, $cr3	; load $eflags
	stw	$0($7), $1	; save $epc
	stw	1($7), $2	; save $eflags

	;; ack interrupt
	.ldi	$1, PIC_ADDR	; &PIC
	.ldi	$2, EOI		; EOI
	stw	$0($1), $2	; send EOI

	.call	task_switch

__load_task:
	;; load new task
	ldw	$2, 1($7)	; load $eflags
	ldw	$1, $0($7)	; load $epc
	scr	$cr3, $2	; save $eflags
	scr	$cr2, $1	; save $epc
	add	$7, $7, 2
	ldw	$1, 6($7)
	stw	1($0), $1	; save temp $7
	ldw	$6, 5($7)	; load $6
	ldw	$5, 4($7)	; load $5
	ldw	$4, 3($7)	; load $4
	ldw	$3, 2($7)	; load $3
	ldw	$2, 1($7)	; load $2
	ldw	$1, $0($7)	; load $1
	addi	$7, 7
	stw	$0($0), $7	; save supervisor stack
	ldw	$7, 1($0)	; load $7
	iret


task_switch:
	.enter	0
	.ldi	$5, tasks	; load pointer to tasks
	add	$6, $7, 2	; load pointer to stack
	;; find previous task by inspecting data segment
	ldw	$4, 1($6)
	shr	$4, $4, 8
	shr	$4, $4, 2
	as.z	$0, $4, -1
	addi	$5, TASK_LEN	; move tasks pointer to task two
	;; save control registers
	ldw	$1, $0($6)	; $pc
	ldw	$2, 1($6)	; $flags
	stw	$0($5), $1
	stw	1($5), $2
	;; increment pointers
	add	$5, $5, 2
	add	$6, $6, 2
	;; save regular registers
	ldw	$1, $0($6)	; $1
	ldw	$2, 1($6)	; $2
	stw	$0($5), $1
	stw	1($5), $2
	ldw	$1, 2($6)	; $3
	ldw	$2, 3($6)	; $4
	stw	2($5), $1
	stw	3($5), $2
	ldw	$1, 4($6)	; $5
	ldw	$2, 5($6)	; $6
	stw	4($5), $1
	stw	5($5), $2
	ldw	$1, 6($6)	; $7
	stw	6($5), $1
	;; find next task
	.ldi	$1, TASK_LEN	; task pointer delta (assuming previous task was one)
	as.z	$0, $4, -1
	addi	$1, -(2*TASK_LEN) ; update task pointer delta for task two
	add	$5, $5, $1	; update task pointer
	;; load regular registers
	ldw	$1, $0($5)	; $1
	ldw	$2, 1($5)	; $2
	stw	$0($6), $1
	stw	1($6), $2
	ldw	$1, 2($5)	; $3
	ldw	$2, 3($5)	; $4
	stw	2($6), $1
	stw	3($6), $2
	ldw	$1, 4($5)	; $5
	ldw	$2, 5($5)	; $6
	stw	4($6), $1
	stw	5($6), $2
	ldw	$1, 6($5)	; $7
	stw	6($6), $1
	;; decrement pointers
	add	$5, $5, -2
	add	$6, $6, -2
	;; load control registers
	ldw	$1, $0($5)
	ldw	$2, 1($5)
	stw	$0($6), $1
	stw	1($6), $2
	.leave


	;; copy code from supervisor to user
	;; $1 = destination pointer (in user segment)
	;; $2 = source pointer (in supervisor segment)
	;; $3 = count
	;; $4 = user segment
copy:	.enter	5
	;; save parameters
	stw	5($7), $4
	stw	4($7), $3
	stw	3($7), $2
	stw	2($7), $1
	;; create and save flags
	shl	$5, $4, 4
	shl	$6, $5, 6
	or	$6, $5, $6
	stw	1($7), $6

loop:	ldiw	$3, 1($2)	; load 2nd word
	ldiw	$4, 2($2)	; load 3rd word
	ldiw	$5, 3($2)	; load 4th word
	scr	$cr1, $6	; swap to user segment
	ldiw	$2, $0($2)	; load 1st word (in shadow of segment change)
	stiw	$0($1), $2	; save 1st word
	stiw	1($1), $3	; save 2nd word
	stiw	2($1), $4	; save 3rd word
	stiw	3($1), $5	; save 4th word
	scr	$cr1, $0	; swap to supervisor segment
	add	$0, $0, $0	; no memory access possible in shadow of segment change
	ldw	$5, 4($7)	; load count
	as.nz	$5, $5, -4	; decrement count
	jmp	done
	stw	4($7), $5	; save count
	add	$1, $1, 4	; increment dest pointer
	ldw	$2, 3($7)	; load source pointer
	add	$2, $2, 4	; increment source pointer
	stw	3($7), $2	; save source pointer
	jmp	loop
done:	.leave


	.align 4
t1code: add	$1, $2, $3
	sub	$2, $3, $4
	add	$3, $4, $5
	sub	$4, $5, $6
	sub	$5, $6, $7
	add	$6, $7, $1
	sub	$7, $1, $2
	jmp	t1code
	.align	4
t1code_end:

	;; task two code
t2code: sub	$1, $2, $3
	add	$2, $3, $4
	sub	$3, $4, $5
	add	$4, $5, $6
	sub	$5, $6, $7
	add	$6, $7, $1
	sub	$7, $1, $2
	jmp	t2code
	.align	4
t2code_end:

	;; interrupt descriptor table
	.align	8
idt:	iret
	iret
	iret
	iret
	iret
	iret
	jmp	irq6
	iret
