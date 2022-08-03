from django import template
register = template.Library()
import pyttsx3
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
#from gtts.tts import gTTS