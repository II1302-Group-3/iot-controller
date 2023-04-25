import time
import os

# Set the threshold value
threshold = 50

turn_usb_off = "echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind"
turn_usb_on = "echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind"


while True:
        
    sensor_value = 70

    if sensor_value > threshold:
        # Turn on the LED strips
        os.system(turn_usb_on)
    else:
        # Turn off the LED strips
        os.system(turn_usb_off)

    
    time.sleep(1)

    sensor_value = 30

    if sensor_value > threshold:
        # Turn on the LED strips
        os.system(turn_usb_on)
    else:
        # Turn off the LED strips
        os.system(turn_usb_off)
    time.sleep(1)
    
