import os
from time import sleep

def arduino_rst_pin_init():
	os.system("sudo echo '17' > /sys/class/gpio/export") # Open gpio 17
	sleep(0.3)
	os.system("sudo echo 'out' > /sys/class/gpio/gpio17/direction") # Setting gpio 17 as out

def restart_arduino():
	os.system("sudo echo '0' > /sys/class/gpio/gpio17/value") # Setting gpio17 to 0
	sleep(0.3)
	os.system("sudo echo '1' > /sys/class/gpio/gpio17/value") # Setting gpio17 to 1
	sleep(2)

def arduino_rst_pin_cleanup():
	os.system("sudo echo 17 >/sys/class/gpio/unexport")
