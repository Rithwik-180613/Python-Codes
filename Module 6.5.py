import speech_recognition as sr
import pyttsx3
from datetime import datetime

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return None

def respond_to_command(command):
    command = command.lower()
    if "time" in command:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
    elif "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "your name" in command:
        speak("I am your voice assistant.")
    elif "stop" in command:
        speak("Goodbye!")
        return False
    else:
        speak("Sorry, I don't understand that command.")


def main():
    speak("Hello! I am your voice assistant. How can I help you?")
    while True:
        command = get_audio()
        if command:
            if not respond_to_command(command):
                break                                       

if __name__ == "__main__":
    main()
