import requests
import json
from django.conf import settings
auth_token = '5114b04a6a67e26d-47b8019b92f46735-b130ed77ec40cc8f' 
hook = 'https://chatapi.viber.com/pa/set_webhook'
headers = {'X-Viber-Auth-Token': auth_token}


sen = dict(url='https://3595-188-163-102-40.ngrok-free.app/viber/',
           event_types = ['unsubscribed', 'conversation_started', 'message', 'seen', 'delivered', 'subscribed'])

r = requests.post(hook, json.dumps(sen), headers=headers)
print(r.json())