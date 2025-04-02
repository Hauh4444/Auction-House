import os
from mailersend import emails
from dotenv import load_dotenv
from cryptography.fernet import Fernet

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
        cipher = Fernet(os.getenv('ENCRYPTION_KEY'))
        MAILERSEND_API_KEY = cipher.decrypt(os.getenv('ENCRYPTED_API_KEY').encode()).decode()

        mailer = emails.NewEmail(MAILERSEND_API_KEY)

        email_data = {
            'from': {
                'email': os.getenv('MAIL_DEFAULT_SENDER')
            },
            'to': [{'email': recipient} for recipient in recipients],
            'subject': subject,
            'text': body
        }

        try:
            response = mailer.send(email_data)
            return response.status_code == 202
        except Exception as e:
            print(e)
            return False