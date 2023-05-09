import smbus2 as smbus
import time
import struct
import i2c_arduino_init

#*************************************
#Data over i2c is always sent 6bytes
# at a time from the arduino
# first 2 is temp
# next 2 is humidity
# last 2 is moisture
#
#*************************************


temp = None
humidity = None
moisture = None


def request_sensor_data():
	global temp, humidity, moisture
	
	data = bytearray()
	for i in range(0,6):
		data.append(i2c_arduino_init.bus.read_byte(i2c_arduino_init.address));
            
	temp_b1 = int(data.pop(0))
	temp_b0 = int(data.pop(0))
	humidity_b1	= int(data.pop(0))
	humidity_b0 = int(data.pop(0))
	moisture_b1	= int(data.pop(0))
	moisture_b0 = int(data.pop(0))
	temp = temp_b0 + temp_b1*256
	humidity = humidity_b0 + humidity_b1 *256
	moisture = (moisture_b0 + moisture_b1 *256)/10 #normalise to 0-100
	

	
#time.sleep(2);
	
		
		
