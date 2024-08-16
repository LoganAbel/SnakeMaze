import pygame as pg
import math
import GUI
from mat_lib.vector import Vec2
from mat_lib.rect import Rect
from resources import Res
from components.tiles import *

class Editor:
	def startup(self, level_i):
		self.saved = level_i < len(Res.level_file.level_headers)
		self.next_state = None
		self.level_i = level_i
		self.editor_level = EditorLevel(Res.level_file.load(level_i))
		self.editor_menu = EditorMenu()
	def cleanup(self):
		pass
	def on_event(self, e):
		if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
			self.next_state = "EditorSelector"
			return
		if e.type == pg.KEYDOWN and e.key == pg.K_s and pg.key.get_pressed()[pg.K_LCTRL]:
			Res.level_file.save(self.editor_level.level, self.level_i)
			self.saved = True
			return
		self.editor_menu.on_event(e, self)
	def update(self):
		pass
	def draw(self, screen):
		screen.fill(Res.colors["black0"])
		inner_rect = self.editor_menu.draw(screen, self)
		level_scr = screen.subsurface(inner_rect.tuple())
		self.editor_level.draw(level_scr, self)
		screen.unlock()

class EditorMenu:
	def __init__(self):
		self.items = ["floor_item", "apple", "wall_item", "snake_body", "portal0", "lever0", "togglewall0", "tele", "poison"]
		self.item_classes = [Floor, Apple, Wall, Snake, Portal, Lever, ToggleWall, Tele, Poison]
		self.tabs = ["settings", "edit"]
		self.selected_item = 0
		self.buttons = GUI.Buttons()
		self.selected_tab = 1
		self.title_selected = False

	def on_event(self, e, editor):
		if e.type == pg.KEYDOWN and self.title_selected:
			header = editor.editor_level.level.header
			if e.key == pg.K_BACKSPACE:
				header.name = header.name[:-1]
			else:
				header.name += e.unicode
			editor.saved = False

	def draw(self, screen, editor):
		if pg.mouse.get_pressed()[0] and not self.buttons.old_mouse_down:
			self.title_selected = False

		mousep = Vec2(*pg.mouse.get_pos())
		rect = Rect(Vec2(0, 0), Vec2.surface_dim(screen))

		outline_size = 4
		item_size = 32

		# tabs display
		rect, tab_disp_rect = rect.split_h(-outline_size)

		pg.draw.rect(screen, Res.colors["black2"], tab_disp_rect.tuple())
		# to modify
		selected_tab_rect = Rect(tab_disp_rect.start + Vec2(0, self.selected_tab * (item_size + outline_size)),
			dim = Vec2(tab_disp_rect.dim().x, item_size + outline_size * 2))
		pg.draw.rect(screen, Res.colors["white"], selected_tab_rect.tuple())

		# tab menu
		rect, tab_menu_rect = rect.split_h(-item_size-outline_size*2)

		pg.draw.rect(screen, Res.colors["black2"], tab_menu_rect.tuple())

		tab_rect = tab_menu_rect.copy().set_dim(Vec2(tab_menu_rect.dim().x)).margin(outline_size)

		for i, tab in enumerate(self.tabs):
			img = Res.sheet.subsurface(tab)
			img = pg.transform.scale(img, (item_size, item_size))
			if pg.mouse.get_pressed()[0] and tab_rect.contains_p(mousep):
				self.selected_tab = i
			screen.blit(img, tab_rect.tuple())
			tab_rect += Vec2(0, item_size + outline_size)

		# save button
		if not editor.saved:
			img = Res.sheet.subsurface("save")
			img = pg.transform.scale(img, (item_size, item_size))
			_, save_rect = tab_menu_rect.split_v(-item_size-outline_size*2)
			save_rect = save_rect.margin(outline_size)
			if self.buttons.update("save", save_rect) == "up":
				Res.level_file.save(editor.editor_level.level, editor.level_i)
				editor.saved = True
			screen.blit(img, save_rect.tuple())

		# item menu
		if self.tabs[self.selected_tab] == "edit":
			outline_size = 4
			item_size = 64

			rect, item_menu_rect = rect.split_h(-item_size-outline_size*2)

			pg.draw.rect(screen, Res.colors["black3"], item_menu_rect.tuple())

			item_menu_rect.set_dim(item_menu_rect.dim().x)
			item_rect = item_menu_rect.margin(outline_size)

			select_rect = item_menu_rect.copy()
			select_rect += Vec2(0, self.selected_item * (item_size + outline_size))
			pg.draw.rect(screen, Res.colors["white"], select_rect.tuple())
			pg.draw.rect(screen, Res.colors["black3"], select_rect.margin(outline_size).tuple())

			for i, item in enumerate(self.items):
				img = Res.sheet.subsurface(item)
				img = pg.transform.scale(img, (item_size, item_size))
				if pg.mouse.get_pressed()[0] and item_rect.contains_p(mousep):
					self.selected_item = i
				screen.blit(img, item_rect.tuple())
				item_rect += Vec2(0, item_size + outline_size)

		if self.tabs[self.selected_tab] == "settings":
			outline_size = 4
			width = 256

			rect, settings_menu_rect = rect.split_h(-width-outline_size*2)
			pg.draw.rect(screen, Res.colors["black3"], settings_menu_rect.tuple())

			font_size = 16
			font = pg.font.SysFont('Consolas', font_size)
			font_h = font.get_ascent() - font.get_descent()

			title_rect, settings_menu_rect = settings_menu_rect.split_v(font_h * 2 + 20)
			title_rect = title_rect.margin(Vec2(10, 10))
			pg.draw.rect(screen, Res.colors["black2"], title_rect.tuple())
			text = editor.editor_level.level.header.name
			text_bounds = GUI.draw_text_box(screen, '#fafcf1', font, text, title_rect)

			if self.buttons.update("title", title_rect) == "up":
				self.title_selected = True

			if self.title_selected:
				pg.draw.rect(screen, Res.colors["white"], Rect(
					Vec2(text_bounds.end.x, text_bounds.start.y), 
					Vec2(text_bounds.end.x + 2, text_bounds.end.y)
				).tuple())

			dim_rect, settings_menu_rect = settings_menu_rect.split_v(settings_menu_rect.dim().x)
			dim_rect = dim_rect.margin(10)

			def put_tri_in_rect(rect, is_vertical, id):
				triangle = (
					rect.start.tuple(), 
					(rect.end.x, (rect.end.y + rect.start.y) / 2) if is_vertical 
					else ((rect.end.x + rect.start.x) / 2, rect.end.y),
					(rect.start.x, rect.end.y) if is_vertical else (rect.end.x, rect.start.y)
				)
				pg.draw.polygon(screen, Res.colors["black1"], triangle)

				if self.buttons.update(id, lambda mousep: mousep.in_triangle(*triangle)) == "up":
					level = editor.editor_level.level
					dir, dx, dy = id
					new_dim = Vec2(level.map.dim.x + dx, level.map.dim.y + dy)
					if new_dim.x < 0 or new_dim.y < 0:
						return
					level.resize(dir, new_dim)
					editor.saved = False

			# todo
			size = dim_rect.dim().x
			tri_dim = Vec2(size / 3, size / 6) # horizontal
			put_tri_in_rect(dim_rect.align(tri_dim, Vec2(0, -1)).flip(), False,	        (0, 0, 1))
			put_tri_in_rect(dim_rect.align(tri_dim.trans(), Vec2(-1, 0)).flip(), True,  (0, 1, 0))
			put_tri_in_rect(dim_rect.align(tri_dim, Vec2(0, 1)), False,	                (1, 0, 1))
			put_tri_in_rect(dim_rect.align(tri_dim.trans(), Vec2(1, 0)), True,          (1, 1, 0))
			dim_rect = dim_rect.margin(tri_dim.x + (size - 4 * tri_dim.x) / (2 + 2 ** .5))
			put_tri_in_rect(dim_rect.align(tri_dim, Vec2(0, -1)), False,                (0, 0, -1))
			put_tri_in_rect(dim_rect.align(tri_dim.trans(), Vec2(-1, 0)), True,         (0, -1, 0))
			put_tri_in_rect(dim_rect.align(tri_dim, Vec2(0, 1)).flip(), False,          (1, 0, -1))
			put_tri_in_rect(dim_rect.align(tri_dim.trans(), Vec2(1, 0)).flip(), True,   (1, -1, 0))

		self.buttons.update_all()

		return rect
		
