from djitellopy import Tello
from drone_debug_logger import DroneDebugLogger
from drone_logger import DroneLogger
import argparse
import env
import sys
import time
import traceback

def main():
    parser = argparse.ArgumentParser(description="Tello Drone Data Collector")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode without connecting to a real drone")
    parser.add_argument("--interval", type=float, default=env.interval() or 1.0, help="Logging interval in seconds")
    args = parser.parse_args()
    interval = args.interval

    if args.mock or not env.live_drone():
        print("Starting in MOCK mode.")
        drone = MockTello()
    else:
        if Tello is None:
            print("Error: djitellopy library not found. Please install it using 'pip install djitellopy'")
            sys.exit(1)
        print("Connecting to real Tello drone...")
        drone = Tello()

    with (DroneDebugLogger() if env.debug() else DroneLogger()) as logger:
        try:
            for i in range(5):
                try:
                    drone.connect(wait_for_state=True)
                    time.sleep(1)
                except Exception as e:
                    print(Exception, e)
                    continue

            print("Press Ctrl+C to stop logging.")
            while True:
                state = drone.get_current_state()
                logger.log(state)
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\nStopping logging...")
        except Exception as e:
            print(Exception, e)
            print(traceback.format_exc())
        finally:
            if hasattr(drone, 'end'):
                drone.end()
            print("Exiting.")


if __name__ == "__main__":
    main()
