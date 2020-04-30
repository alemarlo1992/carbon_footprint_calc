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
    ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    TWILIO_NUMBER = '+12055286381'
  
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
    """Given message and phone number, send users a rec using Twilio API."""

    logging.info("Printing inside the recs function")
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    TWILIO_NUMBER = '+12055286381'

    users = User.query.all()

    for user in users: 
        if user.phone: 
            rec = Weekly_Rec.query.filter_by(id=user.last_rec_sent).first()
            msg = 'Hello ' + str(user.fname) +', here is your weekly recommendation: ' + str(rec)
            
            client = Client(account_sid, auth_token)
            message = client.messages \
                            .create(
                                    body=msg,
                                    from_=TWILIO_NUMBER,
                                    to=user.phone
                     )
            print(message.sid)

            user.last_rec_sent = user.last_rec_sent + 1 

            db.session.commit()


def run_scheduler():
    """Scheduling sed_text_recs to be sent every Monday at 9am"""
    schedule.every().monday.do(send_text_recs)
    logging.error("Send Text Recs Scheduled")
    while True:
        schedule.run_pending()
        time.sleep(1)


