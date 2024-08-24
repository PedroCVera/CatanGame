from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def hello_world(request):
	return HttpResponse("Welcome to the game API!")
