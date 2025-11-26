import csv
import time
import os

class DroneLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.filename = os.path.join(self.log_dir, f"flight_data_{timestamp}.csv")

        # Define headers
        self.headers = [
            "Timestamp",
            "Battery (%)",
            "Height (cm)",
            "Temperature (C)",
            "Pitch",
            "Roll",
            "Yaw",
            "Barometer",
            "TOF (cm)"
        ]
        self.writer.writerow(self.headers)
        print(f"Logging data to {self.filename}")

    def __enter__(self):
        self.file = open(self.filename, 'w', newline='')
        self.writer = csv.writer(self.file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def log(self, drone_state):
        """
        Logs a row of data from the drone state.
        drone_state should be a dictionary or object with the required attributes.
        """
        row = [
            time.strftime("%H:%M:%S"),
            drone_state.get("battery"),
            drone_state.get("height"),
            drone_state.get("temp"),
            drone_state.get("pitch"),
            drone_state.get("roll"),
            drone_state.get("yaw"),
            drone_state.get("baro"),
            drone_state.get("tof")
        ]
        self.writer.writerow(row)
        self.file.flush() # Ensure data is written immediately

    def close(self):
        if self.file:
            self.file.close()
            print("Log file closed.")
