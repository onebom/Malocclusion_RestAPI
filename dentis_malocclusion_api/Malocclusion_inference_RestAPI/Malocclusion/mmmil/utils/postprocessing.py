"""Utilities for model predicted result postprocessing."""

import numpy as np
from .preprocessing import  load_Data
from .modelprediction import load_model, model_prediction

def get_pseudo_distance_RL(prediction):
    """Get pseudo distance rounded score.

    Args:
      prediction: model prediction's output value for pesudo distance.
        To the second index of the `model_prediction` function's return value.

    Returns:
      (r,l): Right,left pseudo distance score tuple
         which rounded to have a value from -1 to 1
    """
    
    # Right prediction
    prediction_distance_r = prediction[0]
    # Left prediction
    prediction_distance_l = prediction[1]

    r = prediction_distance_r.copy()
    l = prediction_distance_l.copy()

    r = np.round(r, 3)
    l = np.round(l, 3)


    return r, l


def get_class_RL_and_prob_RL(prediction):
    """Get prediction's estimated class and probailities for all class

    Args:
      prediction: model prediction's output value for classification by one-hot encoding
        from the second index to the fourth index of the `model_prediction`function's return value.

    Returns:
      tuple consisting of a combination of estimated classes and probabilities for all class.
        - r_class: esitmated class (angle class),
            One of the class 1,2,3 for right data.
            The value determined through arguments of the maxima, 
            from one-hot probaliliteis for all class
        - l_class: esitmated class (angle class)
            One of the class 1,2,3 for left data.
            The value determined through arguments of the maxima, 
            from one-hot probaliliteis for all class
        - r_probs: prababilities of right data for all class (angle class).
            probability was calcaulated through the rounded one-hot predicted score
        - l_probs: prababilities of left data for all class (angle class)
            probability was calcaulated through the rounded one-hot predicted score
    """

    # Right prediction
    prediction_class_r = prediction[0]  
    # Left prediction
    prediction_class_l = prediction[1]

    r = prediction_class_r.copy()
    l = prediction_class_l.copy()

    r = r.tolist()
    r_class = np.argmax(r, axis=-1) + 1
    r_probs =np.round(r, 3)

    l = l.tolist()
    l_class = np.argmax(l, axis=-1) + 1
    l_probs = np.round(l, 3)

    return r_class, l_class, r_probs, l_probs



def get_inference_result(pred):
    """Get all predicted resault and Return it in a dictionary form.

    Args:
      prediction: model prediction's output value consisting of three types

    Returns:
      A dictionary including each inference predicted value.
    """
    inference_result = {}
    pseudo_r, pseudo_l = get_pseudo_distance_RL(pred[:2])
    r_class, l_class, r_prob, l_prob  = get_class_RL_and_prob_RL(pred[2:])

    inference_result["Right_class"] = r_class[0]
    inference_result["Left_class"] = l_class[0]
    inference_result["Right_onehot_predict"] = r_prob[0]
    inference_result["Left_onehot_predict"] = l_prob[0]
    inference_result["Right_regression_score"] = pseudo_r[0]
    inference_result["Left_regression_score"] = pseudo_l[0]

    return inference_result


import threading

ds_lock = threading.Lock()

#------------------------------------

def malocclusion_result(path):
    """final inference function with all pre&post processes in sequence 

    Args:
      path: path where the data are located

    Return:
      inference result value at dictionary form
    """

    # start -------------------------
    # for single thread.
    ds_lock.acquire() 
    
    x_test = load_Data(path)
    predict_list = model_prediction(x_test)

    result = get_inference_result(predict_list)
    ds_lock.release()
    # end -------------------------

    return result
