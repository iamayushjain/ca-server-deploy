import os
from flask import Flask, request
from twilio.util import TwilioCapability
from twilio.rest import TwilioRestClient

import twilio.twiml

# Account Sid and Auth Token can be found in your account dashboard
ACCOUNT_SID = 'ACf3af4b1e02c1c848980b6d0a8047c122'
AUTH_TOKEN = 'f7347d136ab3732577852747ddb352b3'

# TwiML app outgoing connections will use
APP_SID = 'AP89a16704d7600569f8aca23517f03d33'

CALLER_ID = '+9199308 42095'

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

conference = client.conferences.get("CFbbe46ff1274e283f7e3ac1df0072ab39")
print(conference.status)