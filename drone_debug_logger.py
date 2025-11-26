import csv
import json
import time
import os

class DroneDebugLogger:
    def __init__(self, log_dir="logs", mode="csv"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.filename = os.path.join(self.log_dir, f"flight_data_{timestamp}.json")

    def __enter__(self):
        self.file = open(self.filename, 'a')
        self.file.write("[")
        print(f"Logging data to {self.filename}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def log(self, drone_state):
        """
        Logs a row of data from the drone state.
        drone_state should be a dictionary or object with the required attributes.
        """
        state_str = json.dumps(drone_state)
        print(state_str)
        self.file.write(state_str + ",")
        self.file.flush() # Ensure data is written immediately

    def close(self):
        if self.file:
            self.file.write("]")
            self.file.close()
            print("Log file closed.")
