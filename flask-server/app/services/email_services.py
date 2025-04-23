from mailersend import emails
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import os

from ..utils.logger import setup_logger

load_dotenv()

logger = setup_logger(name="email_logger", log_file="logs/email.log")


class EmailService:
    @staticmethod
    def send_email(subject: str, recipients: list, body: str):
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
            logger.info(msg=f"Mail data: {email_data} sent successfully")
            return response
        except Exception as e:
            logger.error(msg=f"Mail data: {email_data} failed to send: {e}")
            return False