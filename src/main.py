import firebase

import platform
import sys

from time import sleep
from smbus2 import SMBus

import serialnumber
login = serialnumber.get_serial_and_key()

import serial
if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyACM0',57600, timeout=1)
	ser.reset_input_buffer()

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
print(f"Serial number: '{login['serial']}'")
print("")

print("Authenticating with Firebase...\n")

def moisture_test(m):
	m = int(m/4)
	print(addr)
	print(m)
	bus.write_byte(addr,m)
	print("test")
	
callbacks = {
	"target_moisture": moisture_test,
	"target_light_level": lambda l: print(f"New target light level: {l}")
}
database = firebase.init_database(login, callbacks)

# Run callbacks on start
moisture_test(database.target_moisture)

print("\nDone!")

if is_raspberry_pi:
	addr = 0x8 # bus address
	bus = SMBus(1) # indicates /dev/i2c-1

try:
	while True:
		database.sync()
		sleep(1)
except KeyboardInterrupt:
	print("")
	print("Exiting...")

	database.stop()
	sys.exit(0)
