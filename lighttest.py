import RPi.GPIO as GPIO
import time

# sets board up to use gpio numbers
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)

for i in range(1, 2):
    GPIO.output(led, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(led, GPIO.LOW)
    time.sleep(5)


GPIO.cleanup()
