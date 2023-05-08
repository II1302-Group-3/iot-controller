
import time

import serial
from smbus2 import SMBus

#Removed USB
#if __name__ == '__main__':
#	ser = serial.Serial('/dev/ttyACM0',57600, timeout=1)
#	ser.reset_input_buffer()

# TODO: Check if we are running on Raspberry Pi

print("Test started")



addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

print("Enter moisture threshold value")
try:
	while True:
		moisture_threshold = int(input(">>>>  "))
		bus.write_word_data(addr,0x00, moisture_threshold)
		time.sleep(3)
except KeyboardInterrupt:
	print("")
	print("Exiting...")

