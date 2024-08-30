from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from num2words import num2words


from django.http import JsonResponse

from game.game_src.catan import Game
from game.game_src.board import Board, Tile

game_list = []

game = None

reg_board_dict = {
	"0-2": "",
	"0-4": "",
	"0-6": "",
	"1-1": "",
	"1-3": "",
	"1-5": "",
	"1-7": "",
	"2-0": "",
	"2-2": "",
	"2-4": "",
	"2-6": "",
	"2-8": "",
	"3-1": "",
	"3-3": "",
	"3-5": "",
	"3-7": "",
	"4-2": "",
	"4-4": "",
	"4-6": "",
}


def update_game_board(board):
	game_board = reg_board_dict.copy()
	for coordinates, tile in board.items():
		tuple_str = f"{coordinates[0]}-{coordinates[1]}"
		game_board[tuple_str] = f"{tile.get_type()} | {num2words(tile.get_number())}"
		print(game_board[tuple_str])
	return game_board


# Create your views here.
@login_required
def hello_world(request):
	return render(request, 'game/game.html')

@login_required
def new_game(request):
	global game
	player_name = request.user.username

	game = Game(2, player_name)
	game_board = game.get_board()
	# game_list.append(game)
	game_board_response = update_game_board(game_board)

	return JsonResponse({'message': 'Game created', 'player': player_name, 'board': game_board_response}, )

