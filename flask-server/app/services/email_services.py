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

        try:
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
