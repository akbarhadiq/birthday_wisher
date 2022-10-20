import smtplib
import pandas
import random
from dotenv import load_dotenv
import os
import datetime as dt

# Load .Environment Variable ----------------  # create your own .env file with your own credentials
load_dotenv()
my_email = os.getenv("MY_EMAIL")
smtp = os.getenv("SMTP")
password = os.getenv("PASSWORD")
port = int(os.getenv("PORT"))
# ------------------------------------------


# Get today's date
current_date = dt.datetime.now()
current_day = current_date.day
current_month = current_date.month


# Birthday Text Writer
def writer(name):
    # randomly chose a letter from the three letters available
    chosen_letter = random.choice(letter)

    # open the birthday wish text and turn it into a variable
    with open(f'letter_templates/{chosen_letter}', mode="r") as file:
        text = file.readlines()
        # print(text)

    # remove the text /n space
    bday_wish_text = ''.join(text)
    # replace default [NAME] with your friends name in the csv u wrote automatically
    bday_wish_text_with_name = bday_wish_text.replace('[NAME]', name)
    print(bday_wish_text_with_name)
    return bday_wish_text_with_name


letter = ["letter_1.txt", "letter_2.txt", "letter_3.txt"] # open these .txt file and change [YOUR NAME] to your name
# your friends name is written automatically from the csv file though. don't bother with that. just write your friends name in the csv.
df = pandas.read_csv("birthdays.csv")  # write your friends birthdays date and name in this file
birthdays_data = pandas.DataFrame.to_dict(df, orient="records")  # remember orient records!!!!

print(birthdays_data)
# print(type(birthdays_data[0]["email"]))


# checks today date (day, month) with birthday_data
for birthday in birthdays_data:
    if birthday["day"] == current_day and birthday["month"] == current_month:

        # get the birthday text
        birthday_text = writer(birthday['name'])

        # send those wishes
        connection = smtplib.SMTP(smtp, port)
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=birthday['email'],
            msg=f"Subject:Happy Birthday!\n\n{birthday_text}"
        )
        connection.close()
