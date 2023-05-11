import pathlib

# https://stackoverflow.com/questions/67631/how-can-i-import-a-module-dynamically-given-the-full-path
from importlib.machinery import SourceFileLoader
from pyrebaselite import initialize_app

config_file = pathlib.Path.home() / "green-garden" / "config.py"
token_file = pathlib.Path.home() / "green-garden" / "token.txt"

config_module = SourceFileLoader("config", str(config_file)).load_module()

app = initialize_app(config_module.config)
auth = app.auth()
database = app.database()
