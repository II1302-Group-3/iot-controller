import argparse
import pathlib
import random
import sys

from pwinput import pwinput
import requests

args_parser = argparse.ArgumentParser()
args_parser.add_argument("--new-serial", action="store_true")
args_parser.add_argument("--set-serial", type=str)

home_dir = pathlib.Path.home() / "green-garden"
serial_file = home_dir / "serial.txt"

if not home_dir.exists():
	home_dir.mkdir()

def register_new_serial_number(serial):
	password = pwinput()
	params = { "serial": serial, "password": password }
	key = requests.get("https://europe-west1-greengarden-iot.cloudfunctions.net/signSerialNumber", params=params).text

	if key == "missing_parameter": print("Missing parameter error")
	elif key == "wrong_password": print("Wrong password")
	else:
		with open(serial_file, "w") as file:
			file.write(f"{serial}\n")
			file.write(f"{key}\n")

		return { "serial": serial, "unique_key": key }

	sys.exit(1)

def get_login():
	args = args_parser.parse_args()

	if args.new_serial:
		new_serial = str(random.randint(0, 999999999999)).zfill(12)

		print(f"Generated new serial number: {new_serial}")
		print("")

		return register_new_serial_number(new_serial)
	elif args.set_serial != None:
		if not args.set_serial.isdigit() or int(args.set_serial) < 0 or int(args.set_serial) > 999999999999:
			print("Warning: Serial number should have 12 digits")
			print("")

		return register_new_serial_number(args.set_serial)
	else:
		if not serial_file.exists():
			print("Error: No serial number set for this garden")
			print("Generate a new serial with --new-serial or create a serial.txt file")
			sys.exit(1)

		with open(serial_file, "r") as file:
			return { "serial": file.readline().strip(), "unique_key": file.readline().strip() }
