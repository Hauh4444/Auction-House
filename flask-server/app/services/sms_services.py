from ozekilibsrest import Configuration, Message, MessageApi
import os
from ..utils.logger import setup_logger

logger = setup_logger(name="sms_logger", log_file="logs/sms.log")


class SMSService:
    @staticmethod
    def send_sms(recipient_number, message_text):
        try:
            configuration = Configuration(
                username=os.getenv("OZEKI_USERNAME"),
                password=os.getenv("OZEKI_PASSWORD"),
                api_url=os.getenv("OZEKI_API_URL")
            )

            api = MessageApi(configuration)

            msg = Message()
            msg.sender = os.getenv("SMS_SENDER")
            msg.recipients = [recipient_number]
            msg.text = message_text

            response = api.send(msg)

            logger.info(f"SMS sent to {recipient_number}: {message_text}")
            return response.http_code

        except Exception as e:
            logger.error(f"Failed to send SMS to {recipient_number}: {str(e)}")
            return 500