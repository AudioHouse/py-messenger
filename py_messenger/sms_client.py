from twilio.rest import Client
from py_messenger.config import Config

# Setup 
SSID = Config.tw_ssid
AUTH_TOKEN = Config.tw_auth_token
TWILIO_NUMBER = Config.tw_phone_number
TWILIO_CLIENT = Client(SSID, AUTH_TOKEN)


def send_sms_message(destination_number: str, sms_message: str) -> None:
    TWILIO_CLIENT.messages.create(to=destination_number, from_=TWILIO_NUMBER, body=sms_message)
