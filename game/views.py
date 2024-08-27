from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from game.game_src.catan import Game

game_list = []

game = None

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
	return JsonResponse({'message': 'Game created', 'player': player_name, 'board': game_board}, )

