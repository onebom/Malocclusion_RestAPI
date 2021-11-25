from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input
import numpy as np
import cv2 as cv
import os
from sklearn.utils import Bunch
params = Bunch(resize_wh = (1920, 1039),
               crop_row_range = (120, -40),
               crop_col_half = 1920//2)

def data_preprocessing(img_path):
    """
    img which has both left and right to respectively img with crop process
    """
    imgs = []
    data_info = os.path.basename(img_path)[:11]
    patient_id = data_info.split('_')[0]

    img = cv.imread(img_path)
    # img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    if img.size > (params.resize_wh[0] * params.resize_wh[1]):
        img = cv.resize(img, params.resize_wh, interpolation=cv.INTER_AREA)
    else:
        print(f'{img_path}: Image size should be larger than ({params.resize_wh[1]}, {params.resize_wh[0]}).')
        raise

    img = img[params.crop_row_range[0]:params.crop_row_range[1]]
    img_r = img[:, : params.crop_col_half]
    img_l = img[:, params.crop_col_half:]
    img_l = np.fliplr(img_l)
    img = np.concatenate((img_r, img_l), axis=2)

    imgs.append(img)
    imgs = np.asarray(imgs)

    return imgs


def generate_data_by_patient(data):
    if data.shape[-1] == 12:
        data = np.concatenate([data[..., :3], data[..., 3:6], data[..., 6:9], data[..., 9:]])
    elif data.shape[-1] == 6:
        data = np.concatenate([data[..., :3], data[..., 3:]])  # Right side,Left side !!!

    return data


def load_Data(img_path):
    """
    final preprocessing function
    return data shape: (2,229,229,3)
    """

    data = data_preprocessing(img_path)
    data = preprocess_input(data)

    x_test = generate_data_by_patient(data)

    return x_test
