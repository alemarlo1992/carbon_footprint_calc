from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from model import *
import schedule 
from datetime import date, timedelta
import time
import logging





def phone_verification(phone):
    """Uses Twilio API to look up cell number, returns number as string"""
  
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    try:
        phone_number = client.lookups \
                             .phone_numbers(phone) \
                             .fetch(type=['carrier'])

        return phone_number.phone_number

    #checks Twilio exception responses if number not real
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        else:
            raise e


def send_text_recs():
    """Given message and phone number, send users a text using Twilio API."""

    logging.info("Printing inside the recs function")


    users = User.query.all()

    for user in users: 
        if user.phone: 
            msg = Weekly_Rec.query.filter_by(id=user.last_rec_sent).first()
            
            client = Client(account_sid, auth_token)
            message = client.messages \
                            .create(
                                    body=msg,
                                    from_=TWILIO_NUMBER,
                                    to=user.phone
                     )
            print(message.sid)

            user.last_rec_sent = int(user.last_rec_sent) + 1 


def runscheduler():
    schedule.every().monday.at('9:00').do(send_text_recs)
    logging.error("Send Text Recs Scheduled")
    while True:
        schedule.run_pending()
        time.sleep(1)



