import smbus2 as smbus
import time
import struct


#*************************************
#Data over i2c is always sent 6bytes
# at a time from the arduino
# first 2 is temp
# next 2 is humidity
# last 2 is moisture
#
#*************************************


bus = smbus.SMBus(1)

address = 0x8

data = bytearray()
for i in range(0,6):
	data.append(bus.read_byte(address));
		
temp_b1 = int(data.pop(0))
temp_b0 = int(data.pop(0))
humidity_b1	= int(data.pop(0))
humidity_b0 = int(data.pop(0))
moisture_b1	= int(data.pop(0))
moisture_b0 = int(data.pop(0))
	
temp = temp_b0 + temp_b1*256
humidity = humidity_b0 + humidity_b1 *256
moisture = moisture_b0 + moisture_b1 *256

	
#time.sleep(2);
	
		
		
