import json
import logging
import smtplib
import ssl
from email.message import EmailMessage
from typing import Optional

import pandas as pd
from langchain_core.output_parsers import JsonOutputParser

from .models import ModelFactory
from .prompts import PromptFactory

# Configure logging
logging.basicConfig(
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class CreateMessagesPipeline:
    """
    Pipeline to make a review of water analysis results and send an email.
    """

    def __init__(self):
        self.sender_email = "ibm.hackaton.ai@gmail.com"
        self.app_password = "zslv iafx oihh kbsm"  # Usa una contraseña de aplicación de Gmail
        self.receivers = ["citycouncilspain@gmail.com"]
        self.subject = "Anomaly Detected in Water Tank Sensor Data"
        
        model_gpt4 = ModelFactory.factory_method(
            temperature=0.0,
            model="gpt-4",
        )

        prompt = PromptFactory.factory_method(
            domain="describe_water_data",
        )["describe_water_data"]["PROMPT"]

        self.analysis_chain = prompt | model_gpt4
        logging.info("DescribeWaterGPT initialized successfully.")

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
        except Exception as e:
            logging.error(f"Failed to send email: {e}")

    def invoke(self, water_info: str) -> str:
        """
        Creates the message and sends an email.
        """
        response = self.analysis_chain.invoke({"water_data": water_info})

        # Send email with the generated response
        self.send_email(response)

        return response
