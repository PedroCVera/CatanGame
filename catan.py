from board import *
from player import Player
import random

board = Board()
player1 = Player()
player2 = Player()
player3 = Player()
player4 = Player()
player_list = [player1, player2, player3, player4]

resource_convertion_dic = {
	"w": "wheat",
	"W": "wood",
	"b": "brick",
	"o": "ore",
	"s": "sheep"
}

def new_road(player: str):
	global board

	new_road = input("Where do you want to put your new road? tileX,tileY X,Y ")
	coords = new_road.split(' ')
	tile_coords = coords[0].split(',')
	settlement_coords = coords[1].split(',')
	tile_coords_tuple = (int(tile_coords[0]), int(tile_coords[1]))
	road_coords_tuple = (int(settlement_coords[0]), int(settlement_coords[1]))
	print(f"This is tile {tile_coords_tuple} and this is road{road_coords_tuple}")
	board.place_road(tile_coords_tuple, road_coords_tuple, player)


def new_settlement(player: str):
	global board

	new_settlement = input("Where do you want to put your new settlement?<(tileX/tileY)(X/Y) ")

	coord_string = new_settlement.strip('()')
	coords = coord_string.split(')(')
	tile_coords = coords[0].split('/')
	settlement_coords = coords[1].split('/')
	tile_coords_tuple = (int(tile_coords[0]), int(tile_coords[1]))
	settlement_coords_tuple = (int(settlement_coords[0]), int(settlement_coords[1]))
	board.place_settlement(tile_coords_tuple, settlement_coords_tuple, player)

def play_cav(player_turn, robber: bool):
	global board
	global player1
	global player2
	global player3
	global player4

	action = None
	if player_turn.has_cavaliers() or robber:
		while action is None:
			action = input("What tile do you want to rob?(TileX/TileY) ")
			coord_string = action.strip('()')
			tile_coords = coord_string.split('/')
			tile_coords_tuple = (int(tile_coords[0]), int(tile_coords[1]))
			players = board.move_robber(tile_coords_tuple)
			if type(players) == int:
				print("invalid tile")
				play_cav(player_turn, robber)
			elif len(players) > 0:
				player = random.randint(0, len(players))
				player_to_get_stolen = int(players[player - 1])
				print(f"player: {player_to_get_stolen} ")
				resource = player_list[player_to_get_stolen - 1].get_stolen()
				if resource == 0:
					print("Unlucky")
					return
				if not robber:
					player_turn.remove_card("cavalier")
				player_turn.add_resources(resource, 1)
	else:
		print("You don't have cavaliers")

def distribute_resource(resources: str):
	global player1
	global player2
	global player3
	global player4

	resource_string = resources.strip().rstrip(',')

	resource_entries = resource_string.split(', ')
	for entry in resource_entries:
		# Assuming the format is consistent with <number><resource><player>
		if entry[1] in resource_convertion_dic:
			resource = resource_convertion_dic[entry[1]]
			player_list[int(entry[2]) - 1].add_resources(resource, int(entry[0]))


def make_roll(player_turn: Player):
	results = board.roll()
	print(results)
	if results is None:
		return
	if type(results) == int:
		if results == 7:
			play_cav(player_turn, True)
			return
	distribute_resource(results)

def main():
	global board
	board.new_board("reg")
	player = 0
	while 1:

		while 1:
			action = str(None)
			# while action != "R":
			# 	action = input("Roll(R) or play cav(C): ")
			# 	if action == "R":
			# 		make_roll(player2)
			# while action != "Pass":
			action = input("What do you want to do? Add Settlement(S)? Exit(E) Roll(R) Cav(C) Debug Resources/cav(P) Road(M)")
			if action == "E":
				exit()
			if action == "S":
				new_settlement("player3")
			if action == "M":
				new_road("player3")
			if action == "R":
				make_roll(player2)
			if action == "C":
				play_cav(player2, False)
			if action == "P":
				player3.add_resources("debug", 2)
				for i in range(3):
					player2.add_card("cavalier")


main()