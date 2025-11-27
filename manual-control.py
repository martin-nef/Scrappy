# https://raw.githubusercontent.com/damiafuentes/DJITelloPy/refs/heads/master/examples/manual-control-opencv2.py

# simple example demonstrating how to control a Tello using your keyboard.
# For a more fully featured example see manual-control-pygame.py
# 
# Use W, A, S, D for moving, E, Q for rotating and R, F for going up and down.
# When starting the script the Tello will takeoff, pressing ESC makes it land
#  and the script exit.

# 简单的演示如何用键盘控制Tello
# 欲使用全手动控制请查看 manual-control-pygame.py
#
# W, A, S, D 移动， E, Q 转向，R、F上升与下降.
# 开始运行程序时Tello会自动起飞，按ESC键降落
# 并且程序会退出

from djitellopy import Tello
from drone_debug_logger import DroneDebugLogger
import cv2, math, time
import traceback
import numpy as np
import env
from stream_server import start_server_thread

VIDEO_FEED = env.video_feed()

def main():
    if not VIDEO_FEED:
        start_server_thread(None)
        tello = connect()
    else:
        tello = connect()
        # start_feed(tello)

    time.sleep(1)

    with DroneDebugLogger() as logger:
        while True:
            try:
                log(logger, tello)
                fly(tello)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e.__class__.__name__)
                print(traceback.format_exc())
                continue
    end(tello)





def connect():
    tello = Tello(host=env.drone_ip())

    i = 0
    while True:
        try:
            print("Connecting...")
            wait = False
            if i % 2 == 1:
                wait = True
            tello.connect(wait)
            time.sleep(1)
            # tello.set_video_bitrate(Tello.BITRATE_1MBPS)
            # tello.set_video_resolution(Tello.RESOLUTION_480P)
            # tello.set_video_fps(Tello.FPS_15)
            # tello.set_video_direction(Tello.CAMERA_FORWARD)
            tello.streamoff()
            # tello.streamon()
            print("\n\nConnected!!!")
            break
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(e)
            continue
    return tello


def start_feed(tello):
    tello.streamoff()
    tello.streamon()
    print("Waiting for video stream to stabilize...")
    time.sleep(2)
    start_server_thread()
    return

    frame_read = None
    retry_count = 0
    while True:
        try:
            print("obtaining frame read...")
            frame_read = tello.get_frame_read()
            if frame_read:
                start_server_thread(frame_read)
                break
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(e.__class__.__name__)
            print(traceback.format_exc())
            print("Retrying in 1 second...")
            time.sleep(1)
            retry_count += 1
            if retry_count > 5:
                print("Max retries exceeded for video stream.")
                break
            continue





def log(logger, tello):
    try:
        logger.log(tello.get_current_state())
    except Exception as e:
        print("Failed to log state")
        print(e.__class__.__name__)
        print(traceback.format_exc())





def fly(tello):
    try:
        # keep_alive(tello)

        key = cv2.waitKey(1) & 0xff
        if key == 27: # ESC
            tello.emergency()
            print("Emergency landing...")
        elif key == ord('w'):
            print("Moving forward...")
            tello.move_forward(30)
        elif key == ord('s'):
            print("Moving back...")
            tello.move_back(30)
        elif key == ord('a'):
            print("Moving left...")
            tello.move_left(30)
        elif key == ord('d'):
            print("Moving right...")
            tello.move_right(30)
        elif key == ord('e'):
            print("Rotating clockwise...")
            tello.rotate_clockwise(30)
        elif key == ord('q'):
            print("Rotating counter-clockwise...")
            tello.rotate_counter_clockwise(30)
        elif key == ord('r') or key == cv2.EVENT_FLAG_SHIFTKEY:
            print("Moving up...")
            tello.move_up(30)
        elif key == ord('f') or key == cv2.EVENT_FLAG_CTRLKEY:
            print("Moving down...")
            tello.move_down(30)
        elif key == ord('m'):
            print("Turning motor on...")
            tello.turn_motor_on()
        elif key == ord('l'):
            print("Landing...")
            tello.land()
        elif key == ord('n'):
            print("Turning motor off...")
            tello.turn_motor_off()
        elif key == ord(' ') or key == ord('t'):
            print("Taking off...")
            tello.takeoff() 
    except Exception as e:
        print("Failed to end flight gracefully")
        print(e.__class__.__name__)
        print(traceback.format_exc())





def end(tello):
    try:
        print("Ending flight...")
        tello.land()
        # tello.end()
    except Exception as e:
        print("Failed to end flight gracefully")
        print(e.__class__.__name__)
        print(traceback.format_exc())
    finally:
        exit()

def keep_alive(tello):
    try:
        print("Sending keepalive...")
        tello.send_keepalive()
    except Exception as e:
        print(e.__class__.__name__)
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
