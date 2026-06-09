from time import time_ns

class Misc:
	@staticmethod
	def timeMS() -> int:
		return time_ns() // 1_000_000
