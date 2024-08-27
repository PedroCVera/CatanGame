from game.game_src.board import *
from game.game_src.player import Player
import random

resource_convertion_dic = {
	"w": "wheat",
	"W": "wood",
	"b": "brick",
	"o": "ore",
	"s": "sheep"
}

possible_trades_list = ["3a", "2s", "2b", "2W", "2w", "2o", "4a"]

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
	print(f"PLAYER:{player} WON THE GAME!!! WOWOWOWOWOWOWOWOWOWOWOWOWOW")
	exit(1)

class Game:
	def __init__(self, player_n: int, player1):
		if player_n > 6 or player_n < 2:
			print("Player number must be between 2-6")
			exit(1)
		self._player1_id = player1
		self._player_number = player_n
		self._player_list = []
		self._player_dict = {}
		self._player1 = Player(1)
		self._player2 = Player(2)
		self._player_dict["player1"] = self._player1
		self._player_dict["player2"] = self._player2
		self._player_list.append("player1")
		self._player_list.append("player2")
		self._largest_army = None

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
		# self.round_zero()
		print("I was here too")

	def get_board(self):
		print(self._board.get_board())
		return self._board.get_board()

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
			self.winning_points()
			self._current_player = self._player_list[index]
			self._board.print_board()
			self._current_player = self._player_list[index]
			self.round_first_part()
			self.round_second_part()
			index += 1
			if index > self._player_number - 1:
				index = 0

	def winning_points(self):
		for keys in self._player_dict:
			print(f"Player: {keys} has {self._player_dict[keys].get_points()} points")

	def round_first_part(self, action):
		# action = input(f"Do you want to roll(R) or to play knights(C)) Exit(E)?")
		if action == "R":
			self.make_roll()
		elif action == "E":
			exit(1)
		elif action == "C":
			self.play_cav(False)
			self.round_first_part()
		else:
			self.round_first_part()

	def round_second_part(self, action):
		while True:
			# action = input(f"What action do you want to do? Build a: "
			# "Road(R), Settlement(S), City(C), Development_card(D) or Pass(P), Trade(T) Debug Resources/cav(H)?")
			if action == "R":
				self.new_road(False, False)
			elif action == "S":
				self.new_settlement(False)
			elif action == "D":
				self.choose_card_action()
			elif action == "T":
				self.trade()
			elif action == "C":
				self.new_city()
			elif action == "H":
				self._player_dict[self._current_player].add_resources("debug", 5)
				for i in range(3):
					self._player_dict[self._current_player].add_card("Knight")
			elif action == "P":
				return

	def trade(self, trade_offer, given_resources):
		# trade_offer = input("Whats the trade offer? Ports: 3 for anything(3a) 2 for 1 wood(2W) 2 for 1 wheat(2w) 2 for 1 ore(2o) 2 for 1 brick"
		# 						"(2b) 2 for 1 sheep(2s) or 4 for anything?(4a)")
		# given_resources = input("What do you want to give? wood(W) wheat(w) ore(o) bricks(b) sheep(s)?")

		if (given_resources not in resource_convertion_dic or trade_offer not in possible_trades_list or
				not self._player_dict[self._current_player].has_resource(resource_convertion_dic[given_resources], int(trade_offer[0]))):
			print("Choose a valid trade and resource!")
			self.trade()
		elif self._board.has_port(self._current_player, trade_offer) or trade_offer == "4a":
			if trade_offer == "4a" or trade_offer == "3a":
				wanted_resource = input("What resource do you want? wood(W) wheat(w) ore(o) bricks(b) sheep(s)?")
				if wanted_resource in resource_convertion_dic:
					self._player_dict[self._current_player].add_resources(resource_convertion_dic[wanted_resource], 1)
				else:
					print("Choose a valid resource!")
					self.trade()
			else:
				self._player_dict[self._current_player].add_resources(resource_convertion_dic[trade_offer[1]], 1)
			self._player_dict[self._current_player].remove_resources(resource_convertion_dic[given_resources], int(trade_offer[0]))
			self._player_dict[self._current_player].print_resources()


	def choose_card_action(self, action):
		cards = self._player_dict[self._current_player].get_cards()
		while "VP" in cards:
			cards.remove("VP")
		# action = input(f"What do you want to do? Buy a development card(B) or play one of these? [{cards}] <Name>")
		if action == "B":
			self.new_card()
		if action in development_cards_list:
			self.play_card(action)
			if action != "Knight": #Knights have to be counted on the part due to the army counting
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

	def monopoly_card(self, resource):
		# resource = input("What resource do you want to steal? W: wood, w: wheat, b: brick, o:ore, s: sheep")
		if resource not in resource_convertion_dic:
			print("You need to choose a valid resource")
			self.monopoly_card()
			return
		for entry in self._player_dict:
			if entry != self._player_dict[self._current_player]:
				buffer = self._player_dict[entry].monopoly(resource)
				self._player_dict[self._current_player].add_resources(resource, buffer)

	def resource_card(self, resource1, resource2):
		# resource1 = input("what resources do you want? W: wood, w: wheat, b: brick, o:ore, s: sheep")
		# resource2 = input("what resources do you want? W: wood, w: wheat, b: brick, o:ore, s: sheep")

		if resource1 not in resource_convertion_dic or resource2 not in resource_convertion_dic:
			print("You need to choose valid resources")
			self.resource_card()
			return
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
		if self._player_dict[self._current_player].has_card("Knight") or robber:
			while action is None:
				action = input("What tile do you want to rob? TileX,TileY ")
				if len(action) > 5:
					print("invalid tile")
					self.play_cav(robber)
					return
				tile_coords = action.split(',')
				tile_coords_tuple = (int(tile_coords[0]), int(tile_coords[1]))
				players = self._board.move_robber(tile_coords_tuple) # here they come as numbers in a list e.g [2, 3]
				if type(players) == int:
					print("invalid tile")
					self.play_cav(robber)
					return

				elif len(players) > 0:
					player = random.randint(0, len(players) - 1)
					player_to_get_stolen = int(players[player]) # here a random player gets stolen and its number is converted to an int
					print(f"player: {player_to_get_stolen} ")
					# here that int is used to fetch the player in question since they are put in order
					resource = self._player_dict[self._player_list[player_to_get_stolen - 1]].get_stolen()
					if resource == 0:
						print("Unlucky")
						return

					self._player_dict[self._current_player].add_resources(resource, 1)
				if not robber:
					self._player_dict[self._current_player].remove_card("Knight")
					if self._player_dict[self._current_player].get_army() >= 3 and self._player_dict[self._current_player] != self._largest_army:
						if self._largest_army is None:
							self._player_dict[self._current_player].add_winning_point(2)
							self._largest_army = self._player_dict[self._current_player]
						else:
							if self._player_dict[self._current_player].get_army() > self._largest_army.get_army():
								self._largest_army.remove_winning_points(2)
								self._player_dict[self._current_player].add_winning_point(2)
								self._largest_army = self._player_dict[self._current_player]
		else:
			print("You don't have knights")

	def make_roll(self):
		results = self._board.roll()
		print(results)
		if type(results) == int:
			if results == 7:
				self.discard_everyone()
				self.play_cav(True)
				return
		if len(results) < 1:
			return
		self._distribute_resource(results)

	def discard_everyone(self):
		for player in self._player_dict:
			if self._player_dict[player].get_resources() > 7:
				self._player_dict[player].discard_half()

	def new_road(self, first_round: bool, development_card: bool, new_road_coords):

		if not self._player_dict[self._current_player].try_road() and not first_round and not development_card:
			print("Not enough resources!")
			return
		# new_road_coords = input("Where do you want to put your new road? tileX,tileY X,Y ")
		coords = new_road_coords.split(' ')
		if len(coords) != 2:
			print("wrong coords")
			self.new_road(first_round, development_card)
			return
		tile_coords_tuple, road_coords_tuple = separate_coord_input(coords)
		if tile_coords_tuple == (-3, -3) and road_coords_tuple == (-3, -3):
			print("wrong coords")
			self.new_road(first_round, development_card)
			return

		print(f"This is tile {tile_coords_tuple} and this is road{road_coords_tuple}")
		if not self._board.place_road(tile_coords_tuple, road_coords_tuple, self._current_player, first_round) and (first_round or development_card):
			self.new_road(first_round, development_card)
			return
		if not first_round and not development_card:
			self._player_dict[self._current_player].road_cost()


	def new_settlement(self, first_round: bool, new_settlement_coords):

		if not self._player_dict[self._current_player].try_settlement() and not first_round:
			print("Not enough resources!")
			return
		# new_settlement_coords = input("Where do you want to put your new settlement? tileX,tileY X,Y ")
		coords = new_settlement_coords.split(' ')
		if len(coords) != 2:
			print("wrong coords")
			self.new_settlement(first_round)
			return

		tile_coords_tuple, settlement_coords_tuple = separate_coord_input(coords)
		if tile_coords_tuple == (-3, -3) and settlement_coords_tuple == (-3, -3):
			print("wrong coords")
			self.new_settlement(first_round)
			return

		if self._board.place_settlement(tile_coords_tuple, settlement_coords_tuple, self._current_player, first_round):
			if self._player_dict[self._current_player].add_winning_point(1):
				win(self._current_player)
		elif not self._board.place_settlement(tile_coords_tuple, settlement_coords_tuple, self._current_player, first_round) and first_round:
			self.new_settlement(first_round)
			return
		if not first_round:
			self._player_dict[self._current_player].settlement_cost()

	def new_city(self, new_city_coords):

		if not self._player_dict[self._current_player].try_city():
			print("Not enough resources!")
			return
		# new_city_coords = input("Where do you want to put your new road? tileX,tileY X,Y ")
		coords = new_city_coords.split(' ')
		if len(coords) != 2:
			print("wrong coords")
			self.new_city()
			return
		tile_coords_tuple, city_coords_tuple = separate_coord_input(coords)
		if tile_coords_tuple == (-3, -3) and city_coords_tuple == (-3, -3):
			print("wrong coords")
			self.new_city()
			return

		if self._board.place_city(tile_coords_tuple, city_coords_tuple, self._current_player):
			if self._player_dict[self._current_player].add_winning_point(1):
				win(self._current_player)
		self._player_dict[self._current_player].city_cost()


