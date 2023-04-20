import firebase

import platform
import sys
import time

import serial
from smbus import SMBus
current_serial = serial.get_serial_number()

# TODO: Check if we are running on Raspberry Pi
system = f"{platform.uname().system} {platform.uname().release}"

print("Green Garden IoT Controller started")
print(f"Python: {sys.version_info.major}.{sys.version_info.minor}")
print(f"System: {system}")
print(f"Serial number: '{current_serial}'")
print("")

print("Authenticating with Firebase...")

# Firebase listens on background threads
db = firebase.init_database(
	current_serial,
	lambda l: print(f"Led state: {l}"),
	lambda m: print(f"New target moisture: {m}"),
	lambda l: print(f"New target light level: {l}")
)

print("Done!")

addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

try:
	while True:
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
