from . import scheduler

message_cache = []


class MedProfile:
    # A zero represents medicine was not taken
    taken_list = [0, 0, 0, 0]
    last_taken = scheduler.get_zero_time()
    last_sent = scheduler.get_zero_time()

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
        print("sending message")
        self.last_sent = scheduler.get_time_now()

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
            print("It has not been 4 hours since last dose")


med_profile = MedProfile()


def run():
    # If the time of day is between 9-11
    if scheduler.check_active_range():
        med_profile.notify_for_dosage()
