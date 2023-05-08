import time
import board
import os 
import busio
import adafruit_veml7700

i2c = busio.I2C(board.SCL, board.SDA)
veml7700 = adafruit_veml7700.VEML7700(i2c)

#turn_usb_off = "echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind"
#turn_usb_on = "echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind"

turn_usb_off = "echo 0 | sudo tee /sys/devices/platform/soc/20980000.usb/buspower >/dev/null"
turn_usb_on = "echo 1 | sudo tee /sys/devices/platform/soc/20980000.usb/buspower >/dev/null"

threshold = 200

one_time = 0

while True:

        light_level = veml7700.light

        print(light_level)
        if threshold < light_level:
                if one_time == 0:
                        os.system(turn_usb_off)
                        print("off")
                        one_time = 1
        else:
                if one_time == 1:
                        os.system(turn_usb_on)
                        print("on")
                        one_time = 0

        time.sleep(1)
