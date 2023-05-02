import firebase

import platform
import sys
import os

from time import sleep
import light
import arduino_rst
import plant_detector

#Making sure Arduino is in initial state
arduino_rst.arduino_rst_pin_init()
arduino_rst.restart_arduino()
sleep(2)

plant_detector.plant_detector_init()
sleep(2)

system = f"{platform.uname().system} {platform.uname().release}"

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

print("Green Garden IoT Controller started")
print(f"Python: {sys.version_info.major}.{sys.version_info.minor}")
print(f"System: {device_type} {system}")
print(f"Serial number: '{login['serial']}'")
print("")

print("Authenticating with Firebase...\n")

callbacks = {}

if is_raspberry_pi:
	from moisture import moisture_callback
	from light import light_callback

	callbacks = {
		"target_moisture": moisture_callback,
		"target_light_level": light_callback
	}

database = firebase.init_database(login, callbacks or {})

print("\n Init done!")

try:

	one_shot = 0

	while True:
		detect_plant = plant_detector.check_for_plant()
		print("Plant detector: ", detect_plant)
		sleep(0.1)
		if not(detect_plant):
			if one_shot == 0:
				moisture_callback(database.target_moisture)
				light_callback(database.target_light_level)
			database.sync()
			light.run_light_automation()
			one_shot = 1
		else:
			if one_shot == 1:
				light.turn_lights_off()
				arduino_rst.restart_arduino()
				one_shot = 0
		sleep(1)

except KeyboardInterrupt:

	arduino_rst.restart_arduino()
	arduino_rst.arduino_rst_pin_cleanup()

	plant_detector.plant_detector_cleanup()


	print("\n")
	print("Exiting...")

	database.stop()
	sys.exit(0)
