import logging
import smtplib
import ssl
from email.message import EmailMessage


# Configure logging
logging.basicConfig(
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class SendEmailPipeline:
    """
    This pipeline sends an email with the provided body text to a list of receivers.
    """

    def __init__(self):
        self.sender_email = "ibm.hackaton.ai@gmail.com"
        self.app_password = "zslv iafx oihh kbsm" 
        self.receivers = ["citycouncilspain@gmail.com", "javierechavarren11@gmail.com"]
        self.subject = "Anomaly Detected in Water Tank Sensor Data"
        

    def send_email(self, body: str):
        """
        Sends an email with the provided body.

        Parameters:
        body (str): Body of the email message.
        """
        try:
            msg = EmailMessage()
            msg["From"] = self.sender_email
            msg["Subject"] = self.subject
            msg.set_content(body)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(self.sender_email, self.app_password)
                for receiver in self.receivers:
                    msg["To"] = receiver
                    smtp.send_message(msg)
                    del msg["To"]

            logging.info("Email successfully sent.")
            return {"message" :"Email successfully sent."}
        
        except Exception as e:
            logging.error(f"Failed to send email: {e}")

    # def invoke(self, water_info: str) -> str:
    #     """
    #     Creates the message and sends an email.
    #     """
    #     response = self.analysis_chain.invoke({"water_data": water_info})

    #     # Send email with the generated response
    #     self.send_email(response)

    #     return response

##Test
# pipeline = CreateMessagesPipeline()

# pipeline.send_email("Hola Caracola sábado a las 12:20")