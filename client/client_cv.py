import socket
import cv2

# create socket and bind host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8888))
connection = client_socket.makefile('wb')


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        self.video.set(3, 320)  # pi camera resolution
        self.video.set(4, 240)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpeg', image)
        return jpeg.tobytes(), jpeg



def gen(camera):
    while True:
        frame, image = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


try:
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)
    cap.set(4, 240)
    # stream = io.BytesIO()
    while True:
        success, frame = cap.read()
        ret, jpeg = cv2.imencode('.jpeg', frame)
        connection.write(jpeg.tobytes())
        connection.flush()
finally:
    # pass
    connection.close()
    client_socket.close()
