from dotenv import load_dotenv
import os

load_dotenv()  # reads variables from a .env file and sets them in os.environ

def debug():
    return os.getenv("DEBUG") == "true"

def live_drone():
    return os.getenv("LIVE") != "false"

def interval():
    return os.getenv("INTERVAL")