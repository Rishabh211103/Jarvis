import requests
import json
import pyttsx3
from datetime import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()


def fetch_news(api_key):
    """Fetch top headlines from NewsAPI."""
    current_date = datetime.now().strftime('%Y-%m-%d')  # Get today's date (2025 format)
    url = f'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey={api_key}&from={current_date}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        speak("Sorry, I am unable to fetch the news at the moment.")
        return None


def speak_news(api_key):
    """Fetch and speak top news headlines."""
    news_data = fetch_news(api_key)
    if news_data and news_data.get('status') == 'ok':
        articles = news_data.get('articles', [])
        if not articles:
            speak("No news articles found. Please try again later.")
            return

        speak('Source: The Times Of India.')
        speak('Today\'s headlines are:')
        for index, article in enumerate(articles[:5]):  # Limit to top 5 headlines
            speak(article.get('title', 'No title available.'))
            if index < len(articles) - 1:
                speak('Moving on to the next news headline.')
        speak('These were the top headlines. Have a nice day!')
    else:
        speak("Failed to fetch news. Please check the API key or your internet connection.")


if __name__ == '__main__':
    # Replace 'yourapikey' with your actual NewsAPI key
    API_KEY = '7fa2bc71a4194cc8897977785eb0d6fe'  # Replace with your valid API key
    if API_KEY == 'yourapikey':
        print("Error: Please replace 'yourapikey' with your actual NewsAPI key.")
        speak("Please provide a valid News API key in the code.")
    else:
        speak_news(API_KEY)