class EditorLevel:
	def __init__(self, level):
		self.level = level
		self.prev_p = None
		self.prev_tile = None

	def update_mouse(self, screen, mousep, editor):
		if not pg.mouse.get_pressed()[0] \
		or not Rect(Vec2(0), Vec2(1)).contains_p(mousep) \
		or editor.editor_menu.tabs[editor.editor_menu.selected_tab] != "edit": 
			self.prev_p = None
			return

		mousep = (mousep * self.level.map.dim).floor()
		if self.level.map[mousep] == None: return
		item_class = editor.editor_menu.item_classes[editor.editor_menu.selected_item]
		if item_class != None and item_class.Editor(self.level, mousep, self.prev_p):
			editor.saved = False

		self.prev_p = mousep

	def draw(self, screen, editor):
		mousep = Vec2(*pg.mouse.get_pos())
		level_scr = self.level.draw()

		screen_dim = Vec2.surface_dim(screen)
		level_dim = Vec2.surface_dim(level_scr)
		scale = (screen_dim-(self.level.map.dim+1)) / level_dim
		scale = min(scale.x, scale.y)
		level_scr = pg.transform.scale(level_scr, (level_dim * math.ceil(scale)).tuple())
		level_dim *= int(scale * Res.tilesize) / Res.tilesize
		level_scr = pg.transform.smoothscale(level_scr, level_dim.tuple())

		new_level_dim = level_dim+self.level.map.dim+1
		new_level_scr = pg.Surface(new_level_dim.tuple())
		new_level_scr.fill(Res.colors["white"])

		step = level_dim / self.level.map.dim

		for p in self.level.map.dim.range():
			new_level_scr.blit(level_scr, (p*(step+1)+1).tuple(), 
				Rect(p*step, dim=Vec2(step)).tuple())

		new_level_pos = (screen_dim - new_level_dim) // 2
		screen.blit(new_level_scr, new_level_pos.tuple())

		mousep = (mousep - new_level_pos) / new_level_dim
		self.update_mouse(screen, mousep, editor)