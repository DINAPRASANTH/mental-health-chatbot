from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat,UserProfile
from . import custom2

from django.utils import timezone

import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyBtRt__Qz9UaJmTekm9_MiqYl2AxjV-Bmw"

def ask_openai(message):
    answer = custom2.chatbot(message)
    return answer

@login_required
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:  # Check if message is not None
            response = ask_openai(message)
            chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
            chat.save()
            return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats, 'theme_color': user_profile.color})

@login_required
def preferences(request):
    if request.method == 'POST':
        lang = request.POST['language']
        color = request.POST['color']
        season = request.POST['season']
        pet = request.POST['pet']
        gender = request.POST['gender']
        age_group = request.POST['age']
        prefer, created = UserProfile.objects.get_or_create(user=request.user)
        prefer.lang = lang
        prefer.color = color
        prefer.season = season
        prefer.pet = pet
        prefer.gender = gender
        prefer.age_group = age_group
        prefer.save()
        return redirect('chatbot')
    return render(request, 'preferences.html')


def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('prefer')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                UserProfile.objects.create(user=user)
                auth.login(request, user)
                return redirect('login')
            except:
                error_message = 'Error creating account'
            return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = "Passwords don't match" 
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

from django.contrib.auth.models import User

@login_required
@csrf_exempt
def delete_chats(request):
    if request.method == 'POST':
        request.user.chat_set.all().delete()
        return JsonResponse({'message': 'Chats deleted successfully'})




from deep_translator import GoogleTranslator
import speech_recognition as sr 
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io


@login_required
def audio_chat(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'audiochat.html', {'season': user_profile.season,'pet': user_profile.pet,'gender': user_profile.gender,})

# def recognize_speech():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Say Something in Tamil and pause, no need to press any")
#         audio = r.listen(source)
#         print('Got you')
#     try:
#         WhatUSpoke = r.recognize_google(audio, language='ta-IN')
#         print('What you spoke (Google):', WhatUSpoke)
#         return WhatUSpoke
#     except:
#         pass

def translate_text(text):
    translated = GoogleTranslator(source='auto', target='en').translate(text)
    print(translated)
    return translated

# def translate_tamil(text):
#     user_profile = UserProfile.objects.get(user=request.user)
#     translated = GoogleTranslator(source='auto', target='tamil').translate(text)
#     print(translated)
#     return translated

def text_to_speech(text):
    tts = gTTS(text=text, lang='ta', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp) 
    fp.seek(0)
    song = AudioSegment.from_file(fp, format="mp3")
    play(song)

def audio(request):
    user_profile = UserProfile.objects.get(user=request.user)
    language = 'english'  # default language
    if request.method == 'POST':
        text = request.POST.get('message')
        print(text)
        translated_text = translate_text(text)
        res = custom2.chatbot(translated_text)
        print(res)
        if (user_profile.lang=='en-IN'):
            language = 'english'
        elif (user_profile.lang == 'ta-IN'):
            language = 'tamil'
        elif (user_profile.lang == 'te-IN'):
            language = 'telugu'
        elif (user_profile.lang == 'ml-IN'):
            language = 'malayalam'
        elif (user_profile.lang == 'hi-IN'):
            language = 'hindi'
        print(language)
        tam = GoogleTranslator(source='auto', target=language).translate(res)
        print(tam)
        return JsonResponse({'response': tam,'lang': user_profile.lang})
    
    
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PreferenceForm
from .image_gen import generate_image

def preference_view(request):
    if request.method == 'POST':
        form = PreferenceForm(request.POST)
        if form.is_valid():
            favorite_pet = form.cleaned_data['pet']
            favorite_color = form.cleaned_data['color']
            favorite_season = form.cleaned_data['season']
            gender = form.cleaned_data['gender']
            age_group = form.cleaned_data['age']
            
            # Generate image
            image_path = generate_image(favorite_pet, favorite_color, favorite_season, gender, age_group)
            if image_path:
                # Redirect to chatbot view with success message and image path
                success_message = 'Image generated successfully!'
                image_path = image_path.replace('static/', '')  # Remove 'static/' from the image path
                return redirect('chatbot')
            else:
                return HttpResponse("Error generating image. Please try again.")  # Display error message
    else:
        form = PreferenceForm()

    return render(request, 'preferences.html', {'form': form})


def games_view(request):
    return render(request, 'games.html')
def videochat(request):
    return render(request, 'videochat.html')

