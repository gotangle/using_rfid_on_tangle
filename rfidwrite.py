#!/usr/bin/env python

import RPi.GPIO as GPIO
import sys
from mfrc522 import SimpleMFRC522
from time import sleep

#Select GPIO mode
GPIO.setmode(GPIO.BOARD)

#Set buzzer - pin 16 as output
buzzer=16 
GPIO.setup(buzzer,GPIO.OUT)

reader = SimpleMFRC522()

try:
    while True:
        text = input('Your Name: ')
        print("Now place your Tag to write")
        id, text = reader.write(text) 
        print("recorded")
        print(id)
        print(text)

        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.2) # Delay in seconds
        GPIO.output(buzzer,GPIO.LOW)
        sleep(0.2)
        break
        
finally:
     GPIO.cleanup()

