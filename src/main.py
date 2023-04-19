import firebase

import platform
import sys
import time

import serial
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
	lambda m: print(f"New target moisture: {m}"),
	lambda l: print(f"New target light level: {l}")
)

print("Done!")

try:
	while True:
		# Do useful stuff here
		time.sleep(1)
except KeyboardInterrupt:
	print("")
	print("Exiting...")

	db.stop()
	sys.exit(0)
