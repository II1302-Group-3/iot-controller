import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.IN)

if not(GPIO.input(21)):
  print('There is water\n')
  GPIO.output(20, True)
else:
  print('Not enough water, please refill\n')
	GPIO.output(20, False)

