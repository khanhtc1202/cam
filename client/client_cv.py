import sys
import socket
import cv2

HOST = sys.argv[1]
PORT = int(sys.argv[2])

# create socket and bind host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
connection = client_socket.makefile('wb')

try:
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)
    cap.set(4, 240)
    while True:
        success, frame = cap.read()
        ret, jpeg = cv2.imencode('.jpeg', frame)
        connection.write(jpeg.tobytes())
        connection.flush()
finally:
    # pass
    connection.close()
    client_socket.close()
