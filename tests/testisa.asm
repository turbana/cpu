;;
;; Test ISA
;;
; TODO add memory tests
;
; final check |@| 346 ($1=F00D $cr0=005A)

	.data
n:	.word	0xABCD
m:	.word	0x0000
	.zero	32
sbp:

	.text
	.ldi	$4, n			; $4 = &n			|@|   5 ($4=0000)
	.ldi	$6, m			; $6 = &m			|@|   7 ($6=0001)
	add	$5, $0, 2		; $5 = 2			|@|   8 ($5=0002)
					;
1:	ldw	$1, 0($4)		; $1 = n			|@|   9 ($1=ABCD)
	stw	0($6), $1		;  m = n			<memory test>
	shl	$2, $1, 8		; $2 = n << 8			|@|  11 ($2=CD00)
	shr	$3, $1, 8		; $3 = n >> 8			|@|  12 ($3=00AB)
	or	$1, $3, $2		; $1 = $3 | $2			|@|  13 ($1=CDAB)
	stw	0($4), $1		;  n = $1			<memory test>
	as.z	$5, $5, -1		; $5 -= 1; loop until 0		|@|  15 ($5=0001)
	jmp	1b			;
					;				|@|  26 ($1=ABCD $2=AB00 $3=00CD $5=0000)
	ldw	$1, 0($4)		; $1 = n (0xABCD)		|@|  27 ($1=ABCD)
	ldw	$2, 0($6)		; $2 = m (0xCDAB)		|@|  28 ($2=CDAB)
	sub	$3, $0, -4		; $3 = 4			|@|  29 ($3=0004)
1:	shl	$1, $1, 1		; $1 <<= 1			|@|  30 ($1=579A)
	shr	$2, $2, 1		; $2 >>= 1			|@|  31 ($2=66D5)
	sub	$3, $3, 1		; $3 -= 1			|@|  32 ($3=0003)
	s.eq	$3, $0			; loop until $3 == 0
	jmp	1b			;
					;				|@|  54 ($1=BCD0 $2=0CDA $3=0000)
	or	$3, $1, $2		; $3 = $1 | $2			|@|  56 ($3=BCDA)
	stw	$0($4), $3		;  n = $3			<memory test>
	ldw	$1, $0($4)		; $1 = n			|@|  58 ($1=BCDA)
	ldw	$2, $0($6)		; $2 = m			|@|  59 ($2=CDAB)
	xor	$3, $1, $2		; $3 = 0xBCDA ^ 0xCDAB = 0x7171	|@|  61 ($3=7171)
	shl	$2, $3, 1		; $2 = $3 << 1 = 0xE2E2		|@|  62 ($2=E2E2)
	lui	$1, 0x80		; $1 = 0x8000			|@|  63 ($1=8000)
	or	$1, $1, $3		; $1 = $1 | $3 = 0xF171		|@|  64 ($1=F171)
	xor	$3, $3, $3		; $3 = $3 ^ $3 = 0		|@|  65 ($3=0000)
	sub	$3, $0, 1		; $3 = -1			|@|  66 ($3=FFFF)
	stw	0($6), $3		;  m = $3			<memory test>
	add	$3, $0, -1		; $3 = 0xFFFF			|@|  68 ($3=FFFF)
	shr	$3, $3, 8		; $3 >>= 8 = 0x00FF		|@|  69 ($3=00FF)
	lui	$2, 0xFF		; $2 = 0xFF00			|@|  70 ($2=FF00)
	sar	$2, $2, 8		; $2 >>>= 8 = 0xFFFF		|@|  71 ($2=FFFF)
	and	$1, $1, $2		; $1 = $1 & $2 = 0xF171		|@|  72 ($1=F171)
					;
	.ldi	$7, sbp			; setup stack			|@|  74 ($7=0022)
	.push	$1			; push 0xF171			|@|  75 ($7=0021)
					;				<memory test>
	sub	$7, $7, 1		; .call count_bits		|@|  77 ($7=0020)
	lcr	$5, $cr0		;				|@|  78 ($5=002C)
	add	$5, $5, 2		;				|@|  79 ($5=002E)
	stw	0($7), $5		;				<memory test>
	jmp	count_bits		;
	.pop	$2			; $2 = result = 9		|@| 236 ($2=0009)
					;				|@| 237 ($7=0022)
	xor	$3, $1, $2		; $3 = $1 ^ $2 = 0xF178		|@| 238 ($3=F178)
					;
	.ldi	$1, test		; $1 = &test			|@| 240 ($1=0035)
	lcr	$2, $cr0		; $2 = PC + 2 (&test)		|@| 241 ($2=0035)
	add	$0, $0, $0		; noop
