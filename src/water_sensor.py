import RPi.GPIO as GPIO
from time import sleep
from smbus2 import SMBus



addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/i2c-1


def water_sensor_GPIO_init():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(21, GPIO.IN)
	

def water_sensor_callback():
	#previos_state = current_state
	sleep(1)
	if not(GPIO.input(21)):
		# There is water
		bus.write_word_data(addr,0x00, 2500)
		time.sleep(3)
	else:
 		# Not enough water, please refill
		bus.write_word_data(addr,0x00, 1500)	
		time.sleep(3)
	