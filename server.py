from flask import Flask, request
from twilio import twiml

from py_messenger import sms_client

app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    print(f'Received a message from {number}: {message_body}')

    # resp = twiml.Response()
    # resp.message('Hello {}, you said: {}'.format(number, message_body))
    # return str(resp)


if __name__ == '__main__':
    app.run()
