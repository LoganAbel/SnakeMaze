import pygame as pg
import GUI
from resources import Res
from mat_lib.vector import Vec2
from mat_lib.rect import Rect

class MainMenu:
	def startup(self, persistent):
		self.next_state = None
		self.buttons = GUI.Buttons()
	def cleanup(self):
		pass
	def on_event(self, e):
		pass
	def update(self):
		pass
	def draw(self, screen):
		screen_rect = Rect.from_surface(screen)

		size = max(min(screen_rect.dim().x, screen_rect.dim().y) // 8, 48)
		margin = size / 3

		rect = screen_rect.align(Vec2(size*2, size*2+margin), Vec2(0))

		game_rect, _ = rect.split_v(size)
		_, editor_rect = rect.split_v(-size)

		if self.buttons.update("GameSelector", game_rect) == "up":
			self.next_state = "GameSelector"
			return

		if self.buttons.update("EditorSelector", editor_rect) == "up":
			self.next_state = "EditorSelector"
			return

		screen.fill(Res.colors["black0"])

		pg.draw.rect(screen, Res.colors["green"], game_rect.tuple(), border_radius = int(game_rect.dim().x/4))
		pg.draw.rect(screen, Res.colors["purple"], editor_rect.tuple(), border_radius = int(editor_rect.dim().x/4))

		font = pg.font.SysFont('Consolas', size//2)
		GUI.draw_text_box(screen, Res.colors["white"], font, 'Play', game_rect)
		GUI.draw_text_box(screen, Res.colors["white"], font, 'Edit', editor_rect)

		self.buttons.update_all()