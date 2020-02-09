from flask import Flask, request
from py_messenger import sms_client

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    return str('Hey, this is py-messenger!')


@app.route('/inbound', methods=['POST'])
def inbound_sms():
    number = request.form['From']
    message_body = request.form['Body']
    print(f'Received a message from {number}: {message_body}')
    return str('OK')


@app.route('/outbound', methods=['POST'])
def outbound_sms():
    destination_number = request.json['destination']
    message = request.json['message']
    sms_client.send_sms_message(destination_number, message)
    return str('OK')


if __name__ == '__main__':
    app.run()
