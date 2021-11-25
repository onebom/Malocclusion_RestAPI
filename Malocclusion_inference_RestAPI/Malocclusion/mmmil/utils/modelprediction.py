"""Utils loading model and returning model's predicted output"""
from tensorflow.keras import models
import numpy as np
import pandas as pd
import os
import glob
from tensorflow.keras import optimizers

ResourcePATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'resource')
model_type5_path = os.path.join(ResourcePATH,'model.hdf5')
weight_path      = os.path.join(ResourcePATH,'weight.hdf5')



def load_model():
    """Loading a model with static model save path

    Returns:
      A weighted type5 model 
    """
    model = models.load_model(model_type5_path)
    model.load_weights(weight_path)
    return model


# load model for the first and last time
# in util module
model_type5 = load_model()


def model_prediction(x_test):
    """Returns the results predicted by model for the test data set.

    Args:
      x_test: input tensor

    Returns:
      result in the form of a list.
      One list contain three types of prediction value.
      - prediction_pseudo_distance 
      - prediction_class
      - prediction_measured_distance
    """
    result = []

    # model predict data set.
    # predction form:
    # prediction contatins R,L data together in one dimension
    # [0]: pseudo_distance [#_of_samples_right + #_of_samples_left,0]
    # [1]: classification [#_of_samples_right + #_of_samples_left] (ont-hot encoded)
    # [2] : measured_distance [#_of_samples_right + #_of_samples_left]
    prediction = model_type5.predict(x_test)

    prediction_pseudo_distance_r = prediction[0][:int(prediction[0].shape[0] / 2), 0]  # Right
    prediction_pseudo_distance_l = prediction[0][int(prediction[0].shape[0] / 2):, 0]  # left

    prediction_class_r = prediction[1][:int(prediction[1].shape[0] / 2)]  # Right
    prediction_class_l = prediction[1][int(prediction[1].shape[0] / 2):]  # left

    prediction_measured_distance_r = prediction[2][:int(prediction[2].shape[0] / 2)]  # Right
    prediction_measured_distance_l = prediction[2][int(prediction[2].shape[0] / 2):]  # left

    result.append(prediction_pseudo_distance_r)
    result.append(prediction_pseudo_distance_l)
    result.append(prediction_class_r)
    result.append(prediction_class_l)
    result.append(prediction_measured_distance_r)
    result.append(prediction_measured_distance_l)

    return result

