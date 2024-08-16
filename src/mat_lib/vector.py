import math

class Vec2:
	def __init__(self, x, y=None):
		if type(x) is Vec2:
			y = x.y
			x = x.x
		if y is None:
			y = x
		self.x = x
		self.y = y
	def surface_dim(surface): # pygame extension
		return Vec2(surface.get_width(), surface.get_height())
	def copy(self):
		return Vec2(self.x, self.y)
	def tuple(self):
		return (self.x, self.y)
	def trans(self):
		return Vec2(self.y, self.x)
	def __abs__(self):
		return Vec2(abs(self.x), abs(self.y))
	def abs(self):
		return Vec2(abs(self.x), abs(self.y))
	def range(self):
		for y in range(int(self.y)):
			for x in range(int(self.x)):
				yield Vec2(x, y)
	def len(self):
		return (self.x * self.x + self.y * self.y) ** .5
	def dot(self, vec2):
		vec2 = Vec2(vec2)
		return self.x * vec2.x + self.y * vec2.y
				
	def min(*vecs):
		return Vec2(min(v.x for v in vecs), min(v.y for v in vecs))
	def max(*vecs):
		return Vec2(max(v.x for v in vecs), max(v.y for v in vecs))
	def __round__(self):
		return Vec2(round(self.x), round(self.y))
	def __abs__(self):
		return Vec2(abs(self.x), abs(self.y))
	def floor(self):
		return Vec2(int(self.x), int(self.y))
	def ceil(self):
		return Vec2(math.ceil(self.x), math.ceil(self.y))
	def normalize(self, r=1):
		return self * (r / (self.x * self.x + self.y * self.y) ** .5)

	def __repr__(self):
		return f"<{self.x},{self.y}>"

	def __eq__(self, vec2):
		if vec2 == None:
			return False
		vec2 = Vec2(vec2)
		return self.x == vec2.x and self.y == vec2.y
	def comp_eq(self, vec2):
		vec2 = Vec2(vec2)
		return Vec2(self.x == vec2.x, self.y == vec2.y)
	def __neg__(self):
		return Vec2(-self.x, -self.y)
	def __gt__(self, vec2):
		vec2 = Vec2(vec2)
		return Vec2(self.x > vec2.x, self.y > vec2.y)
	def __ge__(self, vec2):
		vec2 = Vec2(vec2)
		return Vec2(self.x >= vec2.x, self.y >= vec2.y)
	def __lt__(self, vec2):
		vec2 = Vec2(vec2)
		return Vec2(self.x < vec2.x, self.y < vec2.y)
	def __le__(self, vec2):
		vec2 = Vec2(vec2)
		return Vec2(self.x <= vec2.x, self.y <= vec2.y)
	def __mod__(self, vec2):
		vec2 = Vec2(vec2)
		return Vec2(self.x % vec2.x, self.y % vec2.y)
	def __sub__(self, vec2):
		vec2 = Vec2(vec2)
		return Vec2(self.x - vec2.x, self.y - vec2.y)
	def __add__(self, vec2):
		vec2 = Vec2(vec2)
		return Vec2(self.x + vec2.x, self.y + vec2.y)
	def __rsub__(self, vec2):
		vec2 = Vec2(vec2)
		return Vec2(vec2.x - self.x, vec2.y - self.y)
	def __iadd__(self, vec2):
		vec2 = Vec2(vec2)
		self.x += vec2.x
		self.y += vec2.y
		return self
	def __mul__(self, vec2):
		vec2 = Vec2(vec2)
		return Vec2(self.x*vec2.x, self.y*vec2.y)
	def __rmul__(self, vec2):
		vec2 = Vec2(vec2)
		return Vec2(self.x*vec2.x, self.y*vec2.y)
	def __truediv__(self, vec2):
		vec2 = Vec2(vec2)
		return Vec2(self.x/vec2.x, self.y/vec2.y)
	def __itruediv__(self, vec2):
		vec2 = Vec2(vec2)
		self.x /= vec2.x
		self.y /= vec2.y
		return self
	def __floordiv__(self, vec2):
		vec2 = Vec2(vec2)
		return Vec2(self.x//vec2.x, self.y//vec2.y)

	def in_triangle(self, v1, v2, v3):
		v1 = Vec2(*v1)
		v2 = Vec2(*v2)
		v3 = Vec2(*v3)
		e1 = v2 - v1
		e2 = v3 - v2
		e3 = v1 - v3
		d1 = self - v1
		d2 = self - v2
		d3 = self - v3
		b1 = e1.x * d1.y < e1.y * d1.x
		b2 = e2.x * d2.y < e2.y * d2.x
		b3 = e3.x * d3.y < e3.y * d3.x
		return b1 == b2 and b2 == b3