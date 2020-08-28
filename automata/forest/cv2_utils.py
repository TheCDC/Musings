import numpy as np
import cv2
def numpy_to_cv2(arr:np.array):
    
    return cv2.cvtColor(arr.astype('float32') / 255, cv2.COLOR_RGB2BGR)