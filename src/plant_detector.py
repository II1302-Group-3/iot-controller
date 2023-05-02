import os
from time import sleep

def plant_detector_init():
    os.system("sudo echo '27' > /sys/class/gpio/export") # Open gpio 17
    sleep(0.3)
    os.system("sudo echo 'in' > /sys/class/gpio/gpio27/direction") # Setting gpio 17 as out

def check_for_plant():
    return int(os.popen("sudo cat /sys/class/gpio/gpio27/value").read()) # Setting gpio17 to 0


def plant_detector_cleanup():
    os.system("sudo echo 27 >/sys/class/gpio/unexport")