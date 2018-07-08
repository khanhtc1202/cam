import threading
import SocketServer
import numpy as np
import sys
import cv2

HOST = sys.argv[1]
PORT = int(sys.argv[2])


class VideoStreamHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        print "Starting server video streaming..."
        stream_bytes = ' '

        try:
            while True:
                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    print "Frame loaded..."
                    jpg = stream_bytes[first:last + 2]
                    print "Size = ", len(jpg)
                    stream_bytes = stream_bytes[last + 2:]
                    gray = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
                    cv2.imshow('frame', gray)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            cv2.destroyAllWindows()
        finally:
            print "Connection closed on thread 1"


class Server(object):
    @staticmethod
    def run(host, port):
        server = SocketServer.TCPServer((host, port), VideoStreamHandler)
        server.serve_forever()


def main():
    video_thread = threading.Thread(target=Server.run, args=(HOST, PORT))
    video_thread.start()

if __name__ == '__main__':
    main()
