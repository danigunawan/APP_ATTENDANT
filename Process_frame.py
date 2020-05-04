from face.face_process import face_recognize
from face.utils.config import get_config
from easydict import EasyDict as edict
import cv2
import datetime 
from datetime import datetime
import numpy as np
from search import Data
import time
from tools import generate_detections as gdet
class Process(object):
    def __init__(self):
        self.config=get_config
        self.face=face_recognize(self.config(net_mode = 'ir_se', threshold = 1.22, detect_id = 1))
        self.search = Data()
        self.boxes=[]
        self.names=[]
    def process_frame(self, frame,t):
        if(t%4==0):
            try:
                features,boxes =self.face.feature_img(frame)
                self.boxes=boxes
                names=[]
                if(features.shape[0]!=0):
                    names=self.search.identify(features)
                self.names=names
                boxs=[]
                for box,name in zip(boxes,names):
                    if(name=="Unknown"):
                        text=""
                        cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])),(255,255,255), 2)
                    else:
                        self.search.add_attendance(name)
                        text=name
                        cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])),(255,255,255), 2)
                        now = datetime.now()
                        text=name+now.strftime("%H:%M:%S")
                    cv2.putText(frame, text,(int(box[0]), int(box[1])),0, 5e-3 * 200, (0,255,0),2)
                return frame
            except Exception:
                print(e)
                return frame
        else:
            for box,name in zip(self.boxes,self.names):
                    if(name=="Unknown"):
                        text=""
                        cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])),(255,255,255), 2)
                    else:
                        text=name
                        cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])),(255,255,255), 2)
                        now = datetime.now()
                        text=name+now.strftime("%H:%M:%S")
                    cv2.putText(frame, text,(int(box[0]), int(box[1])),0, 5e-3 * 200, (0,255,0),2)
            return frame


