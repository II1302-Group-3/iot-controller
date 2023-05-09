import firebase.app as app
import requests

from enum import Enum
from queue import Queue
from termcolor import colored
from threading import Thread, Timer
from time import sleep, time

def request_token_from_file():
	with open(app.token_file, "r") as file:
		token = file.readline().strip()
		expiry_time = int(file.readline().strip())

		if time() >= expiry_time:
			raise Exception("Saved login token expired")

		return (token, int(expiry_time - time()))

def request_token_from_firebase(login):
	text = requests.get("https://europe-west1-greengarden-iot.cloudfunctions.net/requestNewToken", params=login).text

	if text == "missing_parameter": raise Exception("Missing parameter error")
	elif text == "invalid_serial": raise Exception("Invalid serial")
	elif text == "wrong_key": raise Exception("Wrong key for this serial number")

	token = text.split(':')[0]
	time_left = int(text.split(':')[1])

	return (token, time_left)

class FirebaseEvent(Enum):
	CONNECT = 0
	DISCONNECT = 1
	REFRESH_TOKEN = 2
	STOP = 3

class FirebaseConnection:
	def __init__(self, login, callbacks):
		self.user = None

		# Thread is blocked waiting on this queue
		self.events = Queue()
		# Push an event telling the thread to try to login to Firebase
		self.events.put(FirebaseEvent.CONNECT)

		self.connected_callback = callbacks.get("connected", None)
		self.disconnected_callback = callbacks.get("disconnected", None)

		self.thread = Thread(target=self.connection_thread, args=[login], daemon=True)
		self.thread.start()

	def connected(self):
		return self.user != None

	def token(self):
		return self.user["idToken"] if self.connected() else ""

	# Called when database has lost connection
	def disconnect(self):
		self.events.put(FirebaseEvent.DISCONNECT)

	def connection_thread(self, login):
		timer = None

		while True:
			event = self.events.get()

			# We are disconnected and should try to connect
			if event == FirebaseEvent.CONNECT:
				try:
					# First, try to use a token we saved to token.txt
					try:
						(token, time_left) = request_token_from_file()
					# Second, request from Firebase cloud function
					except:
						(token, time_left) = request_token_from_firebase(login)

						# Save the token we got from Firebase to token.txt
						with open(app.token_file, "w") as file:
							file.write(f"{token}\n{int(time() + time_left)}")

					self.user = app.auth.sign_in_with_custom_token(token)

					# The user token expires after an hour so we wait 45 minutes before refreshing
					timer = Timer(45 * 60, lambda: self.events.put(FirebaseEvent.REFRESH_TOKEN))
					timer.start()

					if self.connected_callback: self.connected_callback()

					print(colored("Connection status:", attrs=["bold"]), colored("Connected", "green"))
				except:
					# Try to connect again in 60 seconds
					timer = Timer(60, lambda: self.events.put(FirebaseEvent.CONNECT))
					timer.start()

					print(colored(f"Failed to connect (retrying in 60 seconds)", "red"))

			# If we are connected, disconnect and retry
			if event == FirebaseEvent.DISCONNECT:
				if self.connected():
					self.user = None

					if timer: timer.cancel()
					if self.disconnected_callback: self.disconnected_callback()

					# Try to connect again in 60 seconds
					timer = Timer(60, lambda: self.events.put(FirebaseEvent.CONNECT))
					timer.start()

					print(colored("Connection status:", attrs=["bold"]), colored("Disconnected", "red"))

			# Refresh the token and start a new timer
			if event == FirebaseEvent.REFRESH_TOKEN:
				self.user = app.auth.refresh(self.user["refreshToken"])

				timer = Timer(45 * 60, lambda: self.events.put(FirebaseEvent.REFRESH_TOKEN))
				timer.start()

			# Run disconnect callback and stop thread
			if event == FirebaseEvent.STOP:
				if timer: timer.cancel()

				if self.connected():
					self.user = None
					if self.disconnected_callback: self.disconnected_callback()

				return


	def stop(self):
		self.events.put(FirebaseEvent.STOP)

		tries = 0
		while tries < 50:
			if self.thread.is_alive():
				sleep(0.1)
				tries += 1
			else:
				return

		print(colored("Connection thread did not shut down in 5 seconds", "yellow"))
