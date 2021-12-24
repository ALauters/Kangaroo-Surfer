import RPi.GPIO as GPIO
import time
import os
import sys
import wave
import getopt
import requests
import alsaaudio
import distutils
from distutils import util

import pprint


def play(device, f):
    print('%d channels, %d sampling rate\n' % (f.getnchannels(),
                                               f.getframerate()))

    # 8bit is unsigned in wav files
    if f.getsampwidth() == 1:
        format = alsaaudio.PCM_FORMAT_U8
    # Otherwise we assume signed data, little endian
    elif f.getsampwidth() == 2:
        format = alsaaudio.PCM_FORMAT_S16_LE
    elif f.getsampwidth() == 3:
        format = alsaaudio.PCM_FORMAT_S24_LE
    elif f.getsampwidth() == 4:
        format = alsaaudio.PCM_FORMAT_S32_LE
    else:
        raise ValueError('Unsupported format')

    periodsize = f.getframerate() // 8

    device = alsaaudio.PCM(channels=f.getnchannels(), rate=f.getframerate(), format=format, periodsize=periodsize,
                           device=device)

    data = f.readframes(periodsize)
    while data:
        # Read data from stdin
        device.write(data)
        data = f.readframes(periodsize)


def grabScores(url):
    pp = pprint.PrettyPrinter(indent=2)

    try:
        r = requests.get(url)
        data = r.json()
    except:
        return 0

    for event in data['events']:
       # replace with Iowa or something, this is case sensitive for now
       # I could make it lowercase it to be multi use
       if 'Army' in event['name'] and (event['competitions'][0]['status']['type']['completed'] == False):
           for competition in event['competitions']:
               for competitor in competition['competitors']:
                   # Iowa team id is 2294
                   if '349' in competitor['team']['id']:
                        #print competitor['score']
                        return int(competitor['score'])

    # if there is no game this week or not playing return 0
    return 0


def getGameId(url):
    try:
        r = requests.get(url)
        data = r.json()
    except:
        return 0

    for event in data['events']:
       # replace with IOWA
       # if 'Army' in event['name'] and not (bool(distutils.util.strtobool(event['competitions'][0]['status']['type']['completed']))):
       if 'Army' in event['name'] and not (event['competitions'][0]['status']['type']['completed']):

           #debug code
           print('event id is {}'.format(event['id']))
           ################
           return event['id']

    # If there is no game that matches it in the json file then return 0
    return 0



def checkGameCompleted(url, gameId):
    try:
        r = requests.get(url)
        data = r.json()
    except:
        # returning false because it failed to get the game and I want to retry faster
        return False


    for event in data['events']:
        if gameId in event['id']:
            # debug code
            #print('game completed? {}'.format(event['competitions'][0]['status']['type']['completed']))
            ##############

            gameCompleted = event['competitions'][0]['status']['type']['completed']
            return gameCompleted

    # if for saome reason it cant find a game I want it to return default true so it will skip over searching for things constantly
    return True


def main():
    # sets board up to use gpio numbers
    GPIO.setmode(GPIO.BCM)
    led = 26
    GPIO.setup(led, GPIO.OUT)

#    for i in range(1, 2):
#        GPIO.output(led, GPIO.HIGH)
#        time.sleep(5)
#        GPIO.output(led, GPIO.LOW)
#        time.sleep(5)

    device = 'default'
    # Open the music file (needs to be .wav format)
#    filename = os.path.join(os.getcwd(), 'BackInBlack.wav')
    filename = os.path.join(os.getcwd(), 'Tada.wav')

    # this is only for college football, no other sports are here
    url = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
    score = grabScores(url)
    newscore = 0
    gameCompleted = True

    while(True):

        gameId = getGameId(url)
        if gameId != 0:
            gameCompleted = checkGameCompleted(url, gameId)

        while not (gameCompleted):
            newScore = grabScores(url)

            if newScore > score:
                if(os.path.exists(filename)):
                    music_file = wave.open(filename, 'rb')

                print('newScore is {} the old score is'.format(newScore, score))
                play(device, music_file)
                score = newScore
                print('the new score for kent state is {}'.format(score))

                music_file.close()

            gameCompleted = checkGameCompleted(url, gameId)

            time.sleep(1)
        #end while(!gameCompleted)

        # if we cant find a game then we dont need to query every second
        time.sleep(300)
    # end wehile(True)

    # it never gets here but its nice to have
    GPIO.cleanup()


if __name__ == "__main__":
    main()
