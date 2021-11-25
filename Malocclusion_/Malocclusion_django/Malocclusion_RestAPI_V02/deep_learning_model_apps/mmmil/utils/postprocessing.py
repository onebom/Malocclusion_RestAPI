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
    r = np.round(r, 3)  # 반올림
    l = np.round(l, 3)


    return r, l


def one_hot_predict(prediction):

    prediction_class_r = prediction[0]  # Right
    prediction_class_l = prediction[1]  # left

    r = prediction_class_r.copy()
    l = prediction_class_l.copy()

    # onehot value score # 반올림
    r = r.tolist()
    r_class = np.argmax(r, axis=-1) + 1
    r_predict=np.round(r, 3)

    l = l.tolist()
    l_class = np.argmax(l, axis=-1) + 1
    l_predict = np.round(l, 3)

    return r_class, l_class, r_predict, l_predict



def predict_postprocessing(result):
    inference_result = {}
    regress_r, regress_l = regression_predict(result[:2])
    r_class, l_class, r_predict, l_predict  = one_hot_predict(result[2:])

    inference_result["Right_class"] = r_class[0]
    inference_result["Left_class"] = l_class[0]
    inference_result["Right_onehot_predict"] = r_predict[0]
    inference_result["Left_onehot_predict"] = l_predict[0]
    inference_result["Right_regression_score"] = regress_r[0]
    inference_result["Left_regression_score"] = regress_l[0]

    return inference_result


def malocclusion_result(path):
    x_test = load_Data(path)
    regress_model, onehot_model = load_model()
    predict_list = model_prediction(x_test, regress_model, onehot_model)
    result = predict_postprocessing(predict_list)

    return result