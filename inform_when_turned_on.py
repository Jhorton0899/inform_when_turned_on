import cv2
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time
import os 
import requests



photo_storage = "C:\\Users\\vturn\\OneDrive\\email_photos"
def get_location():
    response = requests.get('http://ipinfo.io/json')
    data = response.json()
    city = data.get('city', 'City not found')
    region = data.get('region', 'Region not found')
    return(city, region)

def take_photo(phot_storage):
    save_path = photo_storage
    cap = cv2.VideoCapture(0) 
    time.sleep(10) 
    ret, frame = cap.read()  
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
    filename = "login_photo_{}.jpg".format(timestamp)
    full_path = os.path.join(save_path, filename) 
    
    if ret:
        cv2.imwrite(full_path, frame)  
    cap.release()  
    return full_path if ret else None  
  
def send_email_with_photo(photo_path):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
    sender_email = 'Sender_email@Email.com'
    sender_password = os.getenv('email', 'vmsq mzij cylj syyz ') 
    smtp_server = "smtp.gmail.com"
    receiver_email = 'Receiver_Email@Email.com'
    port = 587
    message = MIMEMultipart()
    message["Subject"] = "Activity Alert"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    
    city, state = get_location()
    body_text = ("User logged in on {} from {}, {}. See the attached photo.".format(timestamp, city, state))
    body = MIMEText(body_text, "plain")
    message.attach(body)

    if photo_path:
        with open(photo_path, "rb") as f:
            photo = MIMEImage(f.read())
            photo.add_header('Content-Disposition', f'attachment; filename="{photo_path}"')
            message.attach(photo)

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email: {}".format(e))
        
photo_path = take_photo(photo_storage)
if photo_path:
    send_email_with_photo(photo_path)
else:
    print("Failed to take photo.")