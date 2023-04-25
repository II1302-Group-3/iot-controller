from pyrebase import initialize_app
from .config import config

import requests
import sys

def FirebaseData():
	led_on = 1

def init_database(login, f1, f2, f3):
	firebase = initialize_app(config)
	auth = firebase.auth()

	# TODO: Save token and refresh

	params = { "serial": login["serial"], "key": login["unique_key"] }
	key = requests.get("https://europe-west1-greengarden-iot.cloudfunctions.net/requestNewToken", params=params).text

	if key == "missing_parameter": print("Missing parameter error")
	elif key == "invalid_serial": print("Invalid serial")
	elif key == "wrong_key": print("Wrong key for this serial number")
	else:
		user = auth.sign_in_with_custom_token(key)
		return FirebaseData()

	sys.exit(1)
