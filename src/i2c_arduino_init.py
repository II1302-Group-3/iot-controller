import smbus2 as smbus
bus = None
address = None
def i2c_arduino_init():
	global bus
	global address
	bus = smbus.SMBus(1)
	address = 0x8