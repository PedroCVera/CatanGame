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

check_vertex_same_hex = {
	(1, 1): [(1, -1), (0, 1)],
	(0, 1): [(1, 1), (-1, 1)],
	(-1, 1): [(-1, -1), (0, 1)],
	(-1, -1): [(0, -1), (-1, 1)],
	(0, -1): [(1, -1), (-1, -1)],
	(1, -1): [(0, -1), (1, 1)]
}

tile_vertices_dict = {
	(0, 1): 'N',
	(0, -1): 'N',
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

	def get_robber(self):
		return self._has_robber

	def get_type(self):
		return self._type

	def get_vertice(self, vertice: tuple[int, int]):
		return self._vertices_map[vertice]

	def get_number(self):
		return self._number

	def get_players(self):
		players = []
		for vertices in self._vertices_map:
			if self._vertices_map[vertices] != 'N' and self._vertices_map[vertices] != 'X' :
				player = self._vertices_map[vertices]
				player = player.strip('S')
				players.append(player)

		return players

	def remove_robber(self):
		self._has_robber = False

	def set_robber(self):
		self._has_rober = True

	def update_tile_number(self, number: int):
		self._number = number

	def update_tile_type(self, tile_type: str):
		self._type = tile_type

	def set_vertice(self, vertice: tuple[int, int], c):
		if c == 'N' or c == 'S' or c == 'X':
			self._vertices_map[vertice] = c

	# debug
		# print(f"Type from arg:{type(self._type)}, type from tile:{type(tile_type)}")

		# def tile_print(self):
		# 	print(f"Type:{self._type}, number:{self._number}", end="")

	def __str__(self):
		return f"Tile(type={self._type}, number={self._number})"

	def create_settlement(self, vertice: tuple[int,int], player: int):
		if self._vertices_map[vertice] == 'N':
			self._vertices_map[vertice] = 'S' + str(player)
			for other_vertices in check_vertex_same_hex[vertice]:
				self._vertices_map[other_vertices] = 'X'

				print(f"Added X to {other_vertices}")
			print("success")
			return 1
		else:
			print("Not possible to place settlement there")
		return 0


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
		self.robber_place = (0,0)
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
				if self.board[board_keys[index]].get_type() == 'desert':
					self.robber_place = board_keys[index]
				else:
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


	# this function takes a tile and a vertice of that tile and puts a settlement there, then it goes to the two
	#	hexes that share the same vertice and put a settlement there too

	def new_settlement(self, tile_coords: tuple[int,int], vertice_coords: tuple[int,int], player_str: str):
		print(f"I got here, tile_coords: {tile_coords}, vertice_coords: {vertice_coords}, type of player: {player_str}")
		player = int(player_str.strip('player'))

		if self.board[tile_coords].create_settlement(vertice_coords, player):
			print(f"added settlement to {tile_coords} in {vertice_coords}")

			for neighbor, neighbor_vertice in zip(vertex_to_offset_place_settlement[vertice_coords],
												  vertex_to_vertex_place_settlement[vertice_coords]):
				neighbor_coord = (tile_coords[0] + neighbor[0], tile_coords[1] + neighbor[1])
				print(neighbor_coord)
				if neighbor_coord in self.board:
					if self.board[neighbor_coord].create_settlement(neighbor_vertice, player):
						print(f"added settlement to {neighbor_coord} in {neighbor_vertice}")


	# This function starts by checking if the vertice and tile inserted are possible
	#	then it goes around each of the hexes on that vertice and sees if any has it marked as an X (or S)
	#	If so, it flags it as an X too

	def check_placement(self, tile_coords: tuple[int,int], vertice_coords: tuple[int,int]):
		if tile_coords in self.board and vertice_coords in tile_vertices_dict:
			for neighbor, neighbor_vertice in zip(vertex_to_offset_place_settlement[vertice_coords],
												  vertex_to_vertex_place_settlement[vertice_coords]):
				neighbor_coord = (tile_coords[0] + neighbor[0], tile_coords[1] + neighbor[1])
				if neighbor_coord in self.board:
					if self.board[tile_coords].get_vertice(vertice_coords) != 'N':
						print("this vertice already has a settlement")
						return False
					if self.board[neighbor_coord].get_vertice(neighbor_vertice) != 'N':
						self.board[neighbor_coord].set_vertice(neighbor_vertice, 'X')

						print("this vertice already has a settlement")
						return False
		else:
			return False
		return True

	def place_settlement(self, tile_coords: tuple[int,int], vertice_coords: tuple[int,int], player: str):
		if self.check_placement(tile_coords, vertice_coords):
			self.new_settlement(tile_coords, vertice_coords, player)

	def roll(self):
		int1 = random.randint(1, 6)
		int2 = random.randint(1, 6)
		roll = int1 + int2
		if roll == 7:
			return 7
		player_resource = []
		print(f"Rolled:{roll}!")
		for tile in self.board:
			if self.board[tile].get_number() == roll:
				if not self.board[tile].get_robber():
					players = self.board[tile].get_players()
					resource = self.board[tile].get_type()
					player_resource.append((players, resource))

	def move_robber(self, tile_coords: tuple[int,int]):
		if tile_coords in self.board:
			self.board[self.robber_place].remove_robber()
			self.board[tile_coords].set_robber()
			self.robber_place = tile_coords
			return self.board[tile_coords].get_players()
