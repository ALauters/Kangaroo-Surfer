import RPi.GPIO as GPIO
import time
import os
import sys
import wave
import getopt
import alsaaudio


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


def main():
    # sets board up to use gpio numbers
    GPIO.setmode(GPIO.BCM)
    led = 26
    GPIO.setup(led, GPIO.OUT)

    for i in range(1, 2):
        GPIO.output(led, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(led, GPIO.LOW)
        time.sleep(5)

    device = 'default'
    # Open the music file (needs to be .wav format)
    filename = os.path.join(os.getcwd(), 'BackInBlack.wav')
    print(filename)

    if(os.path.exists(filename)):
        music_file = wave.open(filename, 'rb')

        play(device, music_file)


    GPIO.cleanup()


if __name__ == "__main__":
    main()

