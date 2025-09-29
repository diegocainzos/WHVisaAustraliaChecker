from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
### EMAIL
def send_email(subject, body):
    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("APP_PASSWORD")
    receiver_email = os.getenv("EMAIL")  # si el receptor es distinto, usa otra var

    # Comprobaciones explícitas y seguras (no mostramos secretos)
    if not sender_email:
        raise RuntimeError("Env var EMAIL no encontrada o vacía.")
    if not sender_password:
        raise RuntimeError("Env var APP_PASSWORD no encontrada o vacía.")

    print("EMAIL presente:", bool(sender_email))
    print("APP_PASSWORD presente:", bool(sender_password))
    print("EMAIL length:", len(sender_email))
    print("APP_PASSWORD length:", len(sender_password))

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)  # aquí falla si password es None
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error al enviar email:", e)
        raise




url = "https://immi.homeaffairs.gov.au/what-we-do/whm-program/status-of-country-caps"
html_doc = requests.get(url).text
soup = BeautifulSoup(html_doc, 'html.parser')
spain_td = soup.find("td", string="Spain")
status = spain_td.next_sibling.text

if "paused" not in status:
    print("ya no esta pausado")
    send_email("VISA AUSTRALIA ABIERTA", "Spain WHM Available!")

else:
    print("sigue pausado")
    send_email("sigue pausado nano", "Spain WHM Not Available!")
