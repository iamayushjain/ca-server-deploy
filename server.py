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
CLIENT = 'jenny'
client_rest = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

app = Flask(__name__)
@app.route('/token')
def token():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  auth_token = os.environ.get("AUTH_TOKEN", AUTH_TOKEN)
  app_sid = os.environ.get("APP_SID", APP_SID)

  capability = TwilioCapability(account_sid, auth_token)

  # This allows outgoing connections to TwiML application
  if request.values.get('allowOutgoing') != 'false':
     capability.allow_client_outgoing(app_sid)

  # This allows incoming connections to client (if specified)
  client = request.values.get('client')
  if client != None:
    capability.allow_client_incoming(client)

  # This returns a token to use with Twilio based on the account and capabilities defined above
  return capability.generate()

@app.route('/call', methods=['GET', 'POST'])
def call():
  """ This method routes calls from/to client                  """
  """ Rules: 1. From can be either client:name or PSTN number  """
  """        2. To value specifies target. When call is coming """
  """           from PSTN, To value is ignored and call is     """
  """           routed to client named CLIENT                  """
  resp = twilio.twiml.Response()
  from_value = request.values.get('From')
  to = request.values.get('To')
  if not (from_value and to):
    resp.say("Invalid request")
    return str(resp)
  from_client = from_value.startswith('client')
  caller_id = os.environ.get("CALLER_ID", CALLER_ID)
  if not from_client:
    # PSTN -> client
    resp.dial(callerId=from_value).client(CLIENT)
  elif to.startswith("client:"):
    # client -> client
    resp.dial(callerId=from_value).client(to[7:])
  elif to.startswith("conference:"):
    #if from_value.startswith("client:teacher"):
      resp.dial(callerId=from_value).conference('MyConference')#,startConferenceOnEnter="true")
    # else:
    #   resp.dial(callerId=from_value).conference('MyConference')#,startConferenceOnEnter="true")
    #resp.dial(callerId=from_value).conference('MyConference').
    #participants = client_rest.participants('CFbbe46ff1274e283f7e3ac1df0072ab39').list()
    # conferences = client_rest.conferences.list()
    # for conference in conferences:
    #   #return str(conference.sid)
    #   welcome()
  else:
    # client -> PSTN
     resp.dial(to, callerId=caller_id)
    
  return str(resp)


@app.route('/', methods=['GET', 'POST'])
def welcome():
  resp = twilio.twiml.Response()
  resp.say("Welcome to Culture Alley Hello English")
  return str(resp)

@app.route('/confercall', methods=['GET', 'POST'])
def confercall():
    partiid = '~'
    conferences = client_rest.conferences.list()
    for conference in conferences:
      participants = client_rest.participants(conference.sid).list()
      len(participants)
      for participant in participants :
           partiid+=(participant.call_sid)
           partiid+='~'
      return partiid
        # return participant.sid
    resp = twilio.twiml.Response()
    resp.say("NO of conference")
    return str(resp)

@app.route('/operation', methods=['GET', 'POST'])
def operation():
  """ This method routes calls from/to client                  """
  """ Rules: 1. From can be either client:name or PSTN number  """
  """        2. To value specifies target. When call is coming """
  """           from PSTN, To value is ignored and call is     """
  """           routed to client named CLIENT                  """
  resp = twilio.twiml.Response()
  partid = request.values.get('partid')
  task = request.values.get('task')
  if not (partid and task):
    resp.say("Invalid request")
    return str(resp)
  mutech = task.startswith('mute')
  confersid = "CF123"
  conferences = client_rest.conferences.list()
  for conference in conferences:
    confersid = conference.sid
    
  if mutech:
    #task for mute person
    participant = client_rest.participants(confersid).update(partid, muted="True")
    resp.say("Mute")
    return str(resp)
  elif task.startswith('delete'):
    #task for delete person
    participant = client_rest.participants(confersid).delete(partid)
    resp.say("Delete")
    return str(resp)
  else:
    #task for unmute person
    participant = client_rest.participants(confersid).update(partid, muted="False")
    resp.say("unmute")
    return str(resp)
    
  return str(resp)
# @app.route('/caller', methods=['GET','POST']) #'GET'
# def caller():
#   participants = client_rest.participants('MyConference').list()
#   retrun str('len(participants)')
  
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)

