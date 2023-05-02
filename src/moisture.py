#import serial
#ser = serial.Serial('/dev/ttyACM0',57600, timeout=1)
#ser.reset_input_buffer()

from smbus2 import SMBus

addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/i2c-1

# Called when the moisture changes in Firebase
def moisture_callback(m):
	m = int(m/4)
	print(f"Sending moisture to Arduino: {m}")
	bus.write_byte(addr,m)
