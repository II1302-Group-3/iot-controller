import platform
import sys

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

if is_raspberry_pi:
	import i2c_arduino_init
	import arduino_rst

	import moisture
	import light

	import plant_detector

	import sensor_data
	import water_sensor

	# Starts all functions that only work on the Raspberry Pi
	def init_raspberry_functions():
		print(colored("Restarting Arduino...", attrs=["bold"]))
		arduino_rst.pin_init()
		arduino_rst.restart_arduino()
		print(colored("Done!\n", "green", attrs=["bold"]))

		print(colored("Initializing I2C for Arduino...",attrs=["bold"]))
		i2c_arduino_init.i2c_arduino_init()
		print(colored("Done!\n", "green", attrs=["bold"]))

		print(colored("Initializing the light sensor...", attrs=["bold"]))
		light.init()
		print(colored("Done!\n", "green", attrs=["bold"]))

		print(colored("Initializing the plant detector...", attrs=["bold"]))
		plant_detector.init()
		print(colored("Done!\n", "green", attrs=["bold"]))

		print(colored("Initializing the water level sensor...",attrs=["bold"]))
		water_sensor.GPIO_init()
		print(colored("Done!\n", "green", attrs=["bold"]))

	# Cleans up all functions that only work on the Raspberry Pi
	def cleanup_raspberry_functions():
		arduino_rst.restart_arduino()
		arduino_rst.pin_cleanup()
		water_sensor.cleanup()
		plant_detector.cleanup()
