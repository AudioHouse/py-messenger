from flask import Flask, request, Response
import threading
import time
from health_kit import medkit

app = Flask(__name__)

server_state = False


class SubThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global server_state
        while True:
            if not server_state:
                print("END: Exiting thread...")
                break
            medkit.run()
            time.sleep(5)


# Init the global var used to hold the thread
init_thread = SubThread()


def stop_if_msg_stop(msg):
    global server_state
    if 'Off' in str(msg) or 'off' in str(msg) or 'OFF' in str(msg):
        server_state = False


def start_if_msg_start(msg):
    global server_state
    if 'Start' in str(msg) or 'start' in str(msg) or 'START' in str(msg):
        server_state = True


@app.route('/', methods=['GET'])
def health_check():
    global server_state
    return str('Health-Kit flask-server up and running! The current thread-state is: ' + str(server_state))


@app.route('/state')
def toggle_on_off():
    global server_state
    global init_thread
    if not server_state:
        server_state = True
        init_thread = SubThread()
        init_thread.start()
        print(f'Request: Turned on health-kit')
        return "Health-Kit has been toggled ON"
    else:
        server_state = False
        print(f'Request: Turned off health-kit')
        return "Health-Kit has been toggled OFF"


@app.route('/inbound', methods=['POST'])
def inbound_sms():
    number = request.form['From']
    message_body = request.form['Body']
    print(f'Received a message from {number}: {message_body}')

    # if msg has START, then start new thread
    start_if_msg_start(message_body)

    # if msg has STOP, then shut down the thread
    stop_if_msg_stop(message_body)

    medkit.receive_message(message_body)
    return Response(status=204)


# Start the first thread
toggle_on_off()

if __name__ == '__main__':
    app.run()
