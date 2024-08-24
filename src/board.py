import random
from warnings import catch_warnings

neighbor_offsets = [
	(-1, -1),  # up-left
	(-1, 1),  # up-right
	(0, -2),  # left
	(0, 2),  # right
	(1, -1),  # down-left
	(1, 1),  # down-right
]

resource_to_port = { # each port and what it trades
	"3a": [(2, 0), (4, 4), (4, 6), (0, 6)],
	"2s": [(3, 1)],
	"2b": [(3, 3)],
	"2W": [(1, 7)],
	"2w": [(0, 4)],
	"2o": [(1, 1)]
}

hex_to_vertice_ports = { # hexes where ports are followed by which vertices can interact with them
	(2, 0): [(1, -1), (1, 1)],
	(3, 1): [(1, 1), (0, 1)],
	(4, 4): [(1, 1), (0, 1)],
	(4, 6): [(0, 1), (-1, 1)],
	(3, 3): [(-1, 1), (-1, -1)],
	(1, 7): [(-1, 1), (-1, -1)],
	(0, 6): [(-1, -1), (0, -1)],
	(0, 4): [(0, -1), (1, -1)],
	(1, 1): [(0, -1), (1, -1)],
}


vertex_to_offset_place_settlement = {  # clockwise its the offset needed to calculate the neighbors
	(1, 1): [(0, -2), (1, -1)],  # top-right vertex
	(0, 1): [(1, -1), (1, 1)],  # right vertex
	(-1, 1): [(1, 1), (0, 2)],  # bottom-right vertex
	(-1, -1): [(0, 2), (-1, 1)],  # bottom-left vertex
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
	(0, 1): 'N',  # right vertice
	(0, -1): 'N',  # left vertice
	(-1, -1): 'N',  # bottom left vertice
	(1, -1): 'N',  # top left vertice
	(1, 1): 'N',  # top right vertice
	(-1, 1): 'N',  # bottom right vertice
}

vertices_around_road = {
	(1, 0): [(1, -1), (1, 1)],
	(1, 1): [(1, 1), (0, 1)],
	(-1, 1): [(0, 1), (-1, 1)],
	(-1, 0): [(-1, 1),(-1, -1)],
	(-1, -1): [(-1, -1), (0, -1)],
	(1, -1): [(0, -1), (1,-1)],
}

road_around_road = {  # first left then right (when facing from the inside of the hex) on first, then both on the opposite hex)
	(1, 0): [[(1, -1), (1, 1)], [(-1, -1), (-1, 1)]],
	(1, 1): [[(1, 0), (-1, 1)], [(-1, 1), (1, 0)]],
	(-1, 1): [[(1, 1), (-1, 0)], [(1, 0), (-1, -1)]],
	(-1, 0): [[(-1, 1), (-1, -1)], [(1, 1), (1, -1)]],
	(-1, -1): [[(-1, 0), (1, -1)], [(-1, 1), (1, 0)]],
	(1, -1): [[(-1, -1), (1, 0)], [(-1, 0), (1, 1)]],
}

road_around_vertice = {  # first left then right (when facing from inside the hex) on first, then second clockwise to match the offset is to the external hexes
	(1, 1): [[(1, 0), (1, 1)], [(-1, 1), (1, -1)]],
	(0, 1): [[(1, 1), (-1, 1)], [(-1, 0), (1, 0)]],
	(-1, 1): [[(-1, 1), (-1, 0)], [(-1, -1), (1, 1)]],
	(-1, -1): [[(-1, 0), (-1, -1)], [(1, -1),(-1, 1)]],
	(0, -1): [[(-1, -1), (1, -1)], [(1, 0), (-1, 0)]],
	(1, -1): [[(1, -1), (1, 0)], [(1, 1), (-1, -1)]],
}

tile_road_dict = {
	(1, 0): 'N',  # top one
	(1, 1): 'N',  # top right one
	(-1, 1): 'N',  # bottom right one
	(-1, 0): 'N',  # bottom one
	(-1, -1): 'N',  #bottom left one
	(1, -1): 'N',  # top left one
}

road_to_offset_place_road = {
	(1, 0): (0, -2),
	(1, 1): (1, -1),
	(1, -1): (-1, -1),
	(-1, 0): (0, 2),
	(-1, -1): (-1, 1),
	(-1, 1): (1, 1),
}

