import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "iotinnovation832@gmail.com"
password = "kqyn pcun yyng nkpu"


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


notifier = None
