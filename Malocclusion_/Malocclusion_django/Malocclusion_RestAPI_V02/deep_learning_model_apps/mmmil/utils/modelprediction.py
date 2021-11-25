

from tensorflow.keras import models
import numpy as np
import pandas as pd
import os
import glob
from tensorflow.keras import optimizers

## Global Variable 설정##########

ResourcePATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'resource')

Model1_PATH = os.path.join(ResourcePATH,'model1.h5')
Model2_PATH = os.path.join(ResourcePATH,'model2.h5')

# ---------------------------



############################################################
## model 한번에 load 해 놓기
#########################################

def load_model():
    model = models.load_model(Model1_PATH)
    model2 = models.load_model(Model2_PATH)

    return model, model2


#############################
# model 관련 함수 ####
###################

def model_prediction(x_test, model, model2):
    result = []

    prediction = model.predict(x_test)
    prediction2 = model2.predict(x_test)

    prediction_distance_r = prediction[0][:int(prediction[0].shape[0] / 2), 0]  # Right
    prediction_distance_l = prediction[0][int(prediction[0].shape[0] / 2):, 0]  # left

    prediction_class_r = prediction2[1][:int(prediction[1].shape[0] / 2)]  # Right
    prediction_class_l = prediction2[1][int(prediction[1].shape[0] / 2):]  # left

    result.append(prediction_distance_r)
    result.append(prediction_distance_l)
    result.append(prediction_class_r)
    result.append(prediction_class_l)

    return result