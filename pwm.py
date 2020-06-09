import os
import glob
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

p= GPIO.PWM(18,50)
p.start(0)
time.sleep(1)
p.ChangeDutyCycle(50)
time.sleep(1)
p.ChangeDutyCycle(75)
time.sleep(1)
p.ChangeDutyCycle(100)
time.sleep(1)
p.stop()

GPIO.cleanup()
