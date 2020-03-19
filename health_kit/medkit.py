from . import scheduler
from py_messenger import sms_client as sms, config

message_cache = []
destination_number = config.Config.destination_number


class TextProfile:
    test = 'Hello! It is time to take your medicine! Have you taken it yet?'

    def ask_if_taken(self):
        return self.test


class MedProfile:
    # A zero represents medicine was not taken
    taken_list = [0, 0, 0, 0]
    last_taken = scheduler.get_zero_time()
    last_sent = scheduler.get_zero_time()
    text_profile = TextProfile()

    @staticmethod
    def check_yes_in_cache():
        global message_cache
        for elem in message_cache:
            if 'Yes' in str(elem) or 'yes' in str(elem):
                return True
        return False

    def update_dosage_list(self):
        for i, ele in enumerate(self.taken_list):
            if ele == 0:
                self.taken_list[i] = 1
                break

    def update_state(self):
        global message_cache
        self.last_taken = scheduler.get_time_now()
        self.update_dosage_list()
        message_cache = []

    def send_dosage_alert(self):
        print("Sending dosage alert")
        sms.send_sms_message(destination_number, self.text_profile.ask_if_taken())
        self.last_sent = scheduler.get_time_now()

    def print_status(self):
        print(f'Med-Profile Status: taken-list: {self.taken_list}, '
              f'last-taken: {self.last_taken}, '
              f'last_sent: {self.last_sent}')

    def notify_for_dosage(self):
        # If it's been more than 4 hours since last dosage
        if scheduler.get_time_now() > scheduler.add_hours(self.last_taken, 4):
            # If dosage list is not full
            if 0 in self.taken_list:
                if self.check_yes_in_cache():
                    self.update_state()
                else:
                    # If it's been more than 30 min since last message sent
                    if scheduler.get_time_now() > scheduler.add_minutes(self.last_sent, 30):
                        self.send_dosage_alert()
                    else:
                        print(f"Message already sent on: {self.last_sent}. Waiting.")

        else:
            print("It has not been 4 hours since last dose")


med_profile = MedProfile()


def run():
    # If the time of day is between 9-11
    if scheduler.check_active_range():
        med_profile.notify_for_dosage()
