'''
公共函数
'''
import logging
import numpy
from PyQt5.QtGui import QImage
import qimage2ndarray


logger = logging.getLogger(__name__)

def img_cv2qt(img_cv):
    ''' 将 OpenCV 格式的图像转换为 QImage
    '''
    # 获取图像维度
    dimen = len(img_cv.shape)
    if dimen > 3 or dimen < 2:
        return None
    # 图像数据格式
    if img_cv.dtype != numpy.dtype(numpy.uint8):
        return None
    # 转换
    if dimen == 3:
        qimg = qimage2ndarray.array2qimage(img_cv)
        qimg = qimg.convertToFormat(QImage.Format_RGB32)
    elif dimen == 2:
        qimg = qimage2ndarray.gray2qimage(img_cv)
        qimg = qimg.convertToFormat(QImage.Format_Grayscale8)
    else:
        qimg = None
    return qimg


def img_qt2cv(img_qt):
    ''' 将 QImage 格式的图像转换为 OpenCV 图像
    '''
    if img_qt.format() == QImage.Format_RGB32:
        return qimage2ndarray.rgb_view(img_qt)
    if img_qt.format() == QImage.Format_Grayscale8:
        return qimage2ndarray.byte_view(img_qt)[:, :, 0]
    return None
