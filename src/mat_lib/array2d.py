class Array2d():
	def __init__(self, dim, data=None):
		self.dim = dim
		self.data = data or [None] * self.dim.x * self.dim.y
	def __getitem__(self, pos):
		if pos.x < 0 or pos.x >= self.dim.x\
		or pos.y < 0 or pos.y >= self.dim.y:
			return None
		return self.data[int(pos.x + pos.y * self.dim.x)]
	def __setitem__(self, pos, val):
		if pos.x < 0 or pos.x >= self.dim.x\
		or pos.y < 0 or pos.y >= self.dim.y:
			return None
		self.data[int(pos.x + pos.y * self.dim.x)] = val
	def __iter__(self):
		for p in self.dim.range():
			yield self[p]
	def enumerate(self):
		return zip(self.dim.range(), self)