import RPi.GPIO as GPIO
from time import sleep
from smbus2 import SMBus
import i2c_arduino_init




#addr = None # bus address
#bus = None # indicates /dev/i2c-1
previous_state = None
water_level = None


def water_sensor_GPIO_init():
	#addr = 0x8 # bus address
	#bus = SMBus(1) # indicates /dev/i2c-1
	previous_state = None
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(21, GPIO.IN)
	

def set_water_sensor_arduino():
	global previous_state  # Use the global variable for previous state
	global water_level # save value for sending to firebase
	sleep(1)
	current_state = GPIO.input(21)

	if current_state != previous_state:
	# State has changed
		if not current_state:
			# There is water
			i2c_arduino_init.bus.write_word_data(i2c_arduino_init.address, 0x00, 2500)
			print("water level HIGH") # value 0
			water_level = 0
		else:
			# Not enough water, please refill
			i2c_arduino_init.bus.write_word_data(i2c_arduino_init.address, 0x00, 1500)
			print("water level LOW") #value 1
			water_level = 1
			
	sleep(2)

	previous_state = current_state
	
def arduino_water_sensor_cleanup():
	os.system("sudo echo 21 >/sys/class/gpio/unexport")
	
	
	
	
	
