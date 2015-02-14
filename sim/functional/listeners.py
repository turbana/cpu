
class StopClock(object):
	def __init__(self, cpu, clock):
		self.cpu = cpu
		self.clock = clock

	def before_fetch(self, _):
		if self.clock == self.cpu.clock:
			self.cpu.halt = True
