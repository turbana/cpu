
@macro("iden u16")
def test(name, value):
	return """
			.data
	{name}:	.word		{value}
			.text
	load_{name}:
			.enter		0
			.ldi		$2, {name}
			ldw			$1, 0($2)
			.leave
			.set		latest, load_{name}
			.set		count, count + 1
	"""
