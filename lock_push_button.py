import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# GPIO.output(18, 1)
# GPIO.output(25, 0)

while True:
    if GPIO.input(12) == GPIO.HIGH:
        # Solenoid 1
        GPIO.setup(18, GPIO.OUT)
        # Solenoid 2
        GPIO.setup(25, GPIO.OUT)

        # Turn off the relay and lock both solenoid door
        GPIO.output(18, 1)
        GPIO.output(25, 0)

        print("Button GPIO12 was pushed and both solenoids were locked!")
    # elif GPIO.input(16) == GPIO.HIGH:
    #     GPIO.output(25, 0)

    #     print("Button GPIO16 was pushed!")
