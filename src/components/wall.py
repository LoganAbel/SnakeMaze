import pygame as pg
from resources import Res
from mat_lib.rect import Rect
from mat_lib.vector import Vec2
from components.snake import Snake

class Wall:
	id = 1
	def init(self, map):
		self.screen = Wall._floor_img(map.dim)
		mask = self._mask_img(map)

		screen_dim = Vec2.surface_dim(self.screen)

		img = pg.Surface(screen_dim.tuple())

		# mask outline
		mask_inv = img
		mask_inv.fill('#ffffff')
		mask_inv.blit(mask, (0,0), special_flags=pg.BLEND_RGB_SUB)
		mask_outline = pg.Surface(screen_dim.tuple())
		for d in ((0,1), (0,-1), (-1,0), (1,0)):
			mask_outline.blit(mask_inv, d, special_flags=pg.BLEND_RGB_ADD)
		mask_outline.blit(mask, (0, 0), special_flags=pg.BLEND_RGB_MULT)

		# wall shadow
		img.fill(Res.colors["black1"])
		img.blit(mask, (0, 0), special_flags=pg.BLEND_RGB_MULT)
		img.set_colorkey(pg.Color(0, 0, 0))
		self.screen.blit(img, (2, 2))

		#wall
		img.fill(Res.colors["purple"])
		img.blit(mask, (0, 0), special_flags=pg.BLEND_RGB_MULT)
		img.set_colorkey(pg.Color(0, 0, 0))
		self.screen.blit(img, (0, 0))

		# wall outline
		img.fill(Res.colors["black0"])
		img.blit(mask_outline, (0, 0), special_flags=pg.BLEND_RGB_MULT)
		img.set_colorkey(pg.Color(0, 0, 0))
		self.screen.blit(img, (0, 0))

	def set_level(self, level):
		self.level = level

	def copy(self):
		return self

	def _mask_img(self, map):
		img = pg.Surface(Vec2.surface_dim(self.screen).tuple())
		black = pg.Color(0, 0, 0)
		white = pg.Color(255, 255, 255)
		for p in map.dim.range():
			id = map[p]

			is_wall = map[p] == self

			if is_wall:
				pg.draw.rect(img, white, Rect(p*Res.tilesize, dim=Vec2(Res.tilesize)).tuple())

			for d1 in (-1,1):
				for d2 in (-1,1):
					if (map[p+Vec2(0,-d2)] in (self, None)) == is_wall:
						continue
					if (map[p+Vec2(-d1,0)] in (self, None)) == is_wall:
						continue
					if not is_wall and not map[p+Vec2(-d1,-d2)] in (self, None):
						continue

					color = black if is_wall else white

					d = Vec2(d1, d2)
					pos = p * Res.tilesize + (d < 0) * (Res.tilesize - 1)
					img.set_at((pos+d).tuple(), color)
					pg.draw.line(img, color, pos.tuple(), (pos+d*Vec2(3,0)).tuple())
					pg.draw.line(img, color, pos.tuple(), (pos+d*Vec2(0,3)).tuple())
					# tile = "bevel_outer" if is_wall else "bevel_inner"
					# Res.sheet.blit(img, (p + (d < 0) * .5)*Res.tilesize, tile, flip=d)

		return img

	def _floor_img(dim):
		img = pg.Surface((dim * Res.tilesize).tuple())
		for p in dim.range():
			color = Res.colors[f"black{2+int((p.x+p.y)%2)}"]
			rect = Rect(p*Res.tilesize, dim=Vec2(Res.tilesize))
			pg.draw.rect(img, color, rect.tuple())
		return img

	def update(self, level):
		pass
	def on_event(self, e):
		pass
	def draw(self, screen):
		screen.blit(self.screen, (0, 0))

	def on_colide(self, level, other, pos):
		if type(other) == Snake:
			other.kill()
	def remove(self, level, pos):
		from components.items import Floor
		level.map[pos] = Floor
		self.init(level.map)

	def add(self, level, pos):
		level.map[pos] = self
		self.init(level.map)

	def move(self, dpos):
		pass

	def Editor(level, pos, old_p):
		if type(level.map[pos]) == Wall:
			return False
		level.map[pos].remove(level, pos)
		level.map2[pos].remove(level, pos)
		wall = next(object for object in level.objects if type(object) == Wall)
		wall.add(level, pos)
		return True