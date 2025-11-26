
class MockTello:
    """Mock class to simulate Tello drone behavior."""
    def __init__(self):
        print("[MOCK] Initializing MockTello...")
        self.battery = 100
        self.height = 0
        self.temp = 25
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.baro = 100.0
        self.tof = 10

    def get_current_state(self):
        return {
                    "battery": self.get_battery(),
                    "height": self.get_height(),
                    "temp": self.get_temperature(),
                    "pitch": self.get_pitch(),
                    "roll": self.get_roll(),
                    "yaw": self.get_yaw(),
                    "baro": self.get_barometer(),
                    "tof": self.get_distance_tof()
                }

    def connect(self):
        print("[MOCK] Connecting to drone...")
        time.sleep(1)
        print("[MOCK] Connected!")

    def get_battery(self):
        self.battery = max(0, self.battery - 1)
        return self.battery

    def get_height(self):
        self.height = (self.height + 1) % 100
        return self.height

    def get_temperature(self):
        return self.temp

    def get_pitch(self):
        return self.pitch
    
    def get_roll(self):
        return self.roll
    
    def get_yaw(self):
        return self.yaw
    
    def get_barometer(self):
        return self.baro
    
    def get_distance_tof(self):
        return self.tof

    def end(self):
        print("[MOCK] Disconnecting...")
