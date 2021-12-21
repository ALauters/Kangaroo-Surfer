import RPi.GPIO as GPIO
import time
import os
import sys
import wave
import getopt
import requests
import alsaaudio

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


def grabScores():
    pp = pprint.PrettyPrinter(indent=2)

    url =  'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
    r = requests.get(url)

    data = r.json()

    for event in data['events']:
       if 'Kent State' in event['name'] and (event['competitions'][0]['status']['type']['completed'] == False):
           for competition in event['competitions']:
               for competitor in competition['competitors']:
                   if '2309' in competitor['team']['id']:
#                       pp.pprint(competitor['score'])
			return competitor['score'])

    #if there is no game this week or not playing return 0
    return 0



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
    if(os.path.exists(filename)):
        music_file = wave.open(filename, 'rb')

    score = grabScores()

    while(True):
        newScore = grabScores()

        if newScore > score:
            play(device, music_file)
            score = newscore
            print('the new score for kent state is {}'.format(score))

        time.sleep(1)
    #end while


    GPIO.cleanup()


if __name__ == "__main__":
    main()
