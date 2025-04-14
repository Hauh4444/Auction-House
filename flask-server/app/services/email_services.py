from mailersend import emails
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from ..utils.logger import setup_logger

import os

email_logger = setup_logger("email", "logs/email.log")

load_dotenv()  # Load environment variables from .env file


class EmailService:
    @staticmethod
    def send_email(subject, recipients, body):
        """
        Sends an email with the given subject, recipients, and body.

        Args:
            subject (str): The subject of the email.
            recipients (list): A list of recipient email addresses.
            body (str): The body of the email.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        cipher = Fernet(os.getenv('CIPHER_ENCRYPTION_KEY'))
        mailer = emails.NewEmail(cipher.decrypt(os.getenv('ENCRYPTED_MAILERSEND_API_KEY').encode()).decode())

        email_data = {
            'from': {'email': os.getenv('MAIL_DEFAULT_SENDER')},
            'to': [{'email': recipient} for recipient in recipients],
            'subject': subject,
            'text': body
        }

        try:
            response = mailer.send(email_data)
            email_logger.info(os.getenv('MAIL_DEFAULT_SENDER') + " successfully sent an email to " + recipients)
            return response
        except Exception as e:
            email_logger.error("Unexpected error sending mail")
            print(f"Unexpected error sending mail: {e}")
            return False