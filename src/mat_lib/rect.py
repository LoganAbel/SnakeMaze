from mat_lib.vector import Vec2

class Rect:
	def __init__(self, start, end=None, dim=None):
		self.start = start
		if None != dim:
			end = start + dim
		self.end = end
	def __repr__(self):
		return f"Rect(start={self.start}, end={self.end})"
	def from_surface(surface):
		return Rect(Vec2(0, 0), Vec2.surface_dim(surface))
	def set_pos(self, start):
		dim = self.end - self.start
		self.start = start
		self.end = self.start + dim
	def set_dim(self, dim):
		self.end = self.start + dim
		return self
	def dim(self):
		return self.end - self.start
	def copy(self):
		return Rect(self.start.copy(), end=self.end.copy())
	def tuple(self):
		return (self.start.x, self.start.y, self.end.x - self.start.x, self.end.y - self.start.y)
	def trans(self, p):
		return p * (self.end - self.start) + self.start
	def inv_trans(self, p):
		return (p - self.start) / (self.end - self.start)
	def contains_p(self, p):
		return p.x >= self.start.x and p.y >= self.start.y \
		and p.x < self.end.x and p.y < self.end.y
	def split_h(self, x):
		if x < 0:
			x += self.dim().x
		x += self.start.x
		return Rect(self.start.copy(), Vec2(x, self.end.y)), Rect(Vec2(x, self.start.y), self.end.copy())
	def split_v(self, y):
		if y < 0:
			y += self.dim().y
		y += self.start.y
		return Rect(self.start.copy(), Vec2(self.end.x, y)), Rect(Vec2(self.start.x, y), self.end.copy())
	def align(self, dim, align):
		return Rect(self.start 
			+ (self.dim() - dim) / 2 * align.comp_eq(0) 
			+ (self.dim() - dim) * align.comp_eq(1), 
		dim=dim)
	def margin(self, margin1, margin2 = None):
		return Rect(self.start + margin1, self.end - (margin2 if margin2 != None else margin1))

	def __add__(self, vec2):
		return Rect(self.start + vec2, self.end + vec2)
	def __iadd__(self, vec2):
		self.start += vec2
		self.end += vec2
		return self
	def __sub__(self, vec2):
		return Rect(self.start - vec2, self.end - vec2)
	def __mul__(self, vec2):
		return Rect(self.start * vec2, self.end * vec2)
	def __truediv__(self, vec2):
		return Rect(self.start / vec2, self.end / vec2)

	def flip(self):
		self.start, self.end = self.end, self.start
		return self