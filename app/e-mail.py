# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.message import EmailMessage


#email and password for account
gmail_user = 'leedsScooterRental@gmail.com'
gmail_password = 'S1lurIan_Per1od'

#Both methods send an email to a designated recipient

def sendConfirmationMessage(gmail_to, message):
    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = 'Confirmation of Scooter rental'
    msg['From'] = gmail_user
    msg['To'] = gmail_to

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login(gmail_user, gmail_password)
    s.send_message(msg)
    s.quit()


def sendConfirmationMessage(name, gmail_to, scooter_name, location, time, date, length):

    message = f'Hi {name},\nThis is an email to confirm your rental of scooter {scooter_name} on {date} at {time} for {length} hours at {location}.\nThanks for your business'
    
    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = 'Confirmation of Scooter rental'
    msg['From'] = gmail_user
    msg['To'] = gmail_to

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login(gmail_user, gmail_password)
    s.send_message(msg)
    s.quit()

#sendConfirmationMessage('Scott James', 'scottowenjames33@gmail.com', '27', 'Train station', '12:00', '27/03/2022', 4)