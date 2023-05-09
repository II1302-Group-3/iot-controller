import time
import os
import busio
import adafruit_veml7700
import threading

from time import sleep

I2C_SDA_PIN = 2
I2C_SCL_PIN = 3

light_threshold = 0

i2c = None
veml7700 = None

turn_usb_off = "echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind"
turn_usb_on = "echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind"

one_time = 1 # To make sure that usb is only turned off/on once

def light_init():
	global i2c, veml7700

	i2c = busio.I2C(I2C_SCL_PIN, I2C_SDA_PIN)
	veml7700 = adafruit_veml7700.VEML7700(i2c)

	sleep(1)

def light_callback(light_thres):
	print(f"New target light level: {light_thres}")
	global light_threshold
	light_threshold = light_thres

def run_light_automation():
	global one_time

	light_level = veml7700.light # Measure the light
	print("Light value: ",light_level)

	if light_threshold < light_level:
		if one_time == 0:
			os.system(turn_usb_off)
			print("Lights off")
			one_time = 1
	else:
		if one_time == 1:
			os.system(turn_usb_on)
			print("Lights on")
			one_time = 0

def toggle_lights(on):
	os.system(turn_usb_on if on else turn_usb_off)
