import firebase

import platform
import sys

from time import sleep
from termcolor import colored

system = f"{platform.uname().system} {platform.uname().release}"
python_version = f"{sys.version_info.major}.{sys.version_info.minor}"

try:
	# https://raspberrypi.stackexchange.com/questions/5100/detect-that-a-python-program-is-running-on-the-pi
	with open("/sys/firmware/devicetree/base/model", "r") as file:
		device_type = file.readline().strip()
		is_raspberry_pi = "Raspberry Pi" in device_type
except:
	device_type = "Computer"
	is_raspberry_pi = False

import authentication
login = authentication.get_serial_and_key()

print(colored("Green Garden IoT Controller started", attrs=["bold"]))
print(f"Python: {python_version}")
print(f"System: {device_type} {system}")
print(f"Serial number: '{login['serial']}'")
print("")

if python_version != "3.9":
	print(colored(f"Warning: The Raspberry Pi uses Python 3.9 and you have {python_version}", "red", attrs=["bold"]))
	print("")

print("Authenticating with Firebase...")
print("")

callbacks = {}

if is_raspberry_pi:
	from moisture import moisture_callback
	from light import light_callback

	callbacks = {
		"target_moisture": moisture_callback,
		"target_light_level": light_callback
	}

database = firebase.init_database(login, callbacks or {})

print(colored("\nDone!", "green"))

try:
	while True:
		database.sync()
		sleep(1)
except KeyboardInterrupt:
	print("")
	print("Exiting...")

	database.stop()
	sys.exit(0)
