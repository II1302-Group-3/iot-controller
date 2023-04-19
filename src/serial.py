import argparse
import pathlib
import random
import sys

args_parser = argparse.ArgumentParser()
args_parser.add_argument("--new-serial", action="store_true")
args_parser.add_argument("--set-serial", type=str)

def get_serial_number():
	home_dir = pathlib.Path.home() / "green-garden"
	serial_file = home_dir / "serial.txt"

	if not home_dir.exists():
		home_dir.mkdir()

	args = args_parser.parse_args()

	if args.new_serial:
		new_serial = str(random.randint(100000000000, 999999999999))

		with open(serial_file, "w") as file:
			file.write(new_serial)

		print(f"Generated new serial number: {new_serial}")
		print("")

		return new_serial
	elif args.set_serial != None:
		if not args.set_serial.isdigit() or int(args.set_serial) < 100000000000 or int(args.set_serial) > 999999999999:
			print("Warning: Serial number should have 12 digits")
			print("")

		with open(serial_file, "w") as file:
			file.write(args.set_serial)

		return args.set_serial
	else:
		if not serial_file.exists():
			print("Error: No serial number set for this garden")
			print("Generate a new serial with --new-serial or create a serial.txt file")
			sys.exit(1)

		with open(serial_file, "r") as file:
			return file.readline().strip()
