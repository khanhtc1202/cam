import threading
import SocketServer
import numpy as np
import cv2


class VideoStreamHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        print "Starting server video streaming..."
        stream_bytes = ' '

        face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
        # stream video frames one by one
        try:
            while True:
                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                # print "Data loaded = ", len(stream_bytes)
                if first != -1 and last != -1:
                    print "Frame loaded..."
                    jpg = stream_bytes[first:last + 2]
                    print "Size = ", len(jpg)
                    stream_bytes = stream_bytes[last + 2:]
                    gray = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
                    # image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)

                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        # roi_gray = gray[y:y + h, x:x + w]
                        # roi_color = img[y:y + h, x:x + w]
                    cv2.imshow('img', gray)
                    # break
                    # cv2.imshow('frame', gray)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            cv2.destroyAllWindows()
        finally:
            print "Connection closed on thread 1"


class ThreadServer(object):
    def server_thread(host, port):
        server = SocketServer.TCPServer((host, port), VideoStreamHandler)
        server.serve_forever()

    video_thread = threading.Thread(target=server_thread('0.0.0.0', 8888))
    video_thread.start()


if __name__ == '__main__':
    ThreadServer()
