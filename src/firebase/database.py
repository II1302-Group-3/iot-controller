import firebase.app as app
from firebase.connection import FirebaseConnection

from threading import Thread
from time import sleep, time
from termcolor import colored

# We can't watch all values because then we will get a notification when we upload sensor values
watched_keys = ["target_moisture", "target_light_level"]
# How many seconds should pass between syncing to Firebase
sync_time = 10

class FirebaseDatabase:
	def __init__(self, login, callbacks={}):
		self.path = f"garden/{login['serial']}"

		self.target_moisture = 0
		self.target_light_level = 0

		self.next_sync_time = 0
		self.syncing = False

		# Will be sent once the Raspberry Pi connects to the internet
		self.queued_water_level_notification = False

		self.connection = FirebaseConnection(login, {
			"connected": lambda: self.connected_handler(callbacks),
			"disconnected": self.disconnected_handler
		})

	# TODO: Should be used by water_sensor.py to send a notification if GPIO pin goes from HIGH to LOW
	def send_water_level_notification(self):
		self.queued_water_level_notification = True

		if self.connection.connected():
			print("Sending notification to app that the water level is low")
		else:
			print(colored("Warning: Tried to send notification while offline", "yellow"))
			print(colored("Notification will be sent as soon as the Raspberry Pi is connected to the internet", "yellow"))

	def connected_handler(self, callbacks):
		self.target_moisture = app.database.child(f"{self.path}/target_moisture").get(self.connection.token()).val() or 0
		self.target_light_level = app.database.child(f"{self.path}/target_light_level").get(self.connection.token()).val() or 0

		for key in watched_keys:
			callback = callbacks.get(key, None)

			if callback:
				callback(getattr(self, key))

			Thread(target=self.stream_thread, args=[key, callback], daemon=True).start()

		# Sync immediately
		self.next_sync_time = time()
		self.syncing = True

		self.current_sync_thread = Thread(target=self.sync_thread, daemon=True)
		self.current_sync_thread.start()

	def disconnected_handler(self):
		self.syncing = False
		tries = 0

		while tries < 50:
			if self.current_sync_thread.is_alive():
				sleep(0.1)
				tries += 1
			else:
				return

		print(colored("Sync thread did not shut down in 5 seconds", "yellow"))

	def stream_handler(self, message, callback):
		key = message["stream_id"]
		value = message["data"]

		# This means the key no longer exists
		if value == None:
			return

		# If the key already has the same value in our local database
		if getattr(self, key) == value:
			return

		setattr(self, key, value)

		if callback:
			callback(value)

	def stream_thread(self, key, callback):
		try:
			app.database.child(f"{self.path}/{key}").stream(lambda m: self.stream_handler(m, callback), self.connection.token(), key, False)
		except:
			print(colored(f"Stream {key} stopped", "red"))
			self.connection.disconnect()

	def sync_thread(self):
		while self.syncing:
			try:
				if time() >= self.next_sync_time:
					# This can be used to determine if the Raspberry Pi has internet access
					app.database.child(f"{self.path}/last_sync_time").set(int(time()))

					if self.queued_water_level_notification:
						app.database.child(f"{self.path}/water_level_low").set(True)
						self.queued_water_level_notification = False

					self.next_sync_time = time() + sync_time
			except:
				print(colored(f"Syncing timed out", "red"))
				self.connection.disconnect()
				return

			sleep(1)

	def stop(self):
		self.connection.stop()
