from smbus2 import SMBus
from time import sleep
import i2c_arduino_init

# Called when the moisture changes in Firebase
def callback(m):
	sleep(1)
	print(f"Sending moisture to Arduino: {m}")
	i2c_arduino_init.bus.write_word_data(i2c_arduino_init.address,0x00,m)
