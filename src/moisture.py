#import serial
#ser = serial.Serial('/dev/ttyACM0',57600, timeout=1)
#ser.reset_input_buffer()

from smbus2 import SMBus
from time import sleep
import i2c_arduino_init
#address = None # bus address
#bus = None


# Called when the moisture changes in Firebase
def moisture_callback(m):
	sleep(1)
	print(f"Sending moisture to Arduino: {m}")
	i2c_arduino_init.bus.write_word_data(i2c_arduino_init.address,0x00,m)
