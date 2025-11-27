from dotenv import load_dotenv
import os

load_dotenv()  # reads variables from a .env file and sets them in os.environ

def debug():
    return os.getenv("DEBUG", "false") == "true"

def live_drone():
    return os.getenv("LIVE", "true") == "true"

def interval():
    return float(os.getenv("INTERVAL", "0.5"))

def video_feed():
    return os.getenv("VIDEO_FEED", "true") == "true"

def drone_ip():
    return os.getenv("DRONE_IP", "192.168.10.1")
