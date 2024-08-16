from mat_lib.vector import Vec2
from mat_lib.rect import Rect
from resources import Res
import components.tiles as TILES
import pygame as pg

class Snake:
	id = 0
	def init(self, body, control):
		self.body = body
		self.dist = 0
		self.dir = Vec2(body[0] - body[1], 0)
		self.move_state = "start"
		self.control = control(self)
		self.state = "play"
		self.next_dir = None
		self.turn_t = None
		self.collision_checked = False
		return self
	def set_level(self, level):
		self.level = level
	def copy(self):
		snake = Snake()
		snake.init([v.copy() for v in self.body], type(self.control))
		return snake
	def on_event(self, e):
		self.control.on_event(e)

	def grow(self):
		self.body.insert(-1, self.body[-2])
	def shrink(self, level):
		if len(self.body) <= 2:
			self.remove(level, self.body[0])
			return
		if len(self.body) < 2 or self.body[-1] != self.body[-2]:
			level.map2[self.body[-1]] = TILES.Floor
		self.body.pop(-1)

	def kill(self):
		self.inc = 0
		self.state = "dead"
	def win(self):
		self.inc = 0
		self.state = "win"

	def on_colide(self, level, other, pos):
		if type(other) == Snake and not (self.body[-1] == pos and self.body[-2] != pos):
			other.kill()

	def draw(self, screen):
		if len(self.body) < 2: return

		def draw_connect(a, b, r, color, offset):
			if hasattr(b, "cut") and b.cut == True:
				return
			a = a + .5
			b = b + .5
			a += offset
			b += offset
			a *= Res.tilesize
			b *= Res.tilesize
			r = r * Res.tilesize
			pg.draw.circle(screen, color, a.tuple(), int(r))
			pg.draw.circle(screen, color, b.tuple(), int(r))
			r -= .5
			if (a-b).len() == 0: return
			dif = (a - b).normalize(r)
			dif = Vec2(dif.y, -dif.x)
			pg.draw.polygon(screen, color, (
				(a + dif).tuple(), (a - dif).tuple(), (b - dif).tuple(), (b + dif).tuple()
			))

		head = self.body[0] + self.dir * self.dist
		if self.state == "win":
			head = self.body[0] + self.dir
		tail = self.body[-1] * (1-self.dist) + self.body[-2] * self.dist
		cells = [tail, *reversed(self.body[:-1]), head]
		# if self.next_dir != None:
		# 	head = head + self.next_dir * (self.dist - self.turn_t)
		# 	cells.append(head)
		cells = [
			cells[i] for i in range(len(cells)) 
			if i == len(cells)-1 or cells[i+1] != cells[i]
		]

		radius = 4/16

		body_color = Res.colors["green"]
		outline_color = Res.colors["black0"]
		eye_color = Res.colors["white"]
		draw_connect(cells[0], cells[1], radius, outline_color, Vec2(1/16,0))
		draw_connect(cells[0], cells[1], radius, outline_color, Vec2(0,1/16))
		draw_connect(cells[0], cells[1], radius, outline_color, Vec2(0,-1/16))
		draw_connect(cells[0], cells[1], radius, outline_color, Vec2(-1/16,0))

		for cell0, cell1, cell2 in zip(cells, cells[1:], cells[2:]):
			draw_connect(cell1, cell2, radius, outline_color, Vec2(1/16,0))
			draw_connect(cell1, cell2, radius, outline_color, Vec2(0,1/16))
			draw_connect(cell1, cell2, radius, outline_color, Vec2(-1/16,0))
			draw_connect(cell1, cell2, radius, outline_color, Vec2(0,-1/16))
			draw_connect(cell0, cell1, radius, body_color, Vec2(0, 0))

		draw_connect(cells[-2], cells[-1], radius, body_color, Vec2(0, 0))

		dir = self.dir # self.next_dir if self.next_dir else self.dir

		eye1_pos = head+.5+dir.trans()*radius
		eye2_pos = head+.5-dir.trans()*radius

		eye1_pos = (eye1_pos*Res.tilesize-(dir.trans()>0)).floor()
		eye2_pos = (eye2_pos*Res.tilesize+dir.trans()-(dir.trans()>0)).floor()

		screen.set_at(eye1_pos.tuple(), eye_color)
		screen.set_at((eye1_pos-dir).tuple(), eye_color)
		screen.set_at(eye2_pos.tuple(), eye_color)
		screen.set_at((eye2_pos-dir).tuple(), eye_color)

	def remove(self, level, pos):
		i = self.body.index(pos)
		bodies = [self.body[:i], self.body[i+1:]]
		snakes = [Snake().init(body, type(self.control)) for body in bodies if len(body) > 1]
		for cell in self.body:
			level.map2[cell] = TILES.Floor
		for snake in snakes:
			for cell in snake.body:
				level.map2[cell] = snake
		level.objects += snakes
		level.objects.remove(self)


	def add(self, level, prev_pos, pos):
		if prev_pos == self.body[-1]:
			level.map2[pos] = self
			self.init([*self.body, pos], type(self.control))

		if prev_pos == self.body[0]:
			level.map2[pos] = self
			self.init([pos, *self.body], type(self.control))

	def move(self, dpos):
		for cell in self.body:
			cell += dpos

	def Editor(level, pos, old_p):
		if old_p == None: return False
		diff = pos - old_p
		if abs(diff.x) + abs(diff.y) != 1:
			return False
		prev_tile = level.map2[old_p]
		if type(prev_tile) == Snake:
			if pos == prev_tile.body[1] and old_p == prev_tile.body[0]\
			or pos == prev_tile.body[-2] and old_p == prev_tile.body[-1]:
				prev_tile.remove(level, old_p)
				level.map[old_p].remove(level, old_p)
			else:
				level.map[pos].remove(level, pos)
				level.map2[pos].remove(level, pos)
				prev_tile = level.map2[old_p]
				prev_tile.add(level, old_p, pos)
		else:
			level.map[pos].remove(level, pos)
			level.map2[pos].remove(level, pos)
			prev_tile.remove(level, old_p)
			snake = Snake().init([pos, old_p], InputControl)
			for cell in snake.body:
				level.map2[cell] = snake
			level.objects.append(snake)
			snake.set_level(level)
		return True

	def update(self, level):
		if self.state == "win":
			self.dist += 1/6
			if self.dist >= 1:
				self.dist -= 1
				if len(self.body) == 0:
					self.level.done = True
					return
				if len(self.body) < 2 or self.body[-1] != self.body[-2]:
					level.map2[self.body[-1]] = TILES.Floor
				self.body.pop(-1)
			return

		if self.state == "dead":
			return

		if self.state == "play":

			self.dist += self.inc

			if self.next_dir == None:
				new_dir = self.control.ask()
				if new_dir != None:
					self.next_dir = new_dir
					self.turn_t = self.dist

			if self.move_state == "start":
				if self.next_dir != None:
					self.dir = self.next_dir
					self.next_dir = None
				self.move_state = "colide"

			if self.dist >= .5 and self.move_state == "colide":
				new_head = self.body[0] + self.dir
				self.move_state = "forward"
				level.map2[new_head].on_colide(level, self, new_head)
				level.map[new_head].on_colide(level, self, new_head)

			if self.dist >= 1 and self.move_state == "forward":
				self.dist -= 1
				self.collision_checked = False
				if len(self.body) < 2 or self.body[-1] != self.body[-2]:
					level.map2[self.body[-1]] = TILES.Floor
				level.map2[self.body[0] + self.dir] = self
				self.body = [self.body[0] + self.dir] + self.body[:-1]
				if self.next_dir != None:
					self.dir = self.next_dir
					# self.dist = 1 - self.turn_t
					self.next_dir = None
				self.move_state = "colide"
				

class InputControl: # could be smoother
	id = 0
	def __init__(self, snake):
		self.snake = snake
		self.speed = 1/16
		self.snake.inc = self.speed
		self.dirs = [self.snake.dir]
	def on_event(self, e):
		if len(self.dirs) > 3: return

		if e.type != pg.KEYDOWN: return

		new_dir = Vec2(
			(e.key == pg.K_RIGHT) - (e.key == pg.K_LEFT),
			(e.key == pg.K_DOWN) - (e.key == pg.K_UP)
		)
		if new_dir == Vec2(0): return
		if new_dir == -self.dirs[-1]: return
		if new_dir == self.dirs[-1]: return

		self.dirs.append(new_dir)
	def ask(self):
		if len(self.dirs) == 1:
			return

		self.dirs.pop(0)
		return self.dirs[0]