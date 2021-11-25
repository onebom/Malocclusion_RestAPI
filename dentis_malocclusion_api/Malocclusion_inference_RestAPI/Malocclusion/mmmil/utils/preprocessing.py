"""Utilis of preprocessing and normalization for data """
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input
import numpy as np
import cv2 as cv
import os
from sklearn.utils import Bunch
params = Bunch(resize_wh = (1920, 1039),
               crop_row_range = (120, -40),
               crop_col_half = 1920//2)

def data_preprocessing(img_path):
    """preprocessing image data.
    
    This function load image and execute cropping&resize function 

    Args:
      img_path: path of img which has both left and right. 
    
    Returns:
      imgs: numpy data which consisting of two image divided right and left
        from origin image by croping process.
        return data shape has to be (sampel_num, width, height, 6).
        The first 3 on channel axis means Right data.
        The rest is the left data
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

    # image seperated into half about the width
    img = img[params.crop_row_range[0]:params.crop_row_range[1]]
    img_r = img[:, : params.crop_col_half]
    img_l = img[:, params.crop_col_half:]
    img_l = np.fliplr(img_l)
    img = np.concatenate((img_r, img_l), axis=2)

    imgs.append(img)
    imgs = np.asarray(imgs)

    return imgs


def generate_data_by_patient(data):
    """seprating combined numpy data by channel axis.

    This function conversion channel based(last dimension) connection for right and left data 
    into sample num based(first dimension) connection
    
    Args:
      data: numpy data connected to the right data and left data on the channel axis.
        data channel must be 6.

    Returns:
      data: numpy data that connects right and left data continuously on the sample num axis
        (then, shape is to be (sample_num*2, width, height, 3))

    """
    if data.shape[-1] == 12:
        data = np.concatenate([data[..., :3], data[..., 3:6], data[..., 6:9], data[..., 9:]])
    elif data.shape[-1] == 6:
        data = np.concatenate([data[..., :3], data[..., 3:]])  # Right side,Left side !!!

    return data


def load_Data(img_path):
    """final preprocessing function 
    
    Args:
      img_path: path of img which has both left and right. 
    
    Returns:
      x_test: numpy data set that has undergone preprocessing and normalization.
        one of x_test data's shape has to be (2,229,229,3)
        data set has a value between -1 and 1.
    """

    data = data_preprocessing(img_path)

    # normalization into -1 and 1
    data = preprocess_input(data)

    x_test = generate_data_by_patient(data)

    return x_test
