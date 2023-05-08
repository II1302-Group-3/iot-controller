import os
from time import sleep
from arduino_rst import restart_arduino

one_shot = 0

def plant_detector_init():
	os.system("sudo echo '27' > /sys/class/gpio/export") # Open gpio 17
	sleep(0.3)
	os.system("sudo echo 'in' > /sys/class/gpio/gpio27/direction") # Setting gpio 17 as out
	sleep(2)

def detect_plant():
	global one_shot

	detected_plant = check_for_plant()
	print("Plant detector: ", detected_plant)
	sleep(0.1)

	if not(detected_plant):
		one_shot = 1
	else:
		if one_shot == 1:
			toggle_lights(False)
			restart_arduino()
			one_shot = 0

def check_for_plant():
	# This closes the file after reading is done
	with os.popen("sudo cat /sys/class/gpio/gpio27/value") as gpio:
		return int(gpio.read()) # Setting gpio17 to 0

def plant_detector_cleanup():
	os.system("sudo echo 27 >/sys/class/gpio/unexport")
