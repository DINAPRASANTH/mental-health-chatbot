from deep_translator import GoogleTranslator
import speech_recognition as sr 
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io
import custom2

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say Something in Tamil and pause, no need to press any")
        audio = r.listen(source)
        print('Got you')
    try:
        WhatUSpoke = r.recognize_google(audio, language='ta-IN')
        if WhatUSpoke:
            print('What you spoke (Google):', WhatUSpoke)
            return WhatUSpoke
        else:
            print('No speech detected. Speak anything.')
            text_to_speech('Sorry, I did not catch you. Speak again')
            return None
    except:
        pass


def translate_text(text):
    translated = GoogleTranslator(source='auto', target='en').translate(text)
    print(translated)
    return translated

def translate_tamil(text):
    translated = GoogleTranslator(source='auto', target='tamil').translate(text)
    print(translated)
    return translated

def text_to_speech(text):
    tts = gTTS(text=text, lang='ta', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp) 
    fp.seek(0)
    song = AudioSegment.from_file(fp, format="mp3")
    play(song)

def audio():
    text = recognize_speech()
    translated_text = translate_text(text)
    res = custom2.chatbot(translated_text)
    tam = translate_tamil(res)
    text_to_speech(tam)

