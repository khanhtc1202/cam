import socket
import cv2

# create socket and bind host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8888))
connection = client_socket.makefile('wb')

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
