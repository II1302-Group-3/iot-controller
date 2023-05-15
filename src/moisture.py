from smbus2 import SMBus
from time import sleep

import i2c_arduino_init
import plant_detector

previous_target_moisture = 0

def update(database):
	global previous_target_moisture

	target_moisture = database.target_moisture * 10
	if not plant_detector.detected_plant:
		target_moisture = 0

	if target_moisture != previous_target_moisture:
		sleep(1)
		print(f"Sending moisture to Arduino: {target_moisture}")
		i2c_arduino_init.bus.write_word_data(i2c_arduino_init.address,0x00,target_moisture)
		previous_target_moisture = target_moisture
