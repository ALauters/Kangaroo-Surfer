import RPi.GPIO as GPIO
import time

def main():
    # sets board up to use gpio numbers
    GPIO.setmode(GPIO.BCM)
    led = 26
    GPIO.setup(led, GPIO.OUT)

    for i in range(1,5):
        GPIO.setmode(led, GPIO.HIGH)
        time.sleep(5)
        GPIO.setmode(led, GPIO.LOW)
        time.sleep(5)

    GPIO.cleanup()


if __name__ == "__main__":
    main()