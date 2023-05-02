# Green Garden IoT Controller

Controller for a smart garden written in Python

## How to use

1. Install pip (Raspberry Pi: `sudo apt install python3-pip`, Arch Linux: `sudo pacman -S python-pip`)
2. Install pipenv (Raspberry Pi: `sudo apt install pipenv`, Arch Linux: `sudo pacman -S python-pipenv`)
3. If you are testing on the Raspberry Pi, run `export PIPENV_PYPI_MIRROR=https://www.piwheels.org/simple`
4. Run `pipenv install --skip-lock`
5. Run the program with `pipenv run python src/main.py`

## Firebase API key

A Firebase API config needs to be put in `~/green-garden/config.py` for the controller to work. The IoT controller uses the normal Web API key.

More information on what `config.py` needs to contain can be found here: [https://github.com/nhorvath/Pyrebase4](https://github.com/nhorvath/Pyrebase4)

## Serial Number

Every Green Garden has a unique serial number that users can register in the app. The serial number is stored in the home directory (`~/green-garden/serial.txt`).

* To generate a new serial number: `pipenv run python src/main.py --new-serial`
* To set the serial number: `pipenv run python src/main.py --set-serial (new serial number)`

Generating a new serial number requires a secret password. Users can't change the serial number of their smart garden without the permission of the project group/product owner.
