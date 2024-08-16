from resources import Res
import GUI
from mat_lib.vector import Vec2
from mat_lib.rect import Rect
import pygame as pg
import math

class GameSelector:
	def __init__(self):
		pass
	def startup(self, persistent):
		self.next_state = None
		self.selected = None
		self.buttons = GUI.Buttons()
	def cleanup(self):
		return self.selected
	def on_event(self, e):
		if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
			self.next_state = "MainMenu"
			return
	def update(self):
		pass
	def draw(self, screen):
		screen_dim = Vec2.surface_dim(screen)
		screen_rect = Rect.from_surface(screen)

		level_count = len(Res.level_file.level_headers)

		# level_count = min(level_count, 12)

		calc_size = lambda w, h: min(screen_rect.dim().x/w,screen_rect.dim().y/h)
		w = (level_count*screen_rect.dim().x/screen_rect.dim().y)**.5
		if w > level_count:
			w = level_count
			h = 1
			size = calc_size(w, h)
		if w < 1:
			w = 1
			h = level_count
			size = calc_size(w, h)
		else:
			w_a = math.floor(w)
			h_a = math.ceil(level_count/w_a)
			size_a = calc_size(w_a, h_a)
			w_b = math.ceil(w)
			h_b = math.ceil(level_count/w_b)
			size_b = calc_size(w_b, h_b)
			if size_a > size_b:
				w = w_a
				h = h_a
				size = size_a
			else:
				w = w_b
				h = h_b
				size = size_b

		dim = Vec2(w, h)
		level_rect = screen_rect.align(dim * size, Vec2(0))
		level_rect.set_dim(size)

		font = pg.font.SysFont('Consolas', int(size*.2))

		screen.fill(Res.colors["black0"])

		i = 0
		for p in dim.range():
			rect = level_rect.trans(Rect(p+.1, p+.9))
			pg.draw.rect(screen, Res.colors["green"], rect.tuple(), border_radius = int(rect.dim().x/4))

			text = to_roman(i+1)
			GUI.draw_text_box(screen, Res.colors["white"], font, text, rect)

			if self.buttons.update(i, rect) == "up":
				self.next_state = "Game"
				self.selected = i
				return

			i += 1
			if i >= level_count:
				break

		self.buttons.update_all()

def to_roman(n):
	str = ''
	for (val, char) in (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I'):
		char *= int(n / val)
		n -= val * len(char)
		str += char
	return str