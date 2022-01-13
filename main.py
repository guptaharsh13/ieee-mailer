from aws_mailer import sendEmail as aws
from mailgun_mailer import sendEmail as mailgun
import csv
import time

choices = [aws, mailgun]


def main():
    temp_emails = []
    with open("emails.csv") as emails_csv:
        emails = csv.reader(emails_csv)
        for email in emails:
            temp_emails.append(email[0])

    emails = temp_emails

    print("\nChoose any service - \n")
    print("1. AWS Simple Email Service")
    print("2. MAILGUN")
    choice = input("\nEnter your choice\n")
    if not (choice == "1" or choice == "2"):
        exit({"error": "INVALID CHOICE"})

    choice = int(choice)
    sendEmail = choices[choice-1]

    print("\n\nEmails\n")

    for email in emails:
        print(email)

    print(f"\nNumber of emails = {len(emails)}")
    cont = input("\nDo you want to continue\n")
    if not cont.lower() == "y":
        exit({"error": "INVALID CHOICE"})

    count = 1
    for email in emails:

        # avoid sending too many requests - wait for 1 second after sending 15 emails
        if count % 15 == 0:
            time.sleep(1)

        sendEmail(email)
        print(f"{count} {'email' if count == 1 else 'emails'} sent\n\n")
        count += 1

    print("Any unsent emails can be found in unsent.csv")
    print("Thank you for using ieee-mailer !!")


if __name__ == "__main__":
    main()
