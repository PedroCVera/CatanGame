from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'user_auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            return render(request, 'user_auth/login.html', {'error': 'Please fill in all fields'})

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id  # Store additional session data if needed
            return redirect('dashboard')
        else:
            return render(request, 'user_auth/login.html', {'error': 'Invalid credentials'})
    return render(request, 'user_auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
