from django.apps import AppConfig
from .mmmil.utils.modelprediction import load_model, model_prediction
from .mmmil.utils.preprocessing import  load_Data
from .mmmil.utils.postprocessing import  predict_postprocessing

class MalocclusionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Malocclusion'
    # regress_model, onehot_model = load_model()


regress_model, onehot_model = load_model()


def malocclusion_result(path):
    x_test = load_Data(path)
    predict_list = model_prediction(x_test, regress_model, onehot_model)
    result = predict_postprocessing(predict_list)

    return result