test:	s.eq	$1, $2			; skip if same address
	add	$3, $3, $1		; scramble $3
					;				|@| 244 ($3=F178)
	shr	$3, $3, 1		; $3 >>= 1 = 0x78BC		|@| 245 ($3=78BC)
	.ldi	$5, 0x8000		; $5 = 0x8000			|@| 247 ($5=8000)
	or	$3, $3, $5		; $3 |= $5 = 0xF8BC		|@| 248 ($3=F8BC)
					;
	add	$3, $3, 1		; $3 += 1 (0xF8BD)		|@| 249 ($3=F8BD)
	ldw	$2, 0($6)		; $2 = m (0xFFFF)		|@| 250 ($2=FFFF)
	ldw	$1, 0($6)		; $1 = m (0xFFFF)		|@| 251 ($1=FFFF)
	.ldi	$5, 12			; $5 = 12 (shift count)		|@| 253 ($5=000C)
1:	shl	$1, $1, 1		; $1 <<= 1			|@| 254 ($1=FFFE)
	shr	$2, $2, 1		; $2 >>= 1			|@| 255 ($2=7FFF)
	as.z	$5, $5, -1		; dec 5, skip if zero		|@| 256 ($5=000B)
	jmp	1b			; loop
					;				|@| 323 ($1=F000 $2=000F $3=F8BD $5=0000)
	or	$1, $1, $2		; $1 = $1 | $2 (0xF00F)		|@| 324 ($1=F00F)
	and	$1, $1, $3		; $1 = $3 & $1 = 0xF00D		|@| 325 ($1=F00D)
					;
	add	$2, $0, 2		; $2 = 2			|@| 326 ($2=0002)
	add	$3, $2, 1		; $3 = 3			|@| 327 ($3=0003)
	add	$4, $3, 1		; $4 = 4			|@| 328 ($4=0004)
	add	$5, $4, 1		; $5 = 5			|@| 329 ($5=0005)
	add	$6, $0, -1		; $6 = -1			|@| 330 ($6=FFFF)
	add	$7, $0, 1		; $7 = 1			|@| 331 ($7=0001)
					;
	s.ne	$2, $3			; test skips			|@| 332 ($1=F00D)
	add	$1, $1, 1		; we shouldn't hit any adds
	s.gt	$7, $6			;				|@| 334 ($1=F00D)
	add	$1, $1, 1		;
	s.gte	$2, $7			;				|@| 336 ($1=F00D)
	add	$1, $1, 1		;
	s.lt	$4, $5			;				|@| 338 ($1=F00D)
	add	$1, $1, 1		;
	s.lte	$6, $2			;				|@| 340 ($1=F00D)
	add	$1, $1, 1		;
	s.ult	$7, $6			;				|@| 342 ($1=F00D)
	add	$1, $1, 1		;
	s.ulte	$7, $2			;				|@| 344 ($1=F00D)
	add	$1, $1, 1		;
					;
	jmp	0			;
					;
count_bits:				;				|@|  83 ($1=F171)
	.push	$1			; preserve $1			|@|  84 ($7=001F)
					;				<memory test>
	ldw	$1, 2($7)		; $1 = argument = 0xF171	|@|  86 ($1=F171)
	.push	$2			; preserve $2			|@|  87 ($7=001E)
					;				<memory test>
	.push	$3			; preserve $3			|@|  89 ($7=001D)
					;				<memory test>
	.push	$4			; preserve $4			|@|  91 ($7=001C)
					;				<memory test>
	add	$2, $0, $0		; $2 = 0			|@|  93 ($2=0000)
	.ldi	$4, 16			; $4 = 16 (bits)		|@|  95 ($4=0010)
1:	and	$3, $1, 1		; $3 = $1 & 1			|@|  96 ($3=0001)
	s.eq	$3, $0			; skip if 0
	add	$2, $2, 1		; inc $2			|@|  98 ($2=0001)
	shr	$1, $1, 1		; $1 = $1 >> 1			|@|  99 ($1=78B8)
	as.z	$4, $4, -1		; dec $4, skip when done	|@| 100 ($4=000F)
	jmp	1b			; loop				|@| 221 ($1=0000 $2=0009 $3=0001 $4=0000)
	.pop	$4			; restore $4			|@| 222 ($4=0000)
					;				|@| 223 ($7=001D)
	stw	4($7), $2		; result = $2 = 9		<memory test>
	.pop	$3			; restore $3			|@| 225 ($3=00FF)
					;				|@| 226 ($7=001E)
	.pop	$2			; restore $2			|@| 227 ($2=FFFF)
					;				|@| 228 ($7=001F)
	.pop	$1			; restore $1			|@| 229	($1=F171)
					;				|@| 230 ($7=0020)
	.pop	$5			; .ret				|@| 231 ($5=002E)
					;				|@| 232 ($7=0021)
	jmp	$5			;
