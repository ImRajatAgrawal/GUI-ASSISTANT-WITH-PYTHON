import pyttsx3
import wolframalpha
import speech_recognition as sr

client = wolframalpha.Client('L269XW-J26V9X4HP3')
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def myCommand():
    r = sr.Recognizer()
    r.energy_threshold = 400
    r.pause_threshold = 0.7
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source,timeout=3)
            query = r.recognize_google(audio, language='en-in')

    except sr.UnknownValueError:
            speak('Sorry sir! I didn\'t get that! Try typing the command!')
            query=""
    except sr.WaitTimeoutError:
        speak('Sorry sir! I didn\'t get that! Try typing the command!')
        query=""
    return query

