from board import *

def main():
	board = Board()
	board.new_board("reg")
	new_settlement = input("Where do you want to put your new settlement?<(tileX/tileY)(X/Y) ")

	coord_string = new_settlement.strip('()')
	coords = coord_string.split(')(')
	tile_coords = coords[0].split('/')
	settlement_coords = coords[1].split('/')
	tile_coords_tuple = (int(tile_coords[0]), int(tile_coords[1]))
	settlement_coords_tuple = (int(settlement_coords[0]), int(settlement_coords[1]))
	board.new_settlement(tile_coords_tuple, settlement_coords_tuple)

main()