import smtplib
import inspect
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import csv
from time import sleep
address_list = []
with open('emails.csv', newline='') as csvfile:
    address = csv.reader(csvfile)
    for lines in address:
        address_list.append(lines[0])
for adress in address_list:
    # Email configuration
    sender_email = "example@gmail.com"
    receiver_email = adress
    password = "app token from gmail"
    subject = "Subject"
    ccreceivers = "ccreceivers@gmail.com"
    body_file = open("body.txt","r")
    body = body_file.read()
    # Create a MIMEMultipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg['CC'] = ccreceivers

    mim = MIMEText(body,'html')
    # Attach the email body
    msg.attach(MIMEText(body, 'html'))

    # Specify the file to be attached
    file_path = "attachment.pdf"
    file_name = os.path.basename(file_path)

    # Open the file in binary mode and attach it to the email
    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode the payload in base64
    encoders.encode_base64(part)

    # Add a header to the attachment
    ''' part.add_header(
        "Content-Disposition",
        "attachment; filename=filename.pdf"
    )'''
    part.add_header('Content-Disposition', 'attachment', filename='filename.pdf')

    # Attach the file to the message
    msg.attach(part)

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP('smtp.gmail.com') as server:  # Use your email provider's SMTP server
            server.starttls()
            server.ehlo()
            server.login(sender_email, password)
            server.send_message(msg)
            server.close()
            print(f'successfully sent the mail to {adress}')
    except Exception as e:
        print(f"Failed to send email to {adress} : {e}")

    sleep(0.5)
