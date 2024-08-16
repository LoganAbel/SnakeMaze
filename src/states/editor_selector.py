from resources import Res
import GUI
from mat_lib.vector import Vec2
from mat_lib.rect import Rect
import pygame as pg
import math

class EditorSelector:
	def __init__(self):
		pass
	def startup(self, persistent):
		self.next_state = None
		self.selected = None
		self.buttons = GUI.Buttons()
		self.click_mouse_y = 0
		self.offset = 0
	def cleanup(self):
		return self.selected
	def on_event(self, e):
		if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
			self.next_state = "MainMenu"
			return
		if e.type == pg.MOUSEWHEEL:
		   self.offset -= e.y * 20
		   return
	def update(self):
		pass
	def draw(self, screen):
		screen_rect = Rect.from_surface(screen)
		screen.fill(Res.colors["black0"])

		rect_h = 48
		margin = rect_h / 3
		level_count = len(Res.level_file.level_headers)

		self.offset = max(0, min(self.offset, margin + (margin + rect_h) * (level_count + 1) - screen_rect.dim().y))
		screen_rect -= Vec2(0, self.offset)

		rect = screen_rect.align(Vec2(min(screen_rect.dim().x * .95, 640), rect_h), Vec2(0, -1))
		rect += Vec2(0, margin)

		font = pg.font.SysFont('Consolas', int(rect.dim().y*.5))
		font_h = font.get_ascent()

		for i in range(level_count):
			# number
			move_rect = rect.copy()
			number_rect, move_rect = move_rect.split_h(font.size("XXXXX")[0])

			GUI.draw_text_box(screen, Res.colors["white"], font, to_roman(i+1), number_rect, align=1, margin=font.size("X")[0])

			if self.buttons.clicked == f"move{i}":
				move_rect += Vec2(0, pg.mouse.get_pos()[1] - self.click_mouse_y)

			pg.draw.rect(screen, Res.colors["purple"], move_rect.tuple())

			def left_line(rect):
				pg.draw.line(screen, Res.colors["black1"], (rect.start.x, rect.start.y+4), (rect.start.x, rect.end.y-4), width = 2)

			# play button section
			move_rect, play_rect = move_rect.split_h(- move_rect.dim().y)
			left_line(play_rect)
			GUI.draw_text_box(screen, Res.colors["white"], font, '>', play_rect)
			if self.buttons.update(f"play{i}", play_rect) == "up":
				self.next_state = "Editor"
				self.selected = i
				return

			# delete section
			delete_rect, move_rect = move_rect.split_h(move_rect.dim().y)
			GUI.draw_text_box(screen, Res.colors["red"], font, 'x', delete_rect)
			if self.buttons.update(f"delete{i}", delete_rect) == "up":
				Res.level_file.delete(i)
				self.buttons = GUI.Buttons()
				return

			#dragable section
			left_line(move_rect)
			if self.buttons.update(f"move{i}", move_rect) == "down":
				self.click_mouse_y = pg.mouse.get_pos()[1]
			if self.buttons.update(f"move{i}", move_rect) == "up":
				dy = pg.mouse.get_pos()[1] - self.click_mouse_y
				dy /= margin + rect_h
				new_i = max(0, min(level_count, int(i + dy + 1)))
				if i != new_i:
					Res.level_file.move(i, new_i)

			# level name
			text = Res.level_file.level_headers[i].name
			GUI.draw_text_box(screen, Res.colors["white"], font, text, move_rect, align=-1, margin=font_h / 2)

			rect += Vec2(0, margin + rect.dim().y)

		# new level box
		i = level_count
		pg.draw.rect(screen, Res.colors["purple"], rect.tuple())
		GUI.draw_text_box(screen, Res.colors["white"], font, '+', rect)
		if self.buttons.update("new", rect) == "up":
			self.next_state = "Editor"
			self.selected = i
			return

		self.buttons.update_all()

def to_roman(n):
	str = ''
	for (val, char) in (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I'):
		char *= int(n / val)
		n -= val * len(char)
		str += char
	return str