import os


class Config:
    tw_ssid = os.getenv('TW_SSID')
    tw_auth_token = os.getenv('TW_AUTH_TOKEN')
    tw_phone_number = os.getenv('TW_PHONE_NUMBER')
