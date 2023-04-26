import firebase

import platform
import sys
import time

from smbus2 import SMBus

import serial
login = serial.get_serial_and_key()

system = f"{platform.uname().system} {platform.uname().release}"

try:
	# https://raspberrypi.stackexchange.com/questions/5100/detect-that-a-python-program-is-running-on-the-pi
	with open("/sys/firmware/devicetree/base/model", "r") as file:
		device_type = file.readline().strip()
		is_raspberry_pi = "Raspberry Pi" in device_type
except:
	device_type = "Computer"
	is_raspberry_pi = False


print("Green Garden IoT Controller started")
print(f"Python: {sys.version_info.major}.{sys.version_info.minor}")
print(f"System: {device_type} {system}")
print(f"Serial number: '{login}'")
print("")

print("Authenticating with Firebase...")

# Firebase listens on a background thread
database = firebase.init_database(login)

print("Done!")

if is_raspberry_pi:
	addr = 0x8 # bus address
	bus = SMBus(1) # indicates /dev/i2c-1

try:
	while True:
		if is_raspberry_pi:
			if database.test_led_on == 1:
				bus.write_byte(addr, 0x1) # switch it on
			elif database.test_led_on == 0:
				bus.write_byte(addr, 0x0) # switch it off

		time.sleep(1)
except KeyboardInterrupt:
	print("")
	print("Exiting...")

	database.stop()
	sys.exit(0)
