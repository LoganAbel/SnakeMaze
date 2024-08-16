import pygame as pg
from resources import Res
from components.wall import Wall
from components.snake import Snake
from mat_lib.vector import Vec2
from mat_lib.rect import Rect

class Floor:
	id = 0
	def on_colide(level, other, pos):
		pass
	def set_level(self, level):
		self.level = level
	def remove(level, pos):
		pass
	def copy():
		return Floor
	def move(dpos):
		pass
	def Editor(level, pos, old_p):
		if level.map[pos] == Floor\
		and level.map2[pos] == Floor:
			return False
		level.map[pos].remove(level, pos)
		level.map2[pos].remove(level, pos)
		return True

class Apple:
	id = 2
	def __init__(self, pos):
		self.pos = pos
	def set_level(self, level):
		self.level = level
	def copy(self):
		return Apple(self.pos)
	def update(self, level):
		pass
	def on_event(self, e):
		pass
	def draw(self, screen):
		Res.sheet.blit(screen, self.pos*Res.tilesize, "apple")
	def on_colide(self, level, other, pos):
		if type(other) == Snake:
			other.grow()
			self.remove(level, pos)
	def remove(self, level, pos):
		level.objects.remove(self)
		level.map[pos] = Floor
		level.apple_count -= 1
	def move(self, dpos):
		self.pos += dpos
	def Editor(level, pos, old_p):
		if type(level.map[pos]) == Apple: return False
		level.map[pos].remove(level, pos)
		level.map2[pos].remove(level, pos)
		apple = Apple(pos)
		level.map[pos] = apple
		level.objects.append(apple)
		apple.set_level(level)
		level.apple_count += 1
		return True

class Poison:
	id = 8
	def __init__(self, pos):
		self.pos = pos
	def set_level(self, level):
		self.level = level
	def copy(self):
		return Poison(self.pos)
	def update(self, level):
		pass
	def on_event(self, e):
		pass
	def draw(self, screen):
		Res.sheet.blit(screen, self.pos*Res.tilesize, "poison")
	def on_colide(self, level, other, pos):
		if type(other) == Snake:
			other.shrink(level)
			self.remove(level, pos)
	def remove(self, level, pos):
		level.objects.remove(self)
		level.map[pos] = Floor
	def move(self, dpos):
		self.pos += dpos
	def Editor(level, pos, old_p):
		if type(level.map[pos]) == Poison: return False
		level.map[pos].remove(level, pos)
		level.map2[pos].remove(level, pos)
		apple = Poison(pos)
		level.map[pos] = apple
		level.objects.append(apple)
		apple.set_level(level)
		return True

class Portal:
	id = 3
	def __init__(self, pos):
		self.pos = pos
	def set_level(self, level):
		self.level = level
	def copy(self):
		return Portal(self.pos)
	def update(self, level):
		pass
	def on_event(self, e):
		pass
	def draw(self, screen):
		Res.sheet.blit(screen, self.pos*Res.tilesize, f"portal{int(self.level.apple_count == 0)}")
	def on_colide(self, level, other, pos):
		if type(other) == Snake:
			if self.level.apple_count == 0:
				other.win()
			else:
				other.kill()
	def remove(self, level, pos):
		level.objects.remove(self)
		level.map[pos] = Floor
	def move(self, dpos):
		self.pos += dpos
	def Editor(level, pos, old_p):
		if type(level.map[pos]) == Portal: return False
		level.map[pos].remove(level, pos)
		level.map2[pos].remove(level, pos)
		portal = Portal(pos)
		level.map[pos] = portal
		level.objects.append(portal)
		portal.set_level(level)
		return True

