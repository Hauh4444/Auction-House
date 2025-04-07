from mailersend import emails
from dotenv import load_dotenv
from cryptography.fernet import Fernet

import os

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
        cipher = Fernet(os.getenv("CIPHER_ENCRYPTION_KEY"))
        mailer = emails.NewEmail(cipher.decrypt(os.getenv("ENCRYPTED_MAILERSEND_API_TOKEN").encode()).decode())
        email_data = {
            "from": {"email": os.getenv("MAIL_DEFAULT_SENDER")},
            "to": [{"email": recipient} for recipient in recipients],
            "subject": subject,
            "text": body
        }

        try:
            response = mailer.send(email_data)
            return response
        except Exception as e:
            print(f"Unexpected error sending mail: {e}")
            return False