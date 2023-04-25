import firebase

import platform
import sys
import time

import serial
login = serial.get_login()

# TODO: Check if we are running on Raspberry Pi
system = f"{platform.uname().system} {platform.uname().release}"
try:
	# https://raspberrypi.stackexchange.com/questions/5100/detect-that-a-python-program-is-running-on-the-pi
	with open("/sys/firmware/devicetree/base/model", "r") as file:
		device_type = file.readline().strip()
		is_raspberry_pi = "Raspberry Pi" in device_type
except:
	device_type = "Computer"
	is_raspberry_pi = False

if is_raspberry_pi:
	from smbus2 import SMBus

print("Green Garden IoT Controller started")
print(f"Python: {sys.version_info.major}.{sys.version_info.minor}")
print(f"System: {device_type} {system}")
print(f"Serial number: '{login}'")
print("")

print("Authenticating with Firebase...")

# Firebase listens on a background thread
db = firebase.init_database(
	login,
	lambda l: print(f"Led state: {l}"),
	lambda m: print(f"New target moisture: {m}"),
	lambda l: print(f"New target light level: {l}")
)

print("Done!")

if is_raspberry_pi:
	addr = 0x8 # bus address
	bus = SMBus(1) # indicates /dev/ic2-1

try:
	while True:
		if is_raspberry_pi:
			if db.led_on == 1:
				bus.write_byte(addr, 0x1) # switch it on
			elif db.led_on == 0:
				bus.write_byte(addr, 0x0) # switch it off

		time.sleep(1)
except KeyboardInterrupt:
	print("")
	print("Exiting...")

	db.stop()
	sys.exit(0)
