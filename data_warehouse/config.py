import configparser
import os

from dotenv import load_dotenv


ROOT_PATH = os.path.dirname(__file__)


load_dotenv(os.path.join(ROOT_PATH, ".env"))
CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(ROOT_PATH, "dwh.cfg"))
CONFIG.add_section("AWS")
CONFIG.set("AWS", "KEY", os.environ.get("AWS_KEY"))
CONFIG.set("AWS", "SECRET", os.environ.get("AWS_SECRET"))
