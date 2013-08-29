from directives import macro

@macro(1, "foobar")
def foobar(z):
	print z**2

import directives
print directives.macros
