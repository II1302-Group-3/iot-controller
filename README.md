# Green Garden IoT Controller

## How to use

1. Install pip (Raspbian: `sudo apt install python3-pip`, Arch: `sudo pacman -S python-pip`)
2. Install pipenv (Raspbian: `sudo apt install pipenv`, Arch: `sudo pacman -S python-pipenv`)
3. Run `pipenv sync`
4. Run the program with `pipenv run python src/main.py`

## Serial Number

Every Green Garden has a unique serial number that users can register in the app. The serial number is stored in the home directory (`~/green-garden/serial.txt`).

* To generate a new serial number: `pipenv run python src/main.py --new-serial`
* To set the serial number: `pipenv run python src/main.py --set-serial (new serial number)`

## Components

* `src/firebase.py`: Contains functions for connecting to Firebase to retrieve target configuration and send updated sensor values
* `src/serial.py`: Contains functions for managing the serial number of the garden
