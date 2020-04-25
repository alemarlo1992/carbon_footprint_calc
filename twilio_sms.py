from twilio.rest import Client
import os
import flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import schedule
from datetime import date, timedelta
import time
from server import app
from model import *

def 