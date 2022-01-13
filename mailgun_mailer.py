import requests
from content import subject, html, text
from dotenv import dotenv_values
from logger_config import configLogger
import csv

mailgun_logger = configLogger(__name__)

config = dotenv_values(dotenv_path=".env")

try:
    MAILGUN_API_KEY = config["MAILGUN_API_KEY"]
    FROM_NAME = config["FROM_NAME"]
    FROM_EMAIL = config["FROM_EMAIL"]
    DOMAIN = config["DOMAIN"]
except:
    mailgun_logger.exception("Improperly Configured Environment")
    exit({"error": "Improperly Configured Environment"})


def sendEmail(email):
    email = email.strip()
    data = {
        "from": f"{FROM_NAME} <{FROM_EMAIL}@{DOMAIN}>",
        "to": [email],
        "subject": subject,
        "html": html,
        "text": text
    }

    auth = ("api", MAILGUN_API_KEY)

    sent = requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages", auth=auth, data=data)

    if not sent.status_code == 200:
        mailgun_logger.error(
            f"Email not sent ({email}) - {sent.status_code}")
        print(sent.content)

        with open("unsent.csv", "a") as unsent_csv:
            csv_w = csv.writer(unsent_csv)
            csv_w.writerow([email])
    else:
        mailgun_logger.debug(f"Email - {email}")
        mailgun_logger.debug(f"Sent - {sent}")


# only to make sure that the code is working
def main():
    sendEmail("example@example.com")


if __name__ == "__main__":
    main()
