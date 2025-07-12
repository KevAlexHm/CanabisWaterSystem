import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Sender's email and app-specific Gmail password (for SMTP authentication)
sender_email = "iotinnovation832@gmail.com"
password = "kqyn pcun yyng nkpu"


# EmailNotifier class handles sending emails
class EmailNotifier:

    def __init__(self):
        # Initialize SMTP server configuration
        self.sender_email = sender_email
        self.password = password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587  # Port used for TLS encryption

    def send_email(self, receiver_email, subject, body):

        try:
            # Create the email message structure
            message = MIMEMultipart()
            # Setting the sender of the e-mail
            message["From"] = self.sender_email
            # Setting the receiver of the e-mail
            message["To"] = receiver_email
            # Setting the subject of the e-mail
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))  # Add plain text body to the email

            # Connect to the Gmail SMTP server and send the email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                # Secure the connection with TLS
                server.starttls()
                # Log in with sender credentials
                server.login(self.sender_email, self.password)
                # Send the composed email
                server.send_message(message)
                print("[System] Email sent successfully.")

        except Exception as e:
            # Handle and print any errors that occur during the process
            print(f"[System] Failed to send email: {e}")


# Global notifier instance (to be initialized later in the application)
notifier = None
