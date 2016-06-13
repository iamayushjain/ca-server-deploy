from twilio.rest import TwilioRestClient

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "ACf3af4b1e02c1c848980b6d0a8047c122"
auth_token  = "f7347d136ab3732577852747ddb352b3"
client = TwilioRestClient(account_sid, auth_token)

conference = client.conferences.get("CFbbe46ff1274e283f7e3ac1df0072ab39")
print(conference.status)