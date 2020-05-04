
from face.face_process import face_recognize
from face.utils.config import get_config
import os
from scipy.stats import norm
import cv2
import math
import numpy as np
import pickle
from connector.query import Query
import datetime 
from datetime import datetime
import glob
class Data():
    def __init__(self):
        try:
            self.features=pickle.load(open("features.pickle","rb"))
        except:
            self.features=np.array([]).reshape(0,512)
        try:
            self.labels=pickle.load(open("labels.pickle","rb"))
        except:
            self.labels=[]
        # print(self.labels)
        print(self.features.shape)
        self.data_dir="data"
        self.threshold = 0.7318799151798612
        self.mu_0 = 89.6058
        self.sigma_0 = 4.5451
        self.mu_1 = 43.5357
        self.sigma_1 = 8.83
        self.threshold_distance=get_config().threshold_distance
        self.query=Query()

    def confidence(self, feature1, feature2):# shape (512,)
        shape= feature1.shape[-1]
        x0 = np.divide(feature1, np.stack([np.linalg.norm(feature1, axis=-1)]*shape, 0))
        x1 = np.divide(feature2, np.stack([np.linalg.norm(feature2, axis=-1)]*shape, 0))
        cosine = np.dot(x0, x1.T)

        theta = np.arccos(cosine)
        theta = theta * 180 / math.pi
        prob = self.get_prob(theta)
        #print(prob)
        return prob 

    def get_prob(self, theta):
        prob_0 = norm.pdf(theta, self.mu_0, self.sigma_0)
        prob_1 = norm.pdf(theta, self.mu_1, self.sigma_1)
        total = prob_0 + prob_1
        return prob_1 / total

    def add_data(self,feature,label):
        self.features=np.concatenate((self.features,feature))
        self.labels.append(label)

    def get_all_data(self):
        face=face_recognize(get_config(net_mode = 'ir_se', threshold = 1.22, detect_id = 1))
        ldir=os.listdir(self.data_dir)
        for x in ldir:
           path=os.path.join(self.data_dir,x)
           for path_img in glob.glob(path+"/*.*"):
               img=cv2.imread(path_img)
               features,boxes=face.feature_img(img)
               if(len(features)==1):
                    self.add_data(features[0].reshape(1,512),x)
        print("NUM WORKER ",self.features.shape)
        pickle.dump(self.features,open("features.pickle",'wb+'))
        pickle.dump(self.labels,open("labels.pickle",'wb+'))

    def identify(self, features):
            res=[]
            features= np.array(features)
            features=np.expand_dims(features, 1)
            diff = self.features - features
            dist = np.sum(np.power(diff, 2), axis=2)
            minimum = np.amin(dist, axis=1)
            min_idx = np.argmin(dist, axis=1)
            result = []
            for id,(min, min_id)  in enumerate(zip(minimum, min_idx)):          
                if min < self.threshold_distance:
                    # confidence = self.confidence(features[id].reshape(512,), self.features[min_id])
                    p_id = self.labels[min_id]
                    res.append(p_id)
                else:
                    res.append("Unknown")
            return res
    def add_attendance(self,id):
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        currtime=now.strftime("%H:%M:%S")
        self.query.add_attendance(id, date,currtime)

    
    def check(self,id):
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        return self.query.check_attendance(id,date)

                    


if __name__ == "__main__":
    x=Data()
    # x.get_all_data()
    # features=x.features[0:10]
    # x.identify(features)
    x.add_attendance("giang")
    x.add_attendance("giang")
    # print("1",x.check("1"))
    print("giang",x.check("giang"))


