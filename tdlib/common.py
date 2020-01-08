#!/usr/bin/env python

''' 共用函数
'''

from itertools import accumulate, repeat
from operator import add
from functools import reduce
from math import sqrt
import numpy as np
import cv2

def tdHighConstract(image, size=255):
    ''' 高反差保留
    Args:
        image 输入的灰度图像
        size  高斯滤波的模板大小
    '''
    guassblur_image = cv2.GaussianBlur(image, (size, size), 0)
    high_constrast_image = np.int64(image) - np.int64(guassblur_image)
    if high_constrast_image.min() < 0:
        high_constrast_image -= high_constrast_image.min()
    if high_constrast_image.max() != 255:
        high_constrast_image = cv2.convertScaleAbs(high_constrast_image, None, 255/high_constrast_image.max(), 0)
    return np.uint8(high_constrast_image)


def tdCalcHist(image, arg1=21, arg2=21, arg3=21, offset=0.10):
    ''' 提取两种字符形式
    黑底白字图和白底黑字图
    Args:
        image 输入的灰度图像
        offset 偏移
        arg1,arg2,arg3 同 cv2.bilateralFilter 中的参数位置
    '''
    # 计算基础灰度值（中值）
    hist_image = cv2.calcHist([image], [0], None, [256], [0, 255]).T.tolist()[0]
    medi = reduce(add, hist_image)/2
    accu = accumulate(hist_image, add)
    base_value = [i for i, v in enumerate(zip(accu, repeat(medi))) if v[0] > v[1]][0]

    # 计算黑底白字图
    hist_left = hist_image[:base_value]
    hist_accu_left = accumulate(hist_left, add)
    cutoff = reduce(add, hist_left)*offset  # for save
    threshold = [i for i, v in enumerate(zip(hist_accu_left, repeat(cutoff))) if v[0] > v[1]][0]
    left = np.int64(image.copy())
    left[left >= threshold] = threshold
    left = cv2.convertScaleAbs(left, 0, 255/left.max(), 0)
    left = cv2.bilateralFilter(left, arg1, arg2, arg3)

    # 计算白底黑字图
    hist_right = hist_image[base_value:]
    hist_accu_right = accumulate(hist_right, add)
    cutoff = reduce(add, hist_right)*(1-offset)  # for cut
    threshold = [i for i, v in enumerate(zip(hist_accu_right, repeat(cutoff))) if v[0] > v[1]][0] + base_value
    right = np.int64(image.copy())
    right[right <= threshold] = threshold
    right = right - right.min()
    right = cv2.convertScaleAbs(right, 0, 255/right.max(), 0)
    right = cv2.bilateralFilter(right, 21, 21, 21)
    return left, right


def tdCanny(image, sigma=0.33, offset=0.0):
    ''' 提取 Canny 边缘
    Args:
        image 输入的灰度图像
        sigma Canny上下阈值偏离均程度
        offset 均值偏离程度
    '''
    image = cv2.GaussianBlur(image, (5, 5), 0)
    v = np.median(image)
    if offset != 0:
        v += (image.max()-v)*offset if offset > 0 else (v-image.min())*(-offset)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    return cv2.Canny(image, lower, upper)


def tdSobel(image):
    ''' 计算图像梯度
    '''
    ddepth = cv2.CV_16S
    image = cv2.GaussianBlur(image, (5, 5), 0)
    gradx = cv2.Sobel(image, ddepth, 1, 0)
    abs_gradx = cv2.convertScaleAbs(gradx)
    grady = cv2.Sobel(image, ddepth, 0, 1)
    abs_grady = cv2.convertScaleAbs(grady)
    grad = cv2.addWeighted(abs_gradx, 0.5, abs_grady, 0.5, 0)
    return grad, gradx, abs_gradx, grady, abs_grady


def tdShape(image):
    ''' 图像锐化
    '''
    kel = np.array([[-1, -1, -1],
                    [-1, 9, -1],
                    [-1, -1, -1]])
    shape_image = cv2.filter2D(image, cv2.CV_8U, kel)
    shape_image = cv2.medianBlur(shape_image, 3)
    shape_image = cv2.bilateralFilter(shape_image, 21, 21, 21)
    return shape_image


def is_in_range(num, range_numlist):
    ''' 判断一个数书否在一个范围内
    '''
    return range_numlist[0] <= num <= range_numlist[1]


def crop_rect(img, region):
    ''' 旋转矩形裁剪
    '''
    rect = cv2.minAreaRect(region)
    if rect[1][1] > rect[1][0]:
        rect = (rect[0], (rect[1][1], rect[1][0]), rect[2]+90)

    # get the parameter of the small rectangle
    center, size, angle = rect[0], rect[1], rect[2]
    center, size = tuple(map(int, center)), tuple(map(int, size))

    # get row and col num in img
    height, width = img.shape[0], img.shape[1]

    # calculate the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1)
    # rotate the original image
    img_rot = cv2.warpAffine(img, M, (width, height))

    # now rotated rectangle becomes vertical and we crop it
    img_crop = cv2.getRectSubPix(img_rot, size, center)

    return img_crop, img_rot


def zoomImage(img, total_pixels):
    ''' 将图像等比缩放到一个指定的像素量
    Args：
        img 输入的灰度图像
        total_pixels 缩放后的像素量
    Return：
        img 缩放后的图像
    '''
    zoom_level = sqrt(img.shape[0] * img.shape[1] / total_pixels)
    return cv2.resize(img, (int(img.shape[1]/zoom_level), int(img.shape[0]/zoom_level)))
    