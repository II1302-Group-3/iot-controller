import sys

from signal import signal, SIGINT
from termcolor import colored
from time import sleep

import requests
from requests.adapters import TimeoutSauce

# https://stackoverflow.com/questions/17782142/why-doesnt-requests-get-return-what-is-the-default-timeout-that-requests-get
# Set a timeout for all requests, this needs to be done at the start
class GlobalTimeout(TimeoutSauce):
	def __init__(self, *args, **kwargs):
		if kwargs["connect"] is None:
			kwargs["connect"] = 5

		# The timeout needs to be high because otherwise stream_thread will lose connection
		if kwargs["read"] is None:
			kwargs["read"] = 45

		super(GlobalTimeout, self).__init__(*args, **kwargs)

requests.adapters.TimeoutSauce = GlobalTimeout

import authentication
login = authentication.get_serial_and_key()

from pi import *

print(colored("Green Garden IoT Controller started", attrs=["bold"]))
print(colored("Python:", attrs=["bold"]), python_version)
print(colored("System:", attrs=["bold"]), device_type, system)
print(colored("Serial number:", attrs=["bold"]), login["serial"])
print("")

if python_version != "3.9":
	print(colored(f"Warning: The Raspberry Pi uses Python 3.9 and you have {python_version}", "red"))
	print("")

if is_raspberry_pi:
	init_raspberry_functions()

print(colored("Initializing Firebase...", attrs=["bold"]))

callbacks = {
	"target_moisture": moisture_callback,
	"target_light_level": light_callback
} if is_raspberry_pi else {}

from firebase import FirebaseDatabase
database = FirebaseDatabase(login, callbacks)

print(colored("Done!\n", "green", attrs=["bold"]))

def stop(*_):
	# Empty function
	signal(SIGINT, lambda *_: {})

	print("\n")
	print(colored("Exiting...", attrs=["bold"]))

	database.stop()

	if is_raspberry_pi:
		cleanup_raspberry_functions()

	sys.exit(0)

signal(SIGINT, stop)

while True:
	if is_raspberry_pi:
		detect_plant()
		run_light_automation()

	sleep(1)
