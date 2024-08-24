# dashboard/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Render the dashboard page where users can prepare to start a game
    return render(request, 'dashboard/dashboard.html')

def game(request):
    return redirect('game')

