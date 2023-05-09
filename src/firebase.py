import pathlib
import requests

from sys import exit
from threading import Thread
from time import sleep, time

from pyrebaselite import initialize_app
from termcolor import colored

# https://stackoverflow.com/questions/67631/how-can-i-import-a-module-dynamically-given-the-full-path
from importlib.machinery import SourceFileLoader

config_file = pathlib.Path.home() / "green-garden" / "config.py"
config_module = SourceFileLoader("config", str(config_file)).load_module()

firebase = initialize_app(config_module.config)
auth = firebase.auth()

# We can't watch all values because then we will get a notification when we upload sensor values
watched_keys = ["target_moisture", "target_light_level"]

# How many seconds should pass between syncing to Firebase
sync_time = 10

token_file = pathlib.Path.home() / "green-garden" / "token.txt"

class FirebaseDatabase:
	def __init__(self, user, database, path, callbacks):
		self.user = user
		self.database = database
		self.path = path

		self.target_moisture = database.child(f"{path}/target_moisture").get(user["idToken"]).val() or 50
		self.target_light_level = database.child(f"{path}/target_light_level").get(user["idToken"]).val() or 50

		threads = [Thread(target=self.stream_thread, args=(k, callbacks.get(k, None)), daemon=True) for k in watched_keys]
		for t in threads: t.start()

		# The user token expires after an hour so we wait 45 minutes before refreshing
		self.next_token_refresh = time() + 45 * 60
		print(f"Refreshing token in 45 minutes")

		# Sync immediately
		self.next_sync_time = time()
		self.stop_sync = False

		self.sync_thread = Thread(target=self.sync_thread, daemon=True)
		self.sync_thread.start()

	def stream_handler(self, message, callback):
		key = message["stream_id"]
		value = message["data"]

		# This means the key no longer exists
		if value is None:
			return

		print(f"{key}={value}")
		setattr(self, key, value)

		if callback:
			callback(value)

	def stream_thread(self, key, callback):
		try:
			self.database.child(f"{self.path}/{key}").stream(lambda m: self.stream_handler(m, callback), self.user["idToken"], key, False)
		except:
			print(f"Stream {key} stopped")

	def sync_thread(self):
		while not self.stop_sync:
			try:
				if time() >= self.next_token_refresh:
					self.user = auth.refresh(self.user["refreshToken"])
					self.next_token_refresh = time() + 50 * 60

				if time() >= self.next_sync_time:
					# This can be used to determine if the Raspberry Pi has internet access
					self.database.child(f"{self.path}/last_sync_time").set(int(time()))
					self.next_sync_time = time() + 10
			except:
				print("Could not sync, timed out")

			sleep(1)

	def stop(self):
		self.stop_sync = True
		tries = 0

		while tries < 50:
			if not self.sync_thread.is_alive():
				return

			sleep(0.1)
			tries += 1

		print(colored("Sync thread did not shut down in 5 seconds", "red", attrs=["bold"]))

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

	if text == "missing_parameter": exit("Missing parameter error")
	elif text == "invalid_serial": exit("Invalid serial")
	elif text == "wrong_key": exit("Wrong key for this serial number")

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
	except: exit(f"Failed to load database path {path}")

	return FirebaseDatabase(user, database, path, callbacks)
