# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ParameterForm, HospitalParameterForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from django.db import IntegrityError
from .test3 import predict  # Import the predict function from the Python script
from django.views.decorators.csrf import csrf_exempt, csrf_protect  # Add this import
import json
from .Voice import record_audio, predict_parkinsons
from .ChatBOT import get_response_with_dynamic_chain

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'default_user_type')  # Provide a default value
        try:
            user = User.objects.create_user(username=username, password=password)
            user.profile.user_type = user_type  # Set the user type on the profile
            user.save()
            return redirect('login')
        except IntegrityError:
            return render(request, 'main/signup.html', {'error': 'Username already exists.'})
    return render(request, 'main/signup.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('recording')  # Redirect to recording page after successful login
        return render(request, 'main/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def hospital_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('hospital_home')
            else:
                return render(request, 'main/hospital_login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'main/hospital_login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def home_view(request):
    return render(request, 'main/home.html')

@login_required
def hospital_home(request):
    if request.method == 'POST':
        form = HospitalParameterForm(request.POST)
        if form.is_valid():
            data = [form.cleaned_data[key] for key in form.cleaned_data]
            chances = predict(data)
            return JsonResponse({'chances': chances})
    else:
        form = HospitalParameterForm()
    return render(request, 'main/hospital_home.html', {'form': form})

@login_required
def result_view(request, result):
    result = float(result)
    return render(request, 'main/result.html', {'result': result})

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        response = get_response_with_dynamic_chain(message)
        return JsonResponse({'response': response})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

def landing(request):
    return render(request, 'main/landing.html')

@csrf_exempt
def process_parameters(request):
    if request.method == 'POST':
        try:
            # Log raw request body
            print("Raw request body:", request.body)

            data = json.loads(request.body)
            print("Parsed data:", data)

            features = data.get('features', [])
            print("Features received:", features)

            if len(features) != 22:
                raise ValueError("Exactly 22 parameters are required.")

            # Call the prediction function
            prediction = predict(features)
            print("Prediction result:", prediction)

            return JsonResponse({"status": "success", "prediction": prediction})
        except Exception as e:
            print("Error occurred:", str(e))  # Log the error
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method."})

@csrf_exempt
def record_voice(request):
    if request.method == 'POST':
        audio_file = 'user_audio.wav'
        record_audio(filename=audio_file, duration=25)  # Record for 25 seconds
        prediction = predict_parkinsons(audio_file)
        return JsonResponse({'status': 'Recording complete', 'prediction': prediction})
    return JsonResponse({'status': 'Invalid request'}, status=400)

@login_required
def recording_view(request):
    return render(request, 'main/recording.html')