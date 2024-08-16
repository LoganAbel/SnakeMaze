import pygame as pg
from components.tiles import *
from resources import Res
from mat_lib.vector import Vec2
from mat_lib.array2d import Array2d

class LevelHeader:
	def __init__(self, name):
		self.name = name
	def Default():
		return LevelHeader("New Level")
	def Load(file):
		name = ''
		while 1:
			byte = file.read(1)
			if byte == b'\x00': break
			name += byte.decode('utf-8')
		return LevelHeader(name)
	def save(self, file):
		file.write(self.name.encode('utf-8')+b'\0')
	def Skip(file):
		while file.read(1) != b'\0':
			pass

class Level:
	def __init__(self, map, objects, header, apple_count):
		self.header = header
		self.map = Array2d(map.dim)
		self.map2 = Array2d(map.dim)
		for p in map.dim.range():
			if type(map[p]) == Snake:
				self.map2[p] = map[p]
				self.map[p] = Floor
			else:
				self.map[p] = map[p]
				self.map2[p] = Floor
		self.objects = objects
		self.apple_count = apple_count
		self.done = False
		self.frozen = True
		self.screen = pg.Surface((map.dim * Res.tilesize).tuple())
		self.button_down = False
		for obj in self.objects:
			obj.set_level(self)

	def Default():
		wall = Wall()
		map = Array2d(Vec2(12, 12), [wall] * 12 * 12)
		wall.init(map)
		return Level(map, [wall], LevelHeader.Default(), 0)

	def copy(self):
		new_objects = [obj.copy() for obj in self.objects]
		new_map_data = []
		for i in self.map.dim.range():
			obj = self.map[i]
			if obj == Floor:
				obj = self.map2[i]
			if obj in self.objects:
				new_map_data.append(new_objects[self.objects.index(obj)])
			else:
				new_map_data.append(obj.copy())
		return Level(Array2d(self.map.dim, new_map_data), new_objects, self.header, self.apple_count)

	def resize(self, dir, dim):
		offset = self.map.dim - dim if dir == 0 else 0
		new_map_data = []
		new_map_data2 = []
		wall = next(obj for obj in self.objects if type(obj) == Wall)
		for p in dim.range():
			p += offset
			if self.map[p] != None:
				new_map_data.append(self.map[p])
			else:
				new_map_data.append(wall)
			if self.map2[p] != None:
				new_map_data2.append(self.map2[p])
			else:
				new_map_data2.append(Floor)
		self.map = Array2d(dim, new_map_data)
		self.map2 = Array2d(dim, new_map_data2)
		wall.init(self.map)
		self.screen = pg.Surface((self.map.dim * Res.tilesize).tuple())
		for obj in self.objects:
			obj.move(-offset)

	def Skip(file):
		w = int(file.read(1)[0])
		h = int(file.read(1)[0])
		file.seek(w * h, 1)
		snake_count = int(file.read(1)[0])
		for i in range(snake_count):
			file.seek(1, 1) # control
			snake_len = int(file.read(1)[0])
			file.seek(snake_len * 2, 1)

	def Load(file, header):
		# map
		LevelHeader.Skip(file)
		w = int(file.read(1)[0])
		h = int(file.read(1)[0])
		dim = Vec2(w, h)

		wall = Wall()
		objs = []
		top_objs = []

		apple_count = 0
		
		map = []
		for p in dim.range():
			id = int(file.read(1)[0])
			if id == Wall.id:
				map.append(wall)
				continue
			if id == Floor.id:
				map.append(Floor)
				continue
			if id == Apple.id:
				apple = Apple(p)
				objs.append(apple)
				map.append(apple)
				apple_count += 1
				continue
			if id == Poison.id:
				apple = Poison(p)
				objs.append(apple)
				map.append(apple)
				continue
			if id == Portal.id:
				portal = Portal(p)
				objs.append(portal)
				map.append(portal)
				continue
			if id == ToggleWall.id1:
				toggle_wall = ToggleWall(p, True)
				objs.append(toggle_wall)
				map.append(toggle_wall)
				continue
			if id == ToggleWall.id2:
				toggle_wall = ToggleWall(p, False)
				objs.append(toggle_wall)
				map.append(toggle_wall)
				continue
			if id == Lever.id:
				lever = Lever(p)
				objs.append(lever)
				map.append(lever)
				continue
			if id == Tele.id:
				tele = Tele(p)
				top_objs.append(tele)
				map.append(tele)
				continue
			raise Exception("Unexpected ID in Level Grid when loading")
		

		map = Array2d(dim, map)
		wall.init(map)

		# snake
		controls = [InputControl]

		snake_count = int(file.read(1)[0])
		snakes = []
		for i in range(snake_count):
			control = controls[int(file.read(1)[0])]
			snake_len = int(file.read(1)[0])
			snake = Snake()
			body = []
			for j in range(snake_len):
				x = int(file.read(1)[0])
				y = int(file.read(1)[0])
				body.append(Vec2(x, y))
				map[Vec2(x, y)] = snake

			snake.init(body, control)
			snakes.append(snake)

		return Level(map, [wall, *objs, *snakes, *top_objs], header, apple_count)

	def save(self, file):
		self.header.save(file)
		file.write(bytearray(self.map.dim.tuple()))
		for p in self.map.dim.range():
			tile = self.map2[p]
			if tile == Floor:
				tile = self.map[p]
			if type(tile) == ToggleWall:
				file.write(bytearray([tile.id1 if tile.fliped else tile.id2]))
			else:
				file.write(bytearray([tile.id]))
		snakes = [object for object in self.objects if type(object) == Snake]
		file.write(bytearray([len(snakes)]))
		for snake in snakes:
			file.write(bytearray([snake.control.id]))
			file.write(bytearray([len(snake.body)]))
			for cell in snake.body:
				file.write(bytearray(cell.tuple()))

	def on_event(self, e):
		if e.type == pg.KEYDOWN and e.key in (pg.K_RIGHT, pg.K_LEFT, pg.K_DOWN, pg.K_UP):
			self.frozen = False
		for object in self.objects:
			object.on_event(e)

	def update(self):
		if not self.frozen:
			for object in [*self.objects]:
				object.update(self)
	def draw(self):
		self.screen.fill('#000000')
		for object in self.objects:
			object.draw(self.screen)
		return self.screen