import speech_recognition as sr
import pyttsx3
import time
from googletrans import Translator
translator = Translator()

def speak(text, language='en'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    if language == 'en':
        engine.setProperty('voice', voices[0].id)  # English voice
    else:
        engine.setProperty('voice', voices[1].id)  # Other language voice (may vary based on system)
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
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

def translate_text(text, target_language, max_retries):
    for attempt in range(max_retries):
        try:
            translated = translator.translate(text, dest=target_language)
            print(f"Translated text: {translated.text}")
            return translated.text
        except Exception as e:
            print(f"Translation attempt {attempt + 1} failed: {e}")
            time.sleep(1)  # Wait before retrying
    print("Max retries reached. Translation failed.")
    return None

def display_language_options():
    languages = {
        '1': 'en',  # English
        '2': 'es',  # Spanish
        '3': 'fr',  # French
        '4': 'de',  # German
        '5': 'zh-cn',  # Chinese (Simplified)
        '6': 'te' # Telugu
    }
    print("Select a language to translate to:")
    for key, value in languages.items():
        print(f"{key}: {value}")
    return languages


def main():
    languages = display_language_options()
    choice = input("Enter the number corresponding to your choice: ")
    target_language = languages.get(choice, 'en')  # Default to English if invalid choice

    text = speech_to_text()
    if text:
        translated_text = translate_text(text, target_language, max_retries=3)
        if translated_text:
            engine = pyttsx3.init()
            engine.say(translated_text)
            engine.runAndWait()


if __name__ == "__main__":
    main()