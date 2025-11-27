from flask import Flask, Response, render_template_string
import cv2
import threading
import time
import numpy as np
import env




app = Flask(__name__)
frame_read = None
drone_videostream = None

# HTML template for the video feed page
PAGE_HTML = """
<html>
  <head>
    <title>Tello Video Feed</title>
    <style>
      body { background-color: #111; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: sans-serif; }
      h1 { position: absolute; top: 20px; }
      img { border: 2px solid #444; box-shadow: 0 0 20px rgba(0,0,0,0.5); max-width: 90%; max-height: 90%; }
    </style>
  </head>
  <body>
    <h1>Tello Live Feed</h1>
    <img src="{{ url_for('video_feed') }}">
  </body>
</html>
"""





def generate_frames():
    global frame_read
    while True:
        if frame_read and frame_read.frame is not None:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame_read.frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            if frame is None:
                # Create a black background for the window so that waitKey works
                height, width = 360, 480
                frame = np.zeros((height, width, 3), np.uint8)

            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            




def generate_frames_web():
    global drone_videostream
    while True:
        if drone_videostream is None:   
            print("drone_videostream is None")
            time.sleep(1)
            drone_videostream = cv2.VideoCapture('udp://' + env.drone_ip() + ':11111?overrun_nonfatal=1&fifo_size=5000')
            continue

        ret, frame = drone_videostream.read()
        if frame is None:
            # Create a black background for the window so that waitKey works
            height, width = 360, 480
            frame = np.zeros((height, width, 3), np.uint8)
        else:
            print("We have footage!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    




@app.route('/')
def index():
    return render_template_string(PAGE_HTML)





@app.route('/video_feed')
def video_feed():
    global drone_videostream
    global frame_read
    if frame_read is not None:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response(generate_frames_web(), mimetype='multipart/x-mixed-replace; boundary=frame')




def run_server(tello_frame_read):
    global frame_read
    frame_read = tello_frame_read
    # Run Flask server on 0.0.0.0 to be accessible externally if needed, port 5000
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)





def run_server_web():
    global drone_videostream
    drone_videostream = cv2.VideoCapture('udp://' + env.drone_ip() + ':11111')
    while True:
        ret, frame = drone_videostream.read()
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    drone_videostream.release()





def start_server_thread(tello_frame_read=None):
    t = None
    if tello_frame_read is None:
        t = threading.Thread(target=run_server_web)
    else:
        t = threading.Thread(target=run_server, args=(tello_frame_read,))
    t.daemon = True
    t.start()
    print("Video stream server started at http://localhost:5000")





if __name__ == '__main__':
    try:
        run_server_web()
    except KeyboardInterrupt:
        exit()
