from face.face_process import face_recognize
from face.utils.config import get_config
from easydict import EasyDict as edict
from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from deep_sort.detection import Detection as ddet
import cv2
import datetime 
from datetime import datetime
import numpy as np
from search import Data
from tools import generate_detections as gdet
class Process(object):
    def __init__(self):
        self.max_cosine_distance = 0.3
        self.nn_budget = None
        self.nms_max_overlap = 1.0
        model_filename = 'model_data/mars-small128.pb'
        self.encoder = gdet.create_box_encoder(model_filename,batch_size=1)
        self.metric = nn_matching.NearestNeighborDistanceMetric("cosine", self.max_cosine_distance, self.nn_budget)
        self.tracker = Tracker(self.metric)
        self.config=get_config
        self.face=face_recognize(self.config(net_mode = 'ir_se', threshold = 1.22, detect_id = 1))
        self.search = Data()

    def process_frame(self, frame):
        features,boxes =self.face.feature_img(frame)
        name=[]
        if(features.shape[0]!=0):
            name=self.search.identify(features)

        boxs=[]
        for box in boxes:
            boxs.append(np.array([box[0],box[1],box[2]-box[0],box[3]-box[1]]))
        features = self.encoder(frame,boxs)
        detections = [Detection(bbox, 1.0, feature) for bbox, feature in zip(boxs, features)]
        # Run non-maxima suppression.
        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = preprocessing.non_max_suppression(boxes, self.nms_max_overlap,scores)
        detections = [detections[i] for i in indices]
        
        self.tracker.predict()
        self.tracker.update(detections,name)
        # Call the tracker
        
        for track in self.tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue 
            bbox = track.to_tlbr()
            name=track.name
            if(name=="Unknown"):text=""
            if(track.hits>=6 and name!="Unknown"):
                self.search.add_attendance(name)
            if(not self.search.check(name)):
                cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,255,255), 2)
                text=name
            else:
                cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,0,0), 2)
                now = datetime.now()
                text=name+now.strftime("%H:%M:%S")
            cv2.putText(frame, text,(int(bbox[0]), int(bbox[1])),0, 5e-3 * 200, (0,255,0),2)
        
        return frame


