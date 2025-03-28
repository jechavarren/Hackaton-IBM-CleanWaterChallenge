import smtplib
import ssl
from email.message import EmailMessage
from io import BytesIO


sender = "ibm.hackaton.ai@gmail.com"
password = "zslv iafx oihh kbsm" # usar contraseña de aplicación de gmail: app password https://myaccount.google.com/u/4/apppasswords
receivers = ['halbix@gmail.com']
subject = 'Anomaly Detected in Water Tank Sensor Data'

def SendEmail(body: str): 
    """
    Sends an email to one or more recipients with the provided body.

    Parameters:
    body (str): Body of the email message.

    Returns:
    str: Confirmation message if the email is sent successfully.

    """
 
    # Create the email message
    msg = EmailMessage()
    msg['From'] = sender
    msg['Subject'] = subject
    msg.set_content(body)
    
    # Set up SMTP connection
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender, password)
        for receiver in receivers:
            msg['To'] = receiver
            smtp.send_message(msg)
            del msg['To']  # Remove recipient for the next iteration
    
    print("Email successfully sent")
    return "Email successfully sent"

# SendEmail("test email")
