import sys


from termcolor import colored
from time import sleep

import authentication
login = authentication.get_serial_and_key()

from pi import *

print(colored("Green Garden IoT Controller started", attrs=["bold"]))
print(f"Python: {python_version}")
print(f"System: {device_type} {system}")
print(f"Serial number: {login['serial']}")
print("")

if python_version != "3.9":
	print(colored(f"Warning: The Raspberry Pi uses Python 3.9 and you have {python_version}", "red", attrs=["bold"]))
	print("")

if is_raspberry_pi:
	init_raspberry_functions()

print(colored("Initializing Firebase...", attrs=["bold"]))

callbacks = {
	"target_moisture": moisture_callback,
	"target_light_level": light_callback
} if is_raspberry_pi else {}

from firebase import init_database
database = init_database(login, callbacks)

print(colored("Done!\n", "green", attrs=["bold"]))

try:
	while True:
		if is_raspberry_pi:
			if one_shot == 0:
				detect_plant()
				run_light_automation()
				water_sensor.set_water_sensor_arduino()
				sensor_data.request_sensor_data()
				one_shot = 1
				#print("WATER LEVEL")
				#print(water_sensor.water_level)
				#print("SGJKLÖSGGJK")
			else:
				if one_shot == 1:
					light.turn_lights_off()
					arduino_rst.restart_arduino()
					one_shot = 0
		

		database.sync()
		sleep(1)
except KeyboardInterrupt:
	print("\n")
	print("Exiting...")

	if is_raspberry_pi:
		cleanup_raspberry_functions()

	database.stop()
	sys.exit(0)
