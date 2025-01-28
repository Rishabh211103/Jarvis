import urllib.parse
import webbrowser
import os
from sys import platform

# Detect the browser path based on the OS
def get_browser_path(browser="edge"):
    if platform == "linux" or platform == "linux2":
        if browser == "chrome":
            return '/usr/bin/google-chrome'
        elif browser == "firefox":
            return '/usr/bin/firefox'
    elif platform == "darwin":
        if browser == "chrome":
            return 'open -a /Applications/Google\\ Chrome.app'
        elif browser == "firefox":
            return 'open -a /Applications/Firefox.app'
    elif platform == "win32":
        if browser == "chrome":
            return r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        elif browser == "firefox":
            return r'C:\Program Files\Mozilla Firefox\firefox.exe'
    else:
        return None

# Open YouTube search in the specified browser
def youtube(text_to_search, browser="chrome"):
    browser_path = get_browser_path(browser)
    if browser_path and os.path.exists(browser_path):
        webbrowser.register(browser, None, webbrowser.BackgroundBrowser(browser_path))
        query = urllib.parse.quote(text_to_search)
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.get(browser).open_new_tab(url)
    else:
        print(f"{browser.capitalize()} not found or unsupported OS. Opening in default browser.")
        webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(text_to_search)}")

# Main function
if __name__ == '__main__':
    search_query = "Jarvis"  # Example query
    preferred_browser = "edge"  # You can change this to "firefox" or any other supported browser
    youtube(search_query, preferred_browser)
