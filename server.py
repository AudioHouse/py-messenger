from flask import Flask, request, Response
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
    return Response(status=204)


@app.route('/outbound', methods=['POST'])
def outbound_sms():
    destination_number = request.json['destination']
    message = request.json['message']
    sms_client.send_sms_message(destination_number, message)
    return Response(status=204)


if __name__ == '__main__':
    app.run()
