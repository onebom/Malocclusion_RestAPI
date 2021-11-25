import numpy as np
from .preprocessing import  load_Data
from .modelprediction import load_model, model_prediction
####################
# Utils  함수들
###################

def regression_predict(prediction):

    prediction_distance_r = prediction[0]  # Right
    prediction_distance_l = prediction[1]  # left

    r = prediction_distance_r.copy()
    l = prediction_distance_l.copy()

    # -1~1사이 score
    r = np.round(r)  # 반올림
    r[r < -1] = -1
    r[r > 1] = 1


    l = np.round(l)
    l[l < -1] = -1
    l[l > 1] = 1


    return int(r), int(l)


def one_hot_predict(prediction):

    prediction_class_r = prediction[0]  # Right
    prediction_class_l = prediction[1]  # left

    r = prediction_class_r.copy()
    l = prediction_class_l.copy()

    # onehot value score # 반올림
    r = r.tolist()
    r2 = np.round(r, 3)
    r3 = []
    for xx in r2:
        if xx[0] == np.max(xx):
            xx = 0
        elif xx[1] == np.max(xx):
            xx = 1
        elif xx[2] == np.max(xx):
            xx = -1
        r3.append(xx)

    l = l.tolist()
    l2 = np.round(l, 3)
    l3 = []
    for xy in l2:
        if xy[0] == np.max(xy):
            xy = 0
        elif xy[1] == np.max(xy):
            xy = 1
        elif xy[2] == np.max(xy):
            xy = -1
        l3.append(xy)

    return str(r2), str(l2), str(r3), str(l3)


def predict_postprocessing(result):
    inference_result = {}
    regress_r, regress_l , regress_argm_r, regress_argm_l = regression_predict(result[:2])
    onehot_r, onehot_l = one_hot_predict(result[2:])

    inference_result["Right_regression_predict_class"] = regress_r
    inference_result["Left_regression_predict_class"] = regress_l
    inference_result["Right_onehot_predict_class"] = onehot_r
    inference_result["Left_onehot_predict_class"] = onehot_l

    return inference_result


def malocclusion_result(path):
    x_test = load_Data(path)
    regress_model, onehot_model = load_model()
    predict_list = model_prediction(x_test, regress_model, onehot_model)
    result = predict_postprocessing(predict_list)

    return result