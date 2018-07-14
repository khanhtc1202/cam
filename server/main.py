import SocketServer
import numpy as np
import sys
import cv2

HOST = sys.argv[1]
PORT = int(sys.argv[2])


class FrameCreator(object):
    def __init__(self):
        self.frame_tool = cv2

    def showing(self, src_info, stream_bytes):
        trunk = ''
        while True:
            trunk += stream_bytes.read(1024)
            frame_head = trunk.find('\xff\xd8')
            frame_tail = trunk.find('\xff\xd9')
            if frame_head != -1 and frame_tail != -1:
                jpg_frame = trunk[frame_head:frame_tail+2]
                trunk = trunk[frame_tail+2:]
                print 'Receive data from {} with size = {}'.format(src_info, len(jpg_frame))
                gray_scale_frame = self.frame_tool.imdecode(
                    np.fromstring(jpg_frame, dtype=np.uint8),
                    self.frame_tool.CV_LOAD_IMAGE_GRAYSCALE)
                self.frame_tool.imshow(src_info, gray_scale_frame)
                if self.frame_tool.waitKey(1) & 0xFF == ord('q'):
                    break
        self.frame_tool.destroyAllWindows()


class VideoStreamHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        print 'Start receive data from {}'.format(self.client_address)
        client_ip = self.client_address[0]
        try:
            FrameCreator().showing(client_ip, self.rfile)
        finally:
            print 'Connection closed with {}'.format(self.client_address)


class Server(object):
    @staticmethod
    def run(host, port):
        print "Starting server video streaming..."
        server = SocketServer.ThreadingTCPServer((host, port), VideoStreamHandler)
        server.serve_forever()


if __name__ == '__main__':
    Server.run(HOST, PORT)
