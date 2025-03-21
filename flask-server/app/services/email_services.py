import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

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
        message = Mail(
            from_email=os.getenv('MAIL_DEFAULT_SENDER'),
            to_emails=recipients,
            subject=subject,
            plain_text_content=body
        )
        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
            return response.status_code == 202
        except Exception as e:
            print(e.message)
            return False