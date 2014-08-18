#!/usr/bin/python
import RPi.GPIO as GPIO
import time

### Change it ###
LIGHT_RPI_PIN = 11  # RPI pinout #11 equals to GPIO#17
INTERVAL = 1  # 1 second.


### Setup GPIO-0(aka:pin LIGHT_RPI_PIN)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LIGHT_RPI_PIN, GPIO.OUT)

### looping
while True:
 GPIO.output(LIGHT_RPI_PIN, GPIO.HIGH)
 time.sleep(INTERVAL)
 GPIO.output(LIGHT_RPI_PIN, GPIO.LOW)
 time.sleep(INTERVAL)
