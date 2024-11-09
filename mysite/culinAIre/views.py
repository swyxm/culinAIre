from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .flavorProfile import analyzeFlavor

def analyze_flavor_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data from request body
            date = data.get('date')
            mealName = data.get('mealName')
            review = data.get('review')
            rating = data.get('rating')
            
            # Process data and return a response
            response_data = {'message': 'Data received successfully!'}
            return analyzeFlavor(mealName,review,rating)
            #return JsonResponse(data, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Somethings wrong'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def home(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'homepage.html', {'username': username})

def userAuth(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    register_form = UserCreationForm()
    login_form = AuthenticationForm()
    
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials')
        elif 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Account created successfully. You can log in now.')
                return redirect('userAuth')
            else:
                messages.warning(request, 'Registration failed. Please check the form.')

    return render(request, 'login.html', {'register_form': register_form})

