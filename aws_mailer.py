import boto3
from botocore.exceptions import ClientError
from content import html, subject, text
from dotenv import dotenv_values
from logger_config import configLogger
import csv

aws_logger = configLogger(__name__)

config = dotenv_values(dotenv_path=".env")

try:
    AWS_REGION = config["AWS_REGION"]
    FROM_NAME = config["FROM_NAME"]
    FROM_EMAIL = config["FROM_EMAIL"]
    DOMAIN = config["DOMAIN"]
except:
    aws_logger.exception("Improperly Configured Environment")
    exit({"error": "Improperly Configured Environment"})

SENDER = f"{FROM_NAME} <{FROM_EMAIL}@{DOMAIN}>"
CHARSET = "UTF-8"

client = boto3.client('ses', region_name=AWS_REGION)


def sendEmail(email):
    email = email.strip()
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    email,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': html,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': text,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:

        aws_logger.error(f"Email not sent ({email})")
        print({e.response['Error']['Message']})

        with open("unsent.csv", "a") as unsent_csv:
            csv_w = csv.writer(unsent_csv)
            csv_w.writerow([email])
    else:
        aws_logger.debug(f"Email - {email}")
        aws_logger.debug(f"Sent - Message ID = {response['MessageId']}")


# only to make sure that the code is working
def main():
    sendEmail("example@example.com")


if __name__ == "__main__":
    main()
