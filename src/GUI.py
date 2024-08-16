from mat_lib.vector import Vec2
from mat_lib.rect import Rect
import pygame as pg

def draw_text_box(screen, color, font, text, rect, align = 0, margin = 0):
	img = font.render(text, True, color)
	font_h = font.get_ascent() - font.get_descent()
	font_w, _ = font.size(text)
	metrics = font.metrics(text)

	text_rect = rect.align(Vec2(font_w, font_h), Vec2(align, 0))
	if align == -1:
		text_rect += Vec2(margin, 0)
	if align == 1:
		text_rect -= Vec2(margin, 0)
	# pg.draw.rect(screen, "#ff0000", text_rect.tuple())
	screen.blit(img, text_rect.tuple())
	return text_rect

class Buttons:
	def __init__(self):
		self.clicked = None
		self.old_mouse_down = False
	def update_all(self):
		mouse_down = pg.mouse.get_pressed()[0]
		if not mouse_down:
			self.clicked = None
		self.old_mouse_down = mouse_down
	def update(self, id, rect):
		mousep = Vec2(*pg.mouse.get_pos())
		mouse_down = pg.mouse.get_pressed()[0]
		if type(rect) == Rect:
			in_button = rect.contains_p(mousep)
		else:
			in_button = rect(mousep)
		if mouse_down and not self.old_mouse_down:
			if in_button:
				self.clicked = id
				return "down"
		if not mouse_down and self.old_mouse_down:
			if self.clicked == id and in_button:
				return "up"
		return None