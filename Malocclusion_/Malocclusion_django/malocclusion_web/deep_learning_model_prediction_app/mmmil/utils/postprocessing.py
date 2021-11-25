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
    r2 = np.round(r.copy())  # 반올림
    r2[r2 < -1] = -1
    r2[r2 > 1] = 1


    l2 = np.round(l.copy())
    l2[l2 < -1] = -1
    l2[l2 > 1] = 1

    return r, l


def one_hot_predict(prediction):

    prediction_class_r = prediction[0]  # Right
    prediction_class_l = prediction[1]  # left

    r = prediction_class_r.copy()
    l = prediction_class_l.copy()

    # onehot value score # 반올림
    r = r.tolist()
    r2 = np.round(r, 3)
    r3 = np.argmax(r2, axis=0) + 1

    l = l.tolist()
    l2 = np.round(l, 3)
    l3 = np.argmax(l2, axis=0) + 1

    return r2, l2, r3, l3


def predict_postprocessing(result):
    inference_result = {}
    regress_r, regress_l = regression_predict(result[:2])
    onehot_r, onehot_l, class_r, class_l = one_hot_predict(result[2:])

    inference_result["Right_regression_predict_class"] = regress_r
    inference_result["Left_regression_predict_class"] = regress_l
    inference_result["Right_onehot_predict_class"] = onehot_r
    inference_result["Left_onehot_predict_class"] = onehot_l
    inference_result["Right_only_class"] = class_r
    inference_result["Left_only_class"] = class_l

    return inference_result


def malocclusion_result(path, mode_selection):
    x_test = load_Data(path)
    regress_model, onehot_model = load_model()
    predict_list = model_prediction(x_test, regress_model, onehot_model)
    if mode_selection = "r":
        # print only regerssion score
        result = [predict_postprocessing(predict_list)["Right_regression_predict_class"],predict_postprocessing(predict_list)["Left_regression_predict_class"]]
    
    elif mode_selection = "o":
        # print only one-hot class percentage
        result = [predict_postprocessing(predict_list)["Right_onehot_predict_class"],predict_postprocessing(predict_list)["Left_onehot_predict_class"]]
    
    elif mode_selection = "c":
        # print only image class
        result = [predict_postprocessing(predict_list)["Right_only_class"],predict_postprocessing(predict_list)["Left_only_class"]]
    
    elif mode_selection = "a":
        # print all
        result = predict_postprocessing(predict_list)
    
    else:
        print("error")
    
    return result

#------"help"-----------
# class는 1,2,3으로 나뉜다. 
# calss1은 정상교합이며, class2와 class3은 각각 상악 돌출, 하악돌출을 의미한다. 
# option "p"는 data의 regerssion score를 출력한다. 
# regression score는 -0.5와 0.5를 기준으로 -0.5이하의 경우 class3, 0.5이상의 경우 class2를 나타내고, -0.5~0.5는 정상범주의 class1을 나타낸다. 
# option "o"의 경우, predict한 data의 class 별 classification percentage를 one-hot encoding 형식으로 표현했다. 각 리스트의 위치는 차례로 class1, class2, class3을 의미한다. 
# option "c"는 data의 predicted class를 정수로 나타낸다. 
# option "a"는 위의 information을 모두 출력한다. 
#------------------------