# noinspection Annotator
class Tile:
	def __init__(self, tile_type: str, number: int):
		self._has_robber = False
		self._vertices_map = tile_vertices_dict.copy()
		self._roads_map = tile_road_dict.copy()

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

	def get_road(self, road: tuple[int, int]):
		return self._roads_map[road]

	def get_vertice(self, vertice: tuple[int, int]):
		if self._vertices_map[vertice][0] == 'S' or self._vertices_map[vertice][0] == 'C':
			player = self._vertices_map[vertice][1]
			return player
		return self._vertices_map[vertice]

	def get_number(self):
		return self._number

	def get_resource_distribution(self):
		player_resource = ""
		for vertices in self._vertices_map:
			if self._vertices_map[vertices] != 'N' and self._vertices_map[vertices] != 'X' :
				player = self._vertices_map[vertices]
				player = player.strip('S')
				if self._vertices_map[vertices][0] == 'S':
					player_resource += str(1) + self.get_type()[0] + player + ", " # a settlement gives the player 1 resource while city gives 2
				if self._vertices_map[vertices][0] == 'C':
					player_resource += str(2) + self.get_type()[0] + player + ", "
		return player_resource

	def get_players(self):
		players = []
		for vertices in self._vertices_map:
			if self._vertices_map[vertices] != 'N' and self._vertices_map[vertices] != 'X' :
				player = self._vertices_map[vertices]

				player = player.strip('SC')
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

	def set_road(self, road: tuple[int, int], c):
		if c == 'N' or c == 'S' or c == 'X':
			self._roads_map[road] = c

	# debug
		# print(f"Type from arg:{type(self._type)}, type from tile:{type(tile_type)}")

		# def tile_print(self):
		# 	print(f"Type:{self._type}, number:{self._number}", end="")

	def __str__(self):
		return f"Tile(type={self._type}, number={self._number})"

	def create_settlement(self, vertice: tuple[int,int], player: str):
		self._vertices_map[vertice] = 'S' + player
		for other_vertices in check_vertex_same_hex[vertice]:
			self._vertices_map[other_vertices] = 'X'
			print(f"Added X to {other_vertices}")
		print("success")
		return 1

	def create_road(self, coords: tuple[int,int], player: str):
		self._roads_map[coords] = player
		return "success"

	def place_city(self, coords: tuple[int,int]):
		self._vertices_map[coords] = self._vertices_map[coords].replace('S', 'C')


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

	def __init__(self, type_of_board: str):
		self.robber_place = (0, 0)
		self.board = reg_board_dict.copy()
		self.new_board(type_of_board)

	def translate_to_text(self, board_list, rows):
		board_text = []
		text_list = ['desert', 'wheat', 'Wood', 'sheep', 'brick', 'ore']
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
		again = input('generate another board? (y/n): ')
		if again == 'y':
			self.board = reg_board_dict.copy()
			self.new_board(_type)
		# else:
		return

	# this function takes a tile and a vertice of that tile and puts a settlement there, then it goes to the two
	#	hexes that share the same vertice and put a settlement there too

	def new_settlement(self, tile_coords: tuple[int,int], vertice_coords: tuple[int,int], player: str):
		print(f"I got here, tile_coords: {tile_coords}, vertice_coords: {vertice_coords}, type of player: {player}")

		if self.board[tile_coords].create_settlement(vertice_coords, player):
			print(f"added settlement to {tile_coords} in {vertice_coords}")

			for neighbor, neighbor_vertice in zip(vertex_to_offset_place_settlement[vertice_coords],
												  vertex_to_vertex_place_settlement[vertice_coords]):
				neighbor_coord = (tile_coords[0] + neighbor[0], tile_coords[1] + neighbor[1])
				print(neighbor_coord)
				if neighbor_coord in self.board:
					if self.board[neighbor_coord].create_settlement(neighbor_vertice, player):
						print(f"added settlement to {neighbor_coord} in {neighbor_vertice}")

	def	get_neighbor_roads_for_settlement(self, tile_coords: tuple[int,int], vertice_coords: tuple[int,int], player: str):
		if vertice_coords in road_around_vertice:
			for roads in road_around_vertice[vertice_coords][0]:
				road = self.board[tile_coords].get_road(roads)
				if road == player:
					return True
			index = 0
			for neighbor in vertex_to_offset_place_settlement[vertice_coords]:
				neighbor_coord = (tile_coords[0] + neighbor[0], tile_coords[1] + neighbor[1])
				if neighbor_coord in self.board:
					road = self.board[neighbor_coord].get_road(road_around_vertice[vertice_coords][1][index])
					if road == player:
						return True
				index += 1
		return False


	# This function starts by checking if the vertice and tile inserted are possible
	#	then it goes around each of the hexes on that vertice and sees if any has it marked as an X (or S)
	#	If so, it flags it as an X too
	#	it sends to the function to check neighbor roads that lead to this settlement (IF) it isnt the first round

	def check_settlement_placement(self, tile_coords: tuple[int,int], vertice_coords: tuple[int,int], first_round: bool, player: str):

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
					if not first_round and not self.get_neighbor_roads_for_settlement(tile_coords, vertice_coords, player):
						print("no roads connecting to this settlement")
						return False
		else:
			return False
		return True

	def place_settlement(self, tile_coords: tuple[int,int], vertice_coords: tuple[int,int], player_str: str, first_round: bool):
		player = player_str.strip('player')
		if self.check_settlement_placement(tile_coords, vertice_coords, first_round, player):
			self.new_settlement(tile_coords, vertice_coords, player)
			return 1
		return 0

	def roll(self):
		int1 = random.randint(1, 6)
		int2 = random.randint(1, 6)
		roll = int1 + int2
		if roll == 7:
			return 7
		player_resources = ""
		print(f"Rolled:{roll}!")
		for tile in self.board:
			if self.board[tile].get_number() == roll:
				if not self.board[tile].get_robber():
					buffer = self.board[tile].get_resource_distribution()
					player_resources += buffer
		return player_resources

	def new_road(self, tile_coords: tuple[int,int], road_coords: tuple[int,int], player: str):

		if self.board[tile_coords].create_road(road_coords, player) == "success":
			print(f"added road to {tile_coords} in {road_coords}")
		update_tile_coords = road_to_offset_place_road[road_coords]
		new_tile_coords = (tile_coords[0] + update_tile_coords[0], tile_coords[1] + update_tile_coords[1])
		if new_tile_coords in self.board:
			new_road = (road_coords[0] * -1, road_coords[1] * -1)
			if self.board[new_tile_coords].create_road(new_road, player) == "success":
				print(f"added road to {new_tile_coords} in {new_road}")

	def check_road_first_round(self, tile_coords: tuple[int,int], road_coords: tuple[int,int], player: str):
		if road_coords in vertices_around_road:
			for vertices in vertices_around_road[road_coords]:
				if self.board[tile_coords].get_vertice(vertices) == player:
					return True
		return False

	def check_road_next_to_road(self, tile_coords: tuple[int,int], road_coords: tuple[int,int], player: str):
		if road_coords in road_around_road:
			for roads in road_around_road[road_coords][0]:
				if self.board[tile_coords].get_road(roads) == player:
					return True
			offset_coords = road_to_offset_place_road[road_coords]
			opposite_hex = (tile_coords[0] + offset_coords[0], tile_coords[1] + offset_coords[1])
			if opposite_hex in self.board:
				for roads in road_around_road[road_coords][1]:
					if self.board[tile_coords].get_road(roads) == player:
						return True
		return False

	def check_road_placement(self, tile_coords: tuple[int,int], road_coords: tuple[int,int], first_round: bool, player: str):
		if tile_coords in self.board and road_coords in tile_road_dict:
			if self.board[tile_coords].get_road(road_coords) != 'N':
				return False
			if first_round:
				if not self.check_road_first_round(tile_coords, road_coords, player):
					print("there isn't any settlement to connect this road to")
					return False
			else:
				if not self.check_road_next_to_road(tile_coords, road_coords, player):
					print("there isn't any road to connect this road to")
					return False
			return True
		else:
			print("invalid position")
		return False

	def place_road(self, tile_coords: tuple[int,int], road_coords: tuple[int,int], player_str: str, first_round: bool):
		player = player_str.strip('player')

		if self.check_road_placement(tile_coords, road_coords, first_round, player):
			self.new_road(tile_coords, road_coords, player)
			return 1
		return 0

	def new_city(self, tile_coords: tuple[int,int], vertice_coords: tuple[int,int]):
		if self.board[tile_coords].place_city(vertice_coords):
			print(f"added city to {tile_coords} in {vertice_coords}")

			for neighbor, neighbor_vertice in zip(vertex_to_offset_place_settlement[vertice_coords],
												  vertex_to_vertex_place_settlement[vertice_coords]):
				neighbor_coord = (tile_coords[0] + neighbor[0], tile_coords[1] + neighbor[1])
				print(neighbor_coord)
				if neighbor_coord in self.board:
					if self.board[neighbor_coord].place_city(neighbor_vertice):
						print(f"added city to {neighbor_coord} in {neighbor_vertice}")

	def check_city_placement(self, tile_coords: tuple[int,int], vertice_coords: tuple[int,int], player_str: str):
		if tile_coords in self.board and vertice_coords in tile_vertices_dict:
			if self.board[tile_coords].get_vertice(vertice_coords) == player_str:
				return True
		return False

	def place_city(self, tile_coords: tuple[int,int], vertice_coords: tuple[int,int], player_str: str):
		player = player_str.strip('player')
		if self.check_city_placement(tile_coords, vertice_coords, player):
			self.new_city(tile_coords, vertice_coords)
			return 1
		return 0

	def move_robber(self, tile_coords: tuple[int,int]):
		if tile_coords in self.board:
			if tile_coords != self.robber_place:
				self.board[self.robber_place].remove_robber()
				self.board[tile_coords].set_robber()
				self.robber_place = tile_coords
				return self.board[tile_coords].get_players()
		return 0

	def get_board(self):
		for coordinates, tile in self.board.items():
			print(f"Coordinates: {coordinates} {tile}")

	def has_port(self, player_str: str, trade_type: str):
		player = player_str.strip('player')
		if trade_type in resource_to_port:
			for tile in resource_to_port[trade_type]:
				for vertice in hex_to_vertice_ports[tile]:
					buffer = self.board[tile].get_vertice(vertice)
					if player in buffer:
						return True

		return False