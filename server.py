import argparse
from py_messenger import sms_client

# parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument("action", type=str, choices=['text'])
parser.add_argument('-n', action="store", dest="number")
parser.add_argument('-m', action="store", dest="message")
args = parser.parse_args()


def send_sms_message(destination_number: str, sms_message: str):
    sms_client.send_sms_message(destination_number, sms_message)


if args.action == 'text':
    send_sms_message(args.number, args.message)
