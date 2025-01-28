import pyttsx3
import pyautogui
import psutil
import pyjokes
import speech_recognition as sr
import json
import requests
import geocoder
from difflib import get_close_matches


# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Load dictionary data
try:
    data = json.load(open('data.json'))
except FileNotFoundError:
    print("Error: 'data.json' file not found!")
    exit()

# Get location data
g = geocoder.ip('me')


def speak(audio) -> None:
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()


def screenshot() -> None:
    """Take a screenshot and save it to a specified path."""
    try:
        img = pyautogui.screenshot()
        img.save('screenshot.png')  # Save screenshot in the current directory
        speak("Screenshot taken and saved successfully.")
    except Exception as e:
        speak("Failed to take a screenshot.")
        print(f"Error: {e}")


def cpu() -> None:
    """Provide CPU and battery status."""
    try:
        usage = psutil.cpu_percent(interval=1)
        battery = psutil.sensors_battery()
        speak(f"CPU usage is at {usage} percent.")
        speak(f"Battery is at {battery.percent} percent.")
    except Exception as e:
        speak("Unable to fetch CPU or battery information.")
        print(f"Error: {e}")


def joke() -> None:
    """Speak 5 random jokes."""
    try:
        jokes = pyjokes.get_jokes()
        for i in range(5):
            speak(jokes[i])
    except Exception as e:
        speak("Unable to fetch jokes.")
        print(f"Error: {e}")


def takeCommand() -> str:
    """Listen to the user's voice command."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.energy_threshold = 494
        r.adjust_for_ambient_noise(source, duration=1.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return None

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f'User said: {query}\n')
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that. Please repeat.")
        return None
    except sr.RequestError:
        print("Error: Unable to connect to the recognition service.")
        return None


def weather() -> None:
    """Fetch and speak the current weather information."""
    try:
        api_url = f"https://fcc-weather-api.glitch.me/api/current?lat={g.latlng[0]}&lon={g.latlng[1]}"
        data_json = requests.get(api_url).json()

        if data_json.get('cod') == 200:
            main = data_json['main']
            wind = data_json['wind']
            weather_desc = data_json['weather'][0]

            speak(f"Latitude: {data_json['coord']['lat']}, Longitude: {data_json['coord']['lon']}.")
            speak(f"Current location is {data_json['name']}, {data_json['sys']['country']}.")
            speak(f"Weather type: {weather_desc['main']}.")
            speak(f"Wind speed is {wind['speed']} meters per second.")
            speak(f"Temperature: {main['temp']} degree Celsius.")
            speak(f"Humidity is {main['humidity']} percent.")
        else:
            speak("Unable to fetch weather data. Please try again later.")
    except Exception as e:
        speak("Failed to retrieve weather information.")
        print(f"Error: {e}")


def translate(word: str) -> None:
    """Translate the word using the loaded dictionary."""
    word = word.lower()
    if word in data:
        speak(data[word])
        print(data[word])  # Optional: Print definition for reference
    elif len(get_close_matches(word, data.keys())) > 0:
        closest_match = get_close_matches(word, data.keys())[0]
        speak(f"Did you mean {closest_match} instead? Respond with 'yes' or 'no'.")
        print(f"Did you mean {closest_match} instead?")

        ans = takeCommand()
        if ans and 'yes' in ans.lower():
            speak(data[closest_match])
            print(data[closest_match])  # Optional: Print definition for reference
        elif ans and 'no' in ans.lower():
            speak("Word doesn't exist. Please make sure you spelled it correctly.")
        else:
            speak("I did not understand your response.")
    else:
        speak("Word doesn't exist. Please double-check it.")


if __name__ == '__main__':
    while True:
        speak("How can I assist you? Say 'exit' to quit.")
        print("How can I assist you? (Say 'exit' to quit):")
        command = takeCommand()
        if command:
            if 'exit' in command.lower():
                speak("Goodbye!")
                break
            elif 'screenshot' in command.lower():
                screenshot()
            elif 'cpu' in command.lower() or 'battery' in command.lower():
                cpu()
            elif 'joke' in command.lower():
                joke()
            elif 'weather' in command.lower():
                weather()
            elif 'translate' in command.lower():
                speak("Please say the word to translate.")
                print("Say the word to translate:")
                word = takeCommand()
                if word:
                    translate(word)
            else:
                speak("Sorry, I didn't understand that. Please try again.")
        else:
            speak("I did not catch that. Please try again.")
