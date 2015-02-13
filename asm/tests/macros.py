
@macro("iden u16")
def test(iden, n):
	return """
			.data
	{name}:	.dw			{value}
			.text
	load_{name}:
			.ldi		$2, {name}
			ldw			$1, 0($2)
			.ret		$6
			.set		latest, load_{name}
			.set		count, count + 1
	""".format(name=iden, value=n)
