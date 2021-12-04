import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.OUT)



def main():
    print("Hello World")



if __name__ == "__main__":
    main()