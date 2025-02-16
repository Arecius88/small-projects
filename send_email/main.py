import smtplib
from email.message import EmailMessage

textfile = "send_email/message.txt"

with open(textfile) as fp:
    msg = EmailMessage()
    msg.set_content(fp.read())

msg["Subject"] = f"The contents of {textfile}"
msg["From"] = "arecius88.mail@gmail.com"
msg["To"] = "arecius88.mail+temp@gmail.com"

s = smtplib.SMTP("localhost")
s.send_message(msg)
s.quit()