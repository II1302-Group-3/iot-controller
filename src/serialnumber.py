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
token_file = home_dir / "token.txt"

if not home_dir.exists():
	home_dir.mkdir()

def register_new_serial_number(serial):
	params = { "serial": serial, "password": pwinput() }
	key = requests.get("https://europe-west1-greengarden-iot.cloudfunctions.net/signSerialNumber", params=params).text

	print("")

	if key == "missing_parameter": sys.exit("Missing parameter error")
	elif key == "wrong_password": sys.exit("Wrong password")
	else:
		with open(serial_file, "w") as file:
			file.write(f"{serial}\n")
			file.write(f"{key}\n")

		if token_file.exists():
			token_file.unlink()

		return { "serial": serial, "key": key }

def get_serial_and_key():
	args = args_parser.parse_args()

	if args.new_serial:
		new_serial = str(random.randint(0, 999999999999)).zfill(12)
		print(f"Generated new serial number: {new_serial}")

		return register_new_serial_number(new_serial)
	elif args.set_serial != None:
		args.set_serial = args.set_serial.strip()

		if not args.set_serial.isdigit() or int(args.set_serial) < 0 or int(args.set_serial) > 999999999999:
			print("Warning: Serial number should have 12 digits")

		return register_new_serial_number(args.set_serial)
	else:
		if not serial_file.exists(): sys.exit("No serial number set for this garden (use --new-serial or --set-serial)")

		with open(serial_file, "r") as file:
			return { "serial": file.readline().strip(), "key": file.readline().strip() }
