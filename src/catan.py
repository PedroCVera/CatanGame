
from board import *
from player import Player
import random

resource_convertion_dic = {
	"w": "wheat",
	"W": "wood",
	"b": "brick",
	"o": "ore",
	"s": "sheep"
}

development_cards_list = ["Knight", "VP", "road", "resources", "monopoly"]

def separate_coord_input(coords: list[str]):
	tile_coords = coords[0].split(',')
	settlement_coords = coords[1].split(',')
	if len(tile_coords) != 2 and len(settlement_coords) != 2:
		return (-3, -3), (-3, -3)
	tile_coords_tuple = (int(tile_coords[0]), int(tile_coords[1]))
	road_coords_tuple = (int(settlement_coords[0]), int(settlement_coords[1]))
	return tile_coords_tuple, road_coords_tuple


def win(player: str):
	print(f"PLAYER:{player} WON THE GAME!!! WOWOOWOOWOWOWOOWOWOWOWOWOOWOW")
	exit(1)

class Game:
	def __init__(self, player_n: int):
		if player_n > 6 or player_n < 2:
			print("Player number must be between 2-6")
			exit(1)
		self._player_number = player_n
		self._player_list = []
		self._player_dict = {}
		self._player1 = Player(1)
		self._player2 = Player(2)
		self._player_dict["player1"] = self._player1
		self._player_dict["player2"] = self._player2
		self._player_list.append("player1")
		self._player_list.append("player2")

		if player_n >= 3:
			self._player3 = Player(3)
			self._player_dict["player3"] = self._player3
			self._player_list.append("player3")

		if player_n == 4:
			self._player4 = Player(4)
			self._player_dict["player4"] = self._player4
			self._player_list.append("player4")

		if player_n < 5:
			self._board = Board("reg")
			self._development_cards = [
				"Knight", "Knight", "Knight", "Knight", "Knight", "Knight", "Knight", "Knight", "Knight", "Knight",
				"Knight", "Knight", "Knight", "Knight",  # 14 Knight cards
				"VP", "VP", "VP", "VP", "VP",  # 5 Victory Point cards
				"road", "road",  # 2 Road Building cards
				"resources", "resources",  # 2 Year of Plenty cards
				"monopoly", "monopoly"  # 2 Monopoly cards
			]
			random.shuffle(self._development_cards)
		else:
			self._board = Board("exp")
		self._current_player = "player1"
		print("I was here")
		self.round_zero()
		print("I was here too")

	def round_zero(self):
		for entry in self._player_list:
			self._current_player = entry
			self.new_settlement(True)
			self.new_road(True, False)
		for entry in reversed(self._player_list):
			self._current_player = entry
			self.new_settlement(True)
			self.new_road(True, False)

		self.game_loop()

	def game_loop(self):
		index = 0
		while 1:
			self._current_player = self._player_list[index]
			self._board.get_board()
			self._current_player = self._player_list[index]
			self.round_first_part()
			self.round_second_part()
			index += 1
			if index > self._player_number - 1:
				index = 0

	def round_first_part(self):
		action = input(f"Do you want to roll(R) or to play knights(C)({self._player_dict[self._current_player].has_card("knight")}) Exit(E)?")
		if action == "R":
			self.make_roll()
		elif action == "E":
			exit(1)
		elif action == "C":
			self.play_cav(False)
			self.round_first_part()
		else:
			self.round_first_part()

	def round_second_part(self):
		while True:
			action = input(f"What action do you want to do? Build a: Road(R), Settlement(S), City(C), Development_card(D) or Pass(P) Debug Resources/cav(H)?")
			if action == "R":
				self.new_road(False, False)
			elif action == "S":
				self.new_settlement(False)
			elif action == "D":
				self.choose_card_action()
			elif action == "C":
				self.new_city()
			elif action == "H":
				self._player_dict[self._current_player].add_resources("debug", 5)
				for i in range(3):
					self._player_dict[self._current_player].add_card("knight")
			elif action == "P":
				return

	def choose_card_action(self):
		cards = self._player_dict[self._current_player].get_cards()
		while "VP" in cards:
			cards.remove("VP")
		action = input(f"What do you want to do? Buy a development card(B) or play one of these? [{cards}] <Name>")
		if action == "B":
			self.new_card()
		if action in development_cards_list:
			self.play_card(action)
			self._player_dict[self._current_player].remove_card(action)

	def play_card(self, card: str):
		if card in self._player_dict[self._current_player].get_cards():
			if card == "Knight":
				self.play_cav(False)
			elif card == "road":
				self.new_road(False, True)
				self.new_road(False, True)
			elif card == "resources":
				self.resource_card()
			elif card == "monopoly":
				self.monopoly_card()
		else:
			print("You don't have that card")

	def monopoly_card(self):
		resource = input("What resource do you want to steal? W: wood, w: wheat, b: brick, o:ore, s: sheep")
		if resource not in resource_convertion_dic:
			print("You need to choose a valid resource")
			self.monopoly_card()
		for entry in self._player_dict:
			if entry != self._player_dict[self._current_player]:
				buffer = self._player_dict[entry].monopoly(resource)
				self._player_dict[self._current_player].add_resources(resource, buffer)



	def resource_card(self):
		resource1 = input("what resources do you want? W: wood, w: wheat, b: brick, o:ore, s: sheep")
		resource2 = input("what resources do you want? W: wood, w: wheat, b: brick, o:ore, s: sheep")

		if resource1 not in resource_convertion_dic or resource2 not in resource_convertion_dic:
			print("You need to choose valid resources")
			self.resource_card()
		else:
			self._player_dict[self._current_player].add_resources(resource_convertion_dic[resource1], 1)
			self._player_dict[self._current_player].add_resources(resource_convertion_dic[resource2], 1)


	def new_card(self):
		if not self._player_dict[self._current_player].try_card():
			print("Not enough resources!")
			return
		else:
			self._player_dict[self._current_player].card_cost()
			if len(self._development_cards):
				first_entry = self._development_cards.pop(0)
				if first_entry == "VP":
					self._player_dict[self._current_player].add_winning_point(1)
				self._player_dict[self._current_player].add_card(first_entry)


	def _distribute_resource(self, resources: str):
		resource_string = resources.strip().rstrip(',')

		resource_entries = resource_string.split(', ')
		for entry in resource_entries:
			# Assuming the format is consistent with <number><resource><player>
			if entry[1] in resource_convertion_dic:
				resource = resource_convertion_dic[entry[1]]

				self._player_dict[self._player_list[int(entry[2]) - 1]].add_resources(resource, int(entry[0]))

	def play_cav(self, robber: bool):
		action = None
		if self._player_dict[self._current_player].has_card("knight") or robber:
			while action is None:
				action = input("What tile do you want to rob?(TileX/TileY) ")
				coord_string = action.strip('()')
				tile_coords = coord_string.split('/')
				tile_coords_tuple = (int(tile_coords[0]), int(tile_coords[1]))
				players = self._board.move_robber(tile_coords_tuple) # here they come as numbers in a list e.g [2, 3]
				if type(players) == int:
					print("invalid tile")
					self.play_cav(robber)
				elif len(players) > 0:
					player = random.randint(0, len(players))
					player_to_get_stolen = int(players[player]) # here a random player gets stolen and its number is converted to an int
					print(f"player: {player_to_get_stolen} ")
					resource = self._player_dict[self._player_list[player_to_get_stolen - 1]].get_stolen() # here that int is used to fetch the player in question since they are put in order
					if resource == 0:
						print("Unlucky")
						return
					if not robber:
						self._player_dict[self._current_player].remove_card("knight")
					self._player_dict[self._current_player].add_resources(resource, 1)
		else:
			print("You don't have knights")

	def make_roll(self):
		results = self._board.roll()
		print(results)
		if type(results) == int:
			if results == 7:
				self.play_cav(True)
				return
		if len(results) < 1:
			return
		self._distribute_resource(results)

	def new_road(self, first_round: bool, development_card: bool):

		if not self._player_dict[self._current_player].try_road() and not first_round and not development_card:
			print("Not enough resources!")
			return
		new_road_coords = input("Where do you want to put your new road? tileX,tileY X,Y ")
		coords = new_road_coords.split(' ')
		if len(coords) != 2:
			print("wrong coords")
			self.new_road(first_round)
		tile_coords_tuple, road_coords_tuple = separate_coord_input(coords)
		if tile_coords_tuple == (-3, -3) and road_coords_tuple == (-3, -3):
			print("wrong coords")
			self.new_road(first_round)

		print(f"This is tile {tile_coords_tuple} and this is road{road_coords_tuple}")
		if not self._board.place_road(tile_coords_tuple, road_coords_tuple, self._current_player, first_round) and (first_round or development_card):
			self.new_road(first_round, False)


	def new_settlement(self, first_round: bool):

		if not self._player_dict[self._current_player].try_settlement() and not first_round:
			print("Not enough resources!")
			return
		new_settlement_coords = input("Where do you want to put your new settlement? tileX,tileY X,Y ")
		coords = new_settlement_coords.split(' ')
		if len(coords) != 2:
			print("wrong coords")
			self.new_settlement(first_round)

		tile_coords_tuple, settlement_coords_tuple = separate_coord_input(coords)
		if tile_coords_tuple == (-3, -3) and settlement_coords_tuple == (-3, -3):
			print("wrong coords")
			self.new_settlement(first_round)

		if self._board.place_settlement(tile_coords_tuple, settlement_coords_tuple, self._current_player, first_round):
			if self._player_dict[self._current_player].add_winning_point(1):
				win(self._current_player)
		elif not self._board.place_settlement(tile_coords_tuple, settlement_coords_tuple, self._current_player, first_round) and first_round:
			self.new_settlement(first_round)

	def new_city(self):

		if not self._player_dict[self._current_player].try_city():
			print("Not enough resources!")
			return
		new_city_coords = input("Where do you want to put your new road? tileX,tileY X,Y ")
		coords = new_city_coords.split(' ')
		if len(coords) != 2:
			print("wrong coords")
			self.new_city()
		tile_coords_tuple, city_coords_tuple = separate_coord_input(coords)
		if tile_coords_tuple == (-3, -3) and city_coords_tuple == (-3, -3):
			print("wrong coords")
			self.new_city()

		if self._board.place_settlement(tile_coords_tuple, city_coords_tuple, self._current_player):
			if self._player_dict[self._current_player].add_winning_point(2):
				win(self._current_player)


game = Game(2)