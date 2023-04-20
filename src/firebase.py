import firebase_admin
import pathlib
import sys

from firebase_admin import credentials
from firebase_admin import db

class FirebaseData:
	led_on = 0
	target_moisture = 0
	target_light_level = 0
	stop = None

def init_database(serial, on_led_on, on_new_moisture_target, on_new_light_level_target):
	home_dir = pathlib.Path.home() / "green-garden"
	cred_file = home_dir / "firebase.json"

	if not cred_file.exists():
		print("Firebase API keys not found")
		sys.exit(1)

	cred = credentials.Certificate(cred_file)
	firebase_admin.initialize_app(cred, { "databaseURL": "https://greengarden-iot-default-rtdb.europe-west1.firebasedatabase.app/" })

	# Test if we have access to database
	try:
		db.reference(f"garden/placeholder").get()
	except firebase_admin.exceptions.UnauthenticatedError:
		print("Error trying to access /garden/placeholder")

	user_db_object = FirebaseData()
	user_db_object.led_on = db.reference(f"garden/placeholder/test_led_on").get()
	user_db_object.target_moisture = db.reference(f"garden/placeholder/target_moisture").get()
	user_db_object.target_light_level = db.reference(f"garden/placeholder/target_light_level").get()

	def callback_led_on(event):
		if user_db_object.led_on != event.data:
			user_db_object.led_on = event.data
			on_led_on(event.data)

	def callback_new_moisture_target(event):
		if user_db_object.target_moisture != event.data:
			user_db_object.target_moisture = event.data
			on_new_moisture_target(event.data)

	def callback_new_light_level(event):
		if user_db_object.target_light_level != event.data:
			user_db_object.target_light_level = event.data
			on_new_light_level_target(event.data)

	stoppers = [
		db.reference(f"garden/placeholder/test_led_on").listen(callback_led_on),
		db.reference(f"garden/placeholder/target_moisture").listen(callback_new_moisture_target),
		db.reference(f"garden/placeholder/target_light_level").listen(callback_new_light_level)
	]

	def callback_stop():
		for stopper in stoppers:
			stopper.close()

	user_db_object.stop = callback_stop

	return user_db_object

