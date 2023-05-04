import smbus2 as smbus
import time
import struct


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

	
	time.sleep(2);
	
		
		
