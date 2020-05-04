from face.face_process import face_recognize
from face.utils.config import get_config
import cv2
import numpy as np

a=np.array([[1,2],[3,4],[3,4],[7,8]])
b=np.array([[1,2],[3,4],[7,8]])
b=np.expand_dims(b, 1)
c=a-b
dist = np.sum(np.power(c, 2), axis=2)
minimum = np.amin(dist, axis=1)
min_idx = np.argmin(dist, axis=1)
print(min_idx)    
