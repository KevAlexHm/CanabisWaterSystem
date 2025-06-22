EMAIL_MESSAGES = {
    "last_watered": {
        "subject": "Raspberry Pi: Plant Watering Time",
        "message": "Your plant was last watered at",
    },
    "check_water_level": {
        "subject": "Raspberry Pi: Check Water Level",
        "message": "Check your water level!",
    },
}


class EmailNotifier:

    def send_email(self, time_last_watered, subject, message):
        # To-Do email implementation
        if time_last_watered == False:
            complete_message = "Subject: {}\n\n{}".format(subject, message)
        else:
            complete_message = "Subject: {}\n\n{} {}".format(
                subject, message, time_last_watered
            )

    def send_last_watered_email(self, time_last_watered):
        message = EMAIL_MESSAGES["last_watered"]["message"]
        subject = EMAIL_MESSAGES["last_watered"]["subject"]
        self.send_email(time_last_watered, subject, message)

    def send_check_water_level_email(self):
        message = EMAIL_MESSAGES["check_water_level"]["message"]
        subject = EMAIL_MESSAGES["check_water_level"]["subject"]
        self.send_email(False, subject, message)
