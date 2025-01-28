import requests
from bs4 import BeautifulSoup
import pyttsx3
import smtplib

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def send_email(subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('youremail@gmail.com', 'yourpassword')  # Use app password here for security
        content = f"Subject: {subject}\n\n{body}"
        server.sendmail('youremail@gmail.com', 'receiveremail@gmail.com', content)
        server.close()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def check_price():
    URL = 'https://www.amazon.in/WOW-Brightening-Vitamin-Face-Wash/dp/B07SZ243VZ/ref=sr_1_6?dchild=1&keywords=wow+face+wash&qid=1594306550&smid=A27LPMZIGZ21IK&sr=8-6'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get product title
    title = soup.find(id='productTitle')
    title_text = title.get_text().strip() if title else "Product not found"

    # Get price
    price_element = soup.find(id='priceblock_dealprice') or soup.find(id='priceblock_ourprice')
    if price_element:
        price_text = price_element.get_text().strip()
        price = float(price_text.replace('₹', '').replace(',', '').strip())

        # Notify user
        speak(f"The price of {title_text} is {price_text}")

        # Check if price is below threshold
        if price < 300.0:  # Example threshold
            send_email(
                subject="Price Alert!",
                body=f"The price of {title_text} has dropped to {price_text}. Check the link: {URL}"
            )
    else:
        speak("Price not found!")
        print("Unable to fetch price. The product may be out of stock or the page structure has changed.")


# Call the function
check_price()
