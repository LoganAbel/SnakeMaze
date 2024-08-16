import pygame as pg
from mat_lib.rect import Rect
from mat_lib.vector import Vec2
from io import BytesIO
import os

class Res:
	sheet = None
	tilesize = 16

	def init():
		Tile = lambda x, y:\
			Rect(Vec2(x * 16, y * 16), dim=Vec2(16))
		Res.sheet = SpriteSheet("..\\res\\spritesheet.png", {
			"apple": Tile(0, 0),
			"portal0": Tile(1, 0),
			"portal1": Tile(2, 0),
			"tele": Tile(3, 0),

			"poison": Tile(0, 2),

			"lever0": Tile(0, 1),
			"lever1": Tile(1, 1),
			"togglewall0": Tile(2, 1),
			"togglewall1": Tile(3, 1),

			"settings": Tile(4, 0),
			"edit": Tile(4, 1),
			"save": Tile(4, 2),

			"floor_item": Tile(5, 0),
			"wall_item": Tile(5, 1),
			"snake_body": Tile(5, 2),
		})
		Res.colors = {
			"purple": "#5e3c98",
			"black0": "#13091a",
			"black1": "#332741",
			"black2": "#494156",
			"black3": "#5c5467",
			"green": "#54c413",
			"white": "#e5dfee",
			"red": "#d93266",
		}
		Res.level_file = LevelFile("..\\res\\levels")

class SpriteSheet:
	def __init__(self, path, rects):
		self.img = pg.image.load(path).convert()
		self.img.set_colorkey('#000000')
		self.rects = rects
	def blit(self, screen, pos, name, flip=Vec2(1, 1)):
		img = self.img.subsurface(self.rects[name].tuple())
		img = pg.transform.flip(img, flip.x < 0, flip.y < 0)
		screen.blit(img, pos.tuple())
		img = pg.transform.flip(img, flip.x < 0, flip.y < 0)
	def subsurface(self, name):
		return self.img.subsurface(self.rects[name].tuple())

def splice_byte_file(path, start, end, write=None):
	dsize = end - start
	with open(filepath, 'r+b') as file:
		file.seek(end)
		end = file.read()
		file.seak(start)
		file.truncate()
		if write():
			dsize -= file.tell()
			write(file)
			dsize += file.tell()
		file.write(end)
	return dsize

class LevelFile:
	from components.level import Level, LevelHeader
	from components.tiles import Floor
	def __init__(self, path):
		self.path = path
		self.level_starts = []
		self.level_headers = []
		with open(self.path, 'ab') as file:
			pass
		with open(self.path, 'rb') as file:
			while file.peek(1) != b'':
				level_start = file.tell()
				self.level_starts.append(level_start)
				self.level_headers.append(LevelFile.LevelHeader.Load(file))
				LevelFile.Level.Skip(file)
			self.level_starts.append(file.tell())

	def load(self, level_i):
		if level_i >= len(self.level_headers):
			return LevelFile.Level.Default()

		with open(self.path, 'rb') as file:
			file.seek(self.level_starts[level_i], 0)
			return LevelFile.Level.Load(file, self.level_headers[level_i])

	def get_level_data(self, level_i):
		with open(self.path, 'rb') as file:
			file.seek(self.level_starts[level_i], 0)
			return file.read(self.level_starts[level_i+1] - self.level_starts[level_i])

	def delete(self, level_i):
		self.splice(level_i, 1)

	def save(self, level, level_i):
		if level_i == len(self.level_headers):
			self.splice(level_i, 0, level.save)
			self.level_headers.append(level.header)
			return

		self.splice(level_i, 1, level.save)

	def move(self, src, dst):
		if dst > src:
			dst -= 1
		src_data = self.get_level_data(src)
		src_header = self.level_headers[src]
		self.splice(src, 1)
		self.splice(dst, 0, lambda file: file.write(src_data))
		if dst == len(self.level_headers):
			self.level_headers.append(None)
		self.level_headers[dst] = src_header

	def splice(self, level_i, delete_count, write=None):
		start = self.level_starts[level_i]
		end = self.level_starts[level_i+delete_count]
		dsize = start - end
		with open(self.path, 'r+b') as file:
			file.seek(end)
			data = file.read()
			file.seek(start)
			file.truncate()
			if write:
				dsize -= file.tell()
				write(file)
				level_i += 1
				delete_count -= 1
				dsize += file.tell()
			file.write(data)
		self.level_starts = self.level_starts[:level_i] + self.level_starts[level_i+delete_count:]
		for i in range(level_i, len(self.level_starts)):
			self.level_starts[i] += dsize
		self.level_headers = self.level_headers[:level_i] + self.level_headers[level_i+delete_count:]