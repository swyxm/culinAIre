from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import os
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .flavorProfile import analyzeFlavor
from .imageProcess import imageProcess
from .vectorDistCalc import vectorDistCalc



def analyze_flavor_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data from request body
            date = data.get('date')
            mealName = data.get('mealName')
            review = data.get('review')
            rating = data.get('rating')
            
            userData = analyzeFlavor(mealName,review,rating)
            request.session['userData'] = userData
            return JsonResponse({'message': 'Data received successfully!'})

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
def upload(request):
    if request.method == 'POST':
        processor = imageProcess()  # Instantiate the imageProcess class

        # Capture the image and process text
        text = processor.capture()  # This will invoke the capture function
        
        # Optional: Pass the extracted text to other methods as needed
        responseString = processor.reviewMenu(text)

        menuVec = processor.analyzeMenu(responseString)
        userData = request.session.get('userData', {})
        topDish = vectorDistCalc(menuVec, userData.get('avgMetrics',[]),responseString)
        imageUrl = os.path.join(settings.MEDIA_URL, 'clipped.jpg')
        return render(request, 'upload.html', {'image_url': imageUrl})
    return render(request, 'upload.html')
