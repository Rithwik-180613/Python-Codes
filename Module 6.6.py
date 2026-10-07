import speech_recognition as sr 
import pyttsx3
from googletrans import Translator

def speak(text, language='en'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    if language == 'en':
        engine.setProperty('voice', voices[0].id)  # English voice
    else:
        engine.setProperty('voice', voices[1].id)  # Spanish voice
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

def translate_text(text, target_language='es'):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text  

def display_language_options():
    print("Select a language to translate to:")
    print("1. English")
    print("2. Spanish")
    print("3. French")
    print("4. German")
    print("5. Italian")
    print("6. Portuguese")
    print("7. Russian")
    print("8. Chinese")
    language = input("Enter the number corresponding to your choice: ")

    language_dict = {
        '1': 'English',
        '2': 'Spanish',
        '3': 'French',
        '4': 'German',
        '5': 'Italian',
        '6': 'Portuguese',
        '7': 'Russian',
        '8': 'Chinese',
    }

    return language_dict.get(language, 'English')  # Default to English if invalid input


def main():
    target_language = display_language_options()
    original_text = speech_to_text()
    if original_text:
        translated_text = translate_text(original_text, target_language=target_language.lower())
        print(f"Translated text ({target_language}): {translated_text}")
        speak(translated_text, language=target_language.lower())    

if __name__ == "__main__":
    main()