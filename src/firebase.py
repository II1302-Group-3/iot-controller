import pathlib
import requests
import sys

from pyrebaselite import initialize_app
from time import sleep, time

# https://stackoverflow.com/questions/67631/how-can-i-import-a-module-dynamically-given-the-full-path
from importlib.machinery import SourceFileLoader

config_file = pathlib.Path.home() / "green-garden" / "config.py"
config_module = SourceFileLoader("config", str(config_file)).load_module()

firebase = initialize_app(config_module.config)
auth = firebase.auth()

# We can't watch all values because then we will get a notification when we upload sensor values
watched_keys = ["test_led_on", "target_moisture", "target_light_level"]
# These are keys that the IoT controller uploads to the database
synced_keys = []

# How many seconds should pass between syncing to Firebase
sync_time = 10

token_file = pathlib.Path.home() / "green-garden" / "token.txt"

class FirebaseDatabase:
	def __init__(self, user, database, path, callbacks):
		self.user = user
		self.database = database
		self.path = path

		self.test_led_on = database.child(f"{path}/test_led_on").get(user["idToken"]).val() or 0
		self.target_moisture = database.child(f"{path}/target_moisture").get(user["idToken"]).val() or 50
		self.target_light_level = database.child(f"{path}/target_light_level").get(user["idToken"]).val() or 50

		self.streams = [database.child(f"{path}/{k}").stream(lambda m: self.stream_handler(m, callbacks), user["idToken"], k) for k in watched_keys]

		# The user token expires after an hour so we wait 45 minutes before refreshing
		self.next_token_refresh = time() + 45 * 60
		print(f"Refreshing token in 45 minutes")

		self.next_sync_time = time()

	def stream_handler(self, message, callbacks):
		key = message["stream_id"]
		value = message["data"]

		# This means the key no longer exists
		if value is None:
			return

		# This checks if this object (self) has an attribute with the same name as the stream_id
		# If this is true, it checks if they are equal, and if they are we can ignore the message
		# For example: If stream_id is "test_led_on", message["data"] is 1 and self.test_led_on is 1, we should ignore this message
		#if getattr(self, key) == value:
		#	return
		# Code is commented out because we want to run callbacks on start

		setattr(self, key, value)

		callback = callbacks.get(key, None)

		if callback:
			callback(value)

	# Needs to be called regularly to sync data to Firebase
	def sync(self):
		if time() >= self.next_token_refresh:
			self.user = auth.refresh(self.user["refreshToken"])
			self.next_token_refresh = time() + 50 * 60

		if time() >= self.next_sync_time:
			# This can be used to determine if the Raspberry Pi has internet access
			self.database.child(f"{self.path}/last_sync_time").set(int(time()))
			self.next_sync_time = time() + 10

	def stop(self):
		[s.close() for s in self.streams]

def request_token_from_file():
	with open(token_file, "r") as file:
		token = file.readline().strip()
		expiry_time = int(file.readline().strip())

		if time() >= expiry_time:
			raise Exception("Saved login token expired")

		print(f"Got login token from token.txt that expires in {expiry_time - int(time())} seconds")

		return token

def request_token_from_firebase(login):
	text = requests.get("https://europe-west1-greengarden-iot.cloudfunctions.net/requestNewToken", params=login).text

	if text == "missing_parameter": sys.exit("Missing parameter error")
	elif text == "invalid_serial": sys.exit("Invalid serial")
	elif text == "wrong_key": sys.exit("Wrong key for this serial number")

	token = text.split(':')[0]
	time_left = int(text.split(':')[1])

	print(f"Got {text.split(':')[2]} login token from Firebase that expires in {time_left} seconds")

	return (token, time_left)

def init_database(login, callbacks={}):
	try:
		print("(1) Trying to sign in with saved login token")
		# First, try to use a token we saved to token.txt
		user = auth.sign_in_with_custom_token(request_token_from_file())
	except:
		print("(2) Trying to sign in by requesting login token from Firebase")

		(token, time_left) = request_token_from_firebase(login)
		user = auth.sign_in_with_custom_token(token)

		# Save the token we got from Firebase to token.txt
		with open(token_file, "w") as file:
			file.write(f"{token}\n{int(time() + time_left)}")

	database = firebase.database()
	path = f"garden/{login['serial']}"

	# Check if we have permission to access the part of the database reserved for this garden
	try: database.child(path).get(user["idToken"])
	except: sys.exit(f"Failed to load database path {path}")

	return FirebaseDatabase(user, database, path, callbacks)
