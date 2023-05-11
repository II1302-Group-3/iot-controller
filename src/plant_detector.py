import os
from time import sleep

import arduino_rst

detected_plant = 0
one_shot = 0

def init():
	os.system("sudo echo '27' > /sys/class/gpio/export") # Open gpio 17
	sleep(0.3)
	os.system("sudo echo 'in' > /sys/class/gpio/gpio27/direction") # Setting gpio 17 as out
	sleep(2)

def detect_plant():
	global one_shot, detected_plant

	detected_plant = check_for_plant()
	print("Plant detector: ", detected_plant)
	sleep(0.1)

	if detected_plant:
		one_shot = 1
	else:
		if one_shot == 1:
			arduino_rst.restart_arduino()
			one_shot = 0

def check_for_plant():
	# This closes the file after reading is done
	with os.popen("sudo cat /sys/class/gpio/gpio27/value") as gpio:
		# Revert so 0 = not detected, 1 = detected
		return 0 if int(gpio.read()) == 1 else 1 # Setting gpio17 to 0

def cleanup():
	os.system("sudo echo 27 >/sys/class/gpio/unexport")
