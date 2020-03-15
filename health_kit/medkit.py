from . import scheduler


class MedProfile:
    # A zero represents medicine was not taken
    taken_list = [0, 0, 0, 0]
    last_taken = scheduler.get_empty_time()

    def check_if_medicine_taken(self):
        # If it's been more than 4 hours since last alert
        if scheduler.get_time_now() > scheduler.add_hours(self.last_taken, 4):
            # If taken list is not full
            if 0 in self.taken_list:
                for i, ele in enumerate(self.taken_list):
                    if ele == 0:
                        self.taken_list[i] = 1
                        break
            print(self.taken_list)
            print("I'm gonna send a message!")


med_profile = MedProfile()


def run():
    # If the time of day is between 9-11
    if scheduler.check_active_range():
        med_profile.check_if_medicine_taken()
