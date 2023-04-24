import smbus
import time
import random

VEML_ADDRESS = 0x10
ARDUINO_ADDRESS = 0x0C

# Create an instance of the I2C bus
bus = smbus.SMBus(1)

while True:
    
    #light_data = bus.read_byte(VEML_ADDRESS)

    moisture_data = bus.read_byte(ARDUINO_ADDRESS)
    print(moisture_data)

    # Wait for some time before reading data again
    time.sleep(1)
