
import pathlib
import requests
import sys

from pyrebase4 import initialize_app

# https://stackoverflow.com/questions/67631/how-can-i-import-a-module-dynamically-given-the-full-path
from importlib.machinery import SourceFileLoader

config_file = pathlib.Path.home() / "green-garden" / "config.py"
config_module = SourceFileLoader("config", str(config_file)).load_module()

class FirebaseDatabase:
	def __init__(self, token, database, path, callbacks):
		self.test_led_on = database.child(f"{path}/test_led_on").get(token).val() or 0
		self.target_moisture = database.child(f"{path}/target_moisture").get(token).val() or 50
		self.target_light_level = database.child(f"{path}/target_light_level").get(token).val() or 50

		# We can't watch all values because then we will get a notification when we upload sensor values
		watched_keys = ["test_led_on", "target_moisture", "target_light_level"]
		self.streams = [database.child(f"{path}/{k}").stream(lambda m: self.stream_handler(m, callbacks.get(k, None)), token, k) for k in watched_keys]

	def stream_handler(self, message, callback):
		# This means the key no longer exists
		if message["data"] is None:
			return

		# This checks if this object (self) has an attribute with the same name as the stream_id
		# If this is true, it checks if they are equal, and if they are we can ignore the message
		# For example: If stream_id is "test_led_on", message["data"] is 1 and self.test_led_on is 1, we should ignore this message
		if getattr(self, message["stream_id"]) == message["data"]:
			return

		if callback:
			callback(message["data"])

	def stop(self):
		[s.close() for s in self.streams]

def init_database(login, callbacks={}):
	firebase = initialize_app(config_module.config)
	auth = firebase.auth()

	# TODO: Save token and refresh
	key = requests.get("https://europe-west1-greengarden-iot.cloudfunctions.net/requestNewToken", params=login).text

	if key == "missing_parameter": sys.exit("Missing parameter error")
	elif key == "invalid_serial": sys.exit("Invalid serial")
	elif key == "wrong_key": sys.exit("Wrong key for this serial number")
	else:
		user = auth.sign_in_with_custom_token(key)
		token = user["idToken"]

		database = firebase.database()
		path = f"garden/{login['serial']}"

		# Check if we have permission to access the part of the database reserved for this garden
		try: database.child(path).get(token)
		except: sys.exit(f"Failed to load database path {path}")

		return FirebaseDatabase(token, database, path, callbacks)
