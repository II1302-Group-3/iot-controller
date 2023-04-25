import pyrebase

config = {
	"apiKey": "AIzaSyBlYOtxk9mWY9W2W0ciWuKJCxhkdt2uI3w",
	"authDomain": "greengarden-iot.firebaseapp.com",
	"databaseURL": "https://greengarden-iot-default-rtdb.europe-west1.firebasedatabase.app",
	"storageBucket": "greengarden-iot.appspot.com"
}

def init_database(serial, unique_key):
	firebase = pyrebase.initialize_app(config)
	auth = firebase.auth()
