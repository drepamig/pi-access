#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

userAccess = [{"Username": "Test User", "Card_ID":657244891756, "Card_Key": "pimylifeup", "Access": True}]

reader = SimpleMFRC522()
GPIO.output(7, False)

try:

    while True:
        try:
            id, key = reader.read()
            

                print(f"I don't know you!: {id}, {key}")
        except:
            break
        
        # if input("Press any key to try again. Press Q to quit").upper() == "Q":
        #     break
except:
    pass
finally:
    GPIO.cleanup()