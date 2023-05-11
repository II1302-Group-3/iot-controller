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
	import sensor_data
	import water_sensor

	from moisture import moisture_callback
	from light import light_init, light_callback, run_light_automation, toggle_lights

	from arduino_rst import arduino_rst_pin_init, restart_arduino, arduino_rst_pin_cleanup
	from plant_detector import plant_detector_init, detect_plant, plant_detector_cleanup

	# Starts all functions that only work on the Raspberry Pi
	def init_raspberry_functions():
		print(colored("Restarting Arduino...", attrs=["bold"]))
		arduino_rst_pin_init()
		restart_arduino()
		print(colored("Done!\n", "green", attrs=["bold"]))

		print(colored("Initializing I2C for Arduino...",attrs=["bold"]))
		i2c_arduino_init.i2c_arduino_init()
		print(colored("Done!\n", "green", attrs=["bold"]))

		print(colored("Initializing the light sensor...", attrs=["bold"]))
		light_init()
		print(colored("Done!\n", "green", attrs=["bold"]))

		print(colored("Initializing the plant detector...", attrs=["bold"]))
		plant_detector_init()
		print(colored("Done!\n", "green", attrs=["bold"]))

		print(colored("Initializing the water level sensor...",attrs=["bold"]))
		water_sensor.water_sensor_GPIO_init()
		print(colored("Done!\n", "green", attrs=["bold"]))

	# Cleans up all functions that only work on the Raspberry Pi
	def cleanup_raspberry_functions():
		restart_arduino()
		arduino_rst_pin_cleanup()
		water_sensor.arduino_water_sensor_cleanup()
		plant_detector_cleanup()