class Tele:
	id = 7
	def __init__(self, pos):
		self.pos = pos
	def set_level(self, level):
		self.level = level
		self.shape = []
		stack = [Vec2(0,0)]
		while len(stack) > 0:
			self.shape += stack
			old_stack = stack
			stack = []
			for pos in old_stack:
				for d in (Vec2(1,0), Vec2(-1,0), Vec2(0,1), Vec2(0,-1)):
					adj = pos + d
					if adj not in self.shape and type(self.level.map[adj+self.pos]) == Tele:
						stack.append(adj)

	def copy(self):
		return Tele(self.pos)
	def update(self, level):
		pass
	def on_event(self, e):
		pass
	def draw(self, screen):
		Res.sheet.blit(screen, self.pos*Res.tilesize, "tele")
		# for p in self.level.map2.dim.range():
		# 	if type(self.level.map2[p]) == Snake:
		# 		pg.draw.rect(screen, Res.colors["red"], Rect(p*Res.tilesize, dim=Vec2(Res.tilesize)).tuple())
	def on_colide(self, level, other, pos):
		if type(other) == Snake:
			def can_tele(obj):
				if type(obj) != Tele: return False
				if obj == self: return False
				if type(level.map[obj.pos + other.dir]) in (Wall, Tele): return False
				if len(self.shape) != len(obj.shape): return False
				for dpos in self.shape:
					dpos = dpos * (1 - (abs(other.dir) > 0) * 2)
					if type(level.map[obj.pos + dpos]) != Tele:
						return False
					if obj.pos + dpos == self.pos:
						return False
				return True
			teles = [obj for obj in level.objects if can_tele(obj)]
			if len(teles) > 0:
				other.body.insert(0,pos)
				# level.map2[pos] = other
				other.body.insert(0,teles[0].pos)
				other.shrink(level)
				other.shrink(level)
				# level.map2[teles[0].pos] = other
				other.body[0].cut = True
				other.move_state = "colide"
			else:
				other.kill()
			# todo
	def remove(self, level, pos):
		level.objects.remove(self)
		level.map[pos] = Floor
	def move(self, dpos):
		self.pos += dpos
	def Editor(level, pos, old_p):
		if type(level.map[pos]) == Tele: return False
		level.map[pos].remove(level, pos)
		level.map2[pos].remove(level, pos)
		tele = Tele(pos)
		level.map[pos] = tele
		level.objects.append(tele)
		tele.set_level(level)
		return True

class ToggleWall:
	id1 = 4
	id2 = 6
	def __init__(self, pos, fliped):
		self.pos = pos
		self.fliped = fliped
	def set_level(self, level):
		self.level = level
	def copy(self):
		return ToggleWall(self.pos, self.fliped)
	def update(self, level):
		pass
	def on_event(self, e):
		pass
	def draw(self, screen):
		Res.sheet.blit(screen, self.pos*Res.tilesize, f"togglewall{int(self.fliped == self.level.button_down)}")
	def on_colide(self, level, other, pos):
		if type(other) == Snake:
			if self.fliped != self.level.button_down:
				other.kill()
	def remove(self, level, pos):
		level.objects.remove(self)
		level.map[pos] = Floor
	def move(self, dpos):
		self.pos += dpos
	def Editor(level, pos, old_p):
		if type(level.map[pos]) == ToggleWall: 
			if old_p != None: return False
			level.map[pos].fliped = not level.map[pos].fliped
			return True
		level.map[pos].remove(level, pos)
		level.map2[pos].remove(level, pos)
		toggle_wall = ToggleWall(pos, True)
		level.map[pos] = toggle_wall
		level.objects.append(toggle_wall)
		toggle_wall.set_level(level)
		return True

class Lever:
	id = 5
	def __init__(self, pos):
		self.pos = pos
	def set_level(self, level):
		self.level = level
	def copy(self):
		return Lever(self.pos)
	def update(self, level):
		pass
	def on_event(self, e):
		pass
	def draw(self, screen):
		Res.sheet.blit(screen, self.pos*Res.tilesize, f"lever{int(self.level.button_down)}")
	def on_colide(self, level, other, pos):
		if type(other) == Snake:
			self.level.button_down = not self.level.button_down
	def remove(self, level, pos):
		level.objects.remove(self)
		level.map[pos] = Floor
	def move(self, dpos):
		self.pos += dpos
	def Editor(level, pos, old_p):
		if type(level.map[pos]) == Lever: return False
		level.map[pos].remove(level, pos)
		level.map2[pos].remove(level, pos)
		lever = Lever(pos)
		level.map[pos] = lever
		level.objects.append(lever)
		lever.set_level(level)
		return True