import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "iotinnovation832@gmail.com"
password = "kqyn pcun yyng nkpu"

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

    def __init__(self):
        self.sender_email = sender_email
        self.password = password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, receiver_email, subject, body):

        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(message)
                print("[System] Email sent successfully.")

        except Exception as e:
            print(f"[System] Failed to send email: {e}")

        """
        # To-Do email implementation
        if time_last_watered == False:
            complete_message = "Subject: {}\n\n{}".format(subject, message)
        else:
            complete_message = "Subject: {}\n\n{} {}".format(
                subject, message, time_last_watered
            )
        """

    def send_last_watered_email(self, time_last_watered):
        message = EMAIL_MESSAGES["last_watered"]["message"]
        subject = EMAIL_MESSAGES["last_watered"]["subject"]
        self.send_email(time_last_watered, subject, message)

    def send_check_water_level_email(self):
        message = EMAIL_MESSAGES["check_water_level"]["message"]
        subject = EMAIL_MESSAGES["check_water_level"]["subject"]
        self.send_email(False, subject, message)


notifier = None

# https://www.youtube.com/watch?v=a13yJ_XyLwg
