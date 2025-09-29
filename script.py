from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
### EMAIL

def send_email(subject, body):
    # Email configuration
    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("APP_PASSWORD")
    receiver_email = os.getenv("EMAIL")
    print("el sender es", sender_email)
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    message.attach(MIMEText(body, "plain"))
    
    # Send email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")



url = "https://immi.homeaffairs.gov.au/what-we-do/whm-program/status-of-country-caps"
html_doc = requests.get(url).text
soup = BeautifulSoup(html_doc, 'html.parser')
spain_td = soup.find("td", string="Spain")
status = spain_td.next_sibling.text

if "paused" not in status:
    print("ya no esta pausado")
else:
    print("sigue pausado")
    send_email("sigue pausado nano", "Spain WHM Not Available!")
