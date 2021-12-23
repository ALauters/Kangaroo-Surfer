import RPi.GPIO as GPIO
import time
import os
import sys
import wave
import getopt
import requests
import alsaaudio
import pprint


pp = pprint.PrettyPrinter(indent=2)

url = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'

r = requests.get(url)

data = r.json()

for event in data['events']:
   # replace with IOWA
   if 'Army' in event['name'] and (event['competitions'][0]['status']['type']['completed'] == False):
       for competition in event['competitions']:
           for competitor in competition['competitors']:
               # Iowa team id is 2294
               pp.pprint(competitor['team']['id'])
               if '349' in competitor['team']['id']:
                    #print competitor['score']
                    #return int(competitor['score'])
                    print('found the team {}'.format(competitor['team']['name']))

# if there is no game this week or not playing return 0

