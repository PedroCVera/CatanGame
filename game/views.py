from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
def hello_world(request):
	return render(request, 'game/game.html')
