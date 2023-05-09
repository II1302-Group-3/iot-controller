import RPi.GPIO as GPIO
from time import sleep
from smbus2 import SMBus



addr = None # bus address
bus = None # indicates /dev/i2c-1
previos_state = None


def water_sensor_GPIO_init():
	addr = 0x8 # bus address
	bus = SMBus(1) # indicates /dev/i2c-1
	previos_state = None
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(21, GPIO.IN)
	

def set_water_sensor_arduino():
	sleep(1)
	global previous_state  # Use the global variable for previous state
    sleep(1)
    current_state = GPIO.input(21)

    if current_state != previous_state:
        # State has changed
        if not current_state:
            # There is water
            bus.write_word_data(addr, 0x00, 2500)
        else:
            # Not enough water, please refill
            bus.write_word_data(addr, 0x00, 1500)
        time.sleep(3)

    previous_state = current_state
	
def arduino_water_sensor_cleanup():
	os.system("sudo echo 21 >/sys/class/gpio/unexport")
	
	
	
	
	