import pygame as pg
import math
from mat_lib.vector import Vec2
from resources import Res

class Game:
	def startup(self, level_i):
		self.next_state = None
		self.level_i = level_i
		self.level = Res.level_file.load(level_i)
		self.level_start = self.level.copy()
	def cleanup(self):
		pass
	def on_event(self, e):
		if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
			self.next_state = "GameSelector"
			return
		if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
			self.level = self.level_start.copy()
			return
		self.level.on_event(e)
	def update(self):
		self.level.update()
		if self.level.done:
			if self.level_i == len(Res.level_file.level_headers)-1:
				self.next_state = "GameSelector"
			else:
				self.cleanup()
				self.startup(self.level_i+1)

	def draw(self, screen):
		level_scr = self.level.draw()
		screen.fill(Res.colors["black0"])
		fit_screen(screen, level_scr)

def fit_screen(parent, child):
	child_dim = Vec2.surface_dim(child)
	parent_dim = Vec2.surface_dim(parent)

	# scale child
	scale = parent_dim / child_dim
	scale = min(scale.x, scale.y)
	# if int(scale) > 0:
	# 	scale = int(scale)
	# 	child_dim *= scale
	# 	child = pg.transform.scale(child, child_dim.tuple())
	# else:
	# 	child_dim *= scale
	# 	child = pg.transform.smoothscale(child, child_dim.tuple())
	child = pg.transform.scale(child, (child_dim * math.ceil(scale)).tuple())
	child_dim *= scale
	child = pg.transform.smoothscale(child, child_dim.tuple())

	# center child
	offset = (parent_dim - child_dim) // 2
	parent.blit(child, offset.tuple())