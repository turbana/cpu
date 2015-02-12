
@macro("iden u16")
def test(iden, n):
	return """
			.data
	%s:		.dw			%s
			.text
	load_%s:
			.ldi		$2, %s
			ldw			$1, 0($2)
			.ret		$6
	""" % (iden, n, iden, iden)
