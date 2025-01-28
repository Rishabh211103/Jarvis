import urllib.parse
import webbrowser
import os
from sys import platform

# Detect the Chrome browser path based on the OS
def get_chrome_path():
    if platform == "linux" or platform == "linux2":
        return '/usr/bin/google-chrome'
    elif platform == "darwin":
        return 'open -a /Applications/Google\\ Chrome.app'
    elif platform == "win32":
        return r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    else:
        return None

# Open YouTube search in Chrome
def youtube(text_to_search):
    chrome_path = get_chrome_path()
    if chrome_path and os.path.exists(chrome_path):
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
        query = urllib.parse.quote(text_to_search)
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.get('chrome').open_new_tab(url)
    else:
        print("Google Chrome not found or unsupported OS.")
        webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(text_to_search)}")

# Main function
if __name__ == '__main__':
    search_query = "Jarvis"  # Example query
    youtube(search_query)
