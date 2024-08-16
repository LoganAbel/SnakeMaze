import pygame as pg
# from pygame._sdl2 import Window
from resources import Res
from states.game import Game
from states.editor import Editor
from states.game_selector import GameSelector
from states.editor_selector import EditorSelector
from states.main_menu import MainMenu

class StateManager:
	def __init__(self, states, state):
		self.states = states
		self.state = states[state]
		self.state.startup(None)
	def update(self):
		self.state.update()
		if self.state.next_state != None:
			new_state = self.states[self.state.next_state]
			new_state.startup(self.state.cleanup())
			self.state = new_state
	def on_event(self, e):
		self.state.on_event(e)
	def draw(self, screen):
		self.state.draw(screen)


class Main:
	def __init__(self, title):
		pg.init()

		pg.display.set_caption(title)
		self.fullscreen = False
		self.dim = (1080, 720)
		self.screen = pg.display.set_mode(self.dim, pg.RESIZABLE)
		# Window.from_display_module().maximize()
		self.clock = pg.time.Clock()

		Res.init()

		self.state_manager = StateManager({
			"GameSelector": GameSelector(),
			"EditorSelector": EditorSelector(),
			"Game": Game(),
			"Editor": Editor(),
			"MainMenu": MainMenu(),
		}, "MainMenu")

	def set_display(self):
		self.screen = pg.display.set_mode(self.dim, pg.FULLSCREEN if self.fullscreen else pg.RESIZABLE)

	def update(self):
		for e in pg.event.get():
			if e.type == pg.QUIT:
				pg.quit()
				exit()
			if e.type == pg.KEYDOWN and e.key == pg.K_F11:
				self.fullscreen = not self.fullscreen
				if self.fullscreen:
					self.dim = pg.display.get_surface().get_size()
				self.set_display()
			self.state_manager.on_event(e)

		self.state_manager.update()
		self.state_manager.draw(self.screen)

	def main(self):
		while 1:
			self.update()
			
			self.clock.tick(60)
			pg.display.flip()

Main("Snake 2.0").main()