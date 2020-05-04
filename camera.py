import cv2
from BaseCamera import BaseCamera
from face.face_process import face_recognize
from face.utils.config import get_config
from easydict import EasyDict as edict
from Process_frame import Process

process_frame = Process()
class Camera(BaseCamera):
   
    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames(unique_id):
        t=0
        #global face
        # camera = cv2.VideoCapture("rtsp://admin:adminFZCAVL@192.168.100.249/ISAPI/Streaming/channels/101")
        camera = cv2.VideoCapture('rtsp://admin:abc@123456@192.168.0.60')
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, frame = camera.read()
            frame=cv2.flip(frame,-1)
            t+=1
            
            frame=process_frame.process_frame(frame,t-1)
            
            yield frame
