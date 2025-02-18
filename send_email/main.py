import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email Config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADRESS= os.getenv("EMAIL_ADRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(recipient_email:str, title:str, body:str)->None:
    
    try:
        message = MIMEMultipart()
        message["From"] = EMAIL_ADRESS
        message["To"] = recipient_email
        message["Subject"] = title
        
        message.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADRESS, recipient_email, message.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")
        
        
if __name__ == "__main__":
    recipient_email = "arecius88.mail@gmail.com"
    title = "Test Email"
    body = "This is a test email"
    send_email(recipient_email, title, body)
    
    #print(EMAIL_ADRESS)
    #print(EMAIL_PASSWORD)