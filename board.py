import random

neighbor_offsets = [
	(-1, -1),  # up-left
	(-1, 1),  # up-right
	(0, -2),  # left
	(0, 2),  # right
	(1, -1),  # down-left
	(1, 1),  # down-right
]

vertex_to_offset_place_settlement = {
	(1, 1): [(0, -2), (1, -1)],  # top-right vertex
	(0, 1): [(1, -1), (1, 1)],  # right vertex
	(-1, 1): [(1, 1), (0, 2)],  # bottom-right vertex
	(-1, -1): [(0, 2), (-1, 1)],  # bottom-left vertex (corrected)
	(0, -1): [(-1, 1), (-1, -1)],  # left vertex
	(1, -1): [(-1, -1), (0, -2)],  # top-left vertex
}

vertex_to_vertex_place_settlement = {  #clockwise first the top then the one to the right
	(1, 1): [(-1, 1), (0, -1)],
	(0, 1): [(-1, -1), (1, -1)],
	(-1, 1): [(0, -1), (1, 1)],
	(-1, -1): [(1, -1),(0, 1)],
	(0, -1): [(1, 1), (-1, 1)],
	(1, -1): [(0, 1), (-1, -1)]
}

tile_vertices_dict = {
	(0, 1): 'N',
	(1, 0): 'N',
	(-1, -1): 'N',
	(1, -1): 'N',
	(1, 1): 'N',
	(-1, 1): 'N',
}


# noinspection Annotator
class Tile:
	def __init__(self, tile_type: str, number: int):
		self._has_robber = False
		self._vertices_map = tile_vertices_dict.copy()

		if tile_type:
			self._type = tile_type
		else:
			self._type = None
		if number:
			self._number = number
		else:
			self._number = 0

	def get_type(self):
		return self._type

	def get_number(self):
		return self._number

	def update_tile_number(self, number: int):
		self._number = number

	def update_tile_type(self, tile_type: str):
		self._type = tile_type

	# debug
		# print(f"Type from arg:{type(self._type)}, type from tile:{type(tile_type)}")

		# def tile_print(self):
		# 	print(f"Type:{self._type}, number:{self._number}", end="")

	def __str__(self):
		return f"Tile(type={self._type}, number={self._number})"

	def create_settlement(self, vertice: tuple[int,int]):
		self._vertices_map[vertice] = 'S'
		print("success")


reg_board_dict = {
	(0, 2): Tile(str(None), 0),
	(0, 4): Tile(str(None), 0),
	(0, 6): Tile(str(None), 0),
	(1, 1): Tile(str(None), 0),
	(1, 3): Tile(str(None), 0),
	(1, 5): Tile(str(None), 0),
	(1, 7): Tile(str(None), 0),
	(2, 0): Tile(str(None), 0),
	(2, 2): Tile(str(None), 0),
	(2, 4): Tile(str(None), 0),
	(2, 6): Tile(str(None), 0),
	(2, 8): Tile(str(None), 0),
	(3, 1): Tile(str(None), 0),
	(3, 3): Tile(str(None), 0),
	(3, 5): Tile(str(None), 0),
	(3, 7): Tile(str(None), 0),
	(4, 2): Tile(str(None), 0),
	(4, 4): Tile(str(None), 0),
	(4, 6): Tile(str(None), 0),
}


class Board:

	def __init__(self):
		self.board = reg_board_dict.copy()

	def translate_to_text(self, board_list, rows):
		board_text = []
		text_list = ['desert', 'wheat', 'wood', 'sheep', 'brick', 'ore']
		for i in range(rows):
			board_text.append([])
		for i in range(rows):
			for j in range(len(board_list[i])):
				board_text[i].append(text_list[board_list[i][j]])
		return board_text

	def update_board(self, board_words):
		board_keys = sorted(self.board.keys())
		index = 0

		for i in range(len(board_words)):
			for j in range(len(board_words[i])):
				self.board[board_keys[index]].update_tile_type(board_words[i][j])
				index += 1

	def update_board_numbers(self, numbers_list, board_words):
		board_keys = sorted(self.board.keys())
		index = 0

		for i in range(len(board_words)):
			for j in range(len(board_words[i])):
				if self.board[board_keys[index]].get_type() != 'desert':
					number = random.choice(numbers_list)
					self.board[board_keys[index]].update_tile_number(number)
					numbers_list.remove(number)
				index += 1

	def new_board(self, _type):

		reg_or_exp = None
		if not _type:
			reg_or_exp = input('Design a board for regular Catan (2-4 p) or Expansion (5-6 p)? Type reg or exp: ')
		# 0 = desert, 1 = wheat, 2 = wood, 3 = sheep, 4 = brick, 5 = ore
		# regular version has 19 tiles total, expansion has 30 tiles total
		if reg_or_exp == 'reg' or _type == 'reg':

			tiles = [0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5]
			numbers_list = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
			board = [[], [], [], [], []]
			row_lengths = [3, 4, 5, 4, 3]
			for i in range(5):
				while len(board[i]) < row_lengths[i]:
					tile = random.choice(tiles)
					board[i].append(tile)
					tiles.remove(tile)
			board_words = self.translate_to_text(board, 5)

			self.update_board(board_words)
			self.update_board_numbers(numbers_list, board_words)

			for coordinates, tile in self.board.items():
				print(f"Coordinates: {coordinates} {tile}")
		# else:
		# 	return
		# again = input('generate another board? (y/n): ')
		# if again == 'y':
		# 	self.board = reg_board_dict.copy()
		# 	self.new_board('reg')
		# else:
		return

	def find_neighbors(self, coord):
		neighbors = []
		for offset in neighbor_offsets:
			neighbor_coord = (coord[0] + offset[0], coord[1] + offset[1])
			if neighbor_coord in self.board:
				neighbors.append(neighbor_coord)
		return neighbors

	def new_settlement(self, tile_coords: tuple[int,int], vertice_coords: tuple[int,int]):
		print(f"I got here, tile_coords: {tile_coords}, vertice_coords: {vertice_coords} and its types were: {type(tile_coords)} and: {type(vertice_coords)}")
		self.board[tile_coords].create_settlement(vertice_coords)

		for neighbor, neighbor_vertice in zip(vertex_to_offset_place_settlement[vertice_coords], vertex_to_vertex_place_settlement[vertice_coords]):
			neighbor_coord = (tile_coords[0] + neighbor[0], tile_coords[1] + neighbor[1])
			print(neighbor_coord)
			if neighbor_coord in self.board:
				print(f"added settlement to {neighbor_coord} in {neighbor_vertice} ")
				self.board[neighbor_coord].create_settlement(neighbor_vertice)

	def check_placement(self, tile_coords: tuple[int,int], vertice_coords: tuple[int,int]):
		pass

	def place_settlement(self, tile_coords: tuple[int,int], vertice_coords: tuple[int,int]):
		if self.check_placement(tile_coords, vertice_coords):
			self.new_settlement(tile_coords, vertice_coords)




# game_board = Board()
# game_board.new_board('reg')
