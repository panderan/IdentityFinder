#!/usr/bin/env python

'''
@package text_detection

@file preprocessing.py
基本预处理

@author panderan@163.com

'''
import logging
from math import sqrt
from enum import Enum
import cv2
import tdlib.common as tcomm
from conf.config import TdPrepConfigKeys


logger = logging.getLogger(__name__)


class TdPreprocessingDebugData:
    ''' 预处理中间数据
    '''
    def __init__(self):
        self.enable = False
        self.data = []

    def addImage(self, name, image):
        ''' 添加中间结果
        '''
        if self.enable:
            self.data.append((name, image.copy()))
        return self

    def setEnable(self, flag):
        ''' 设置是否启用
        '''
        self.enable = bool(flag)
        return self

    def clear(self):
        ''' 清楚所有数据
        '''
        self.data.clear()
        return self


class TdPreprocessing:
    ''' 图像预处理
    '''
    def __init__(self, rgb_image=None, total_pixels=400000):
        self.total_pixels = total_pixels
        self.rgb_image = rgb_image
        self.prep_gray = None
        self.prep_red = None
        self.prep_green = None
        self.prep_blue = None
        self.config = {TdPrepConfigKeys.TOTAL_PIXELS:total_pixels,
                       TdPrepConfigKeys.BILATERAL:[21, 21, 21],
                       TdPrepConfigKeys.GAUSS_SIZE: 255,
                       TdPrepConfigKeys.OFFSET: 10}
        self.debug = TdPreprocessingDebugData()

        return

    def doPreprocessing(self, image, config=None):
        ''' 图像预处理
        '''
        self.setConfig(config)
        # 双边滤波
        image = cv2.bilateralFilter(image, self.config[TdPrepConfigKeys.BILATERAL][0], \
                                           self.config[TdPrepConfigKeys.BILATERAL][1], \
                                           self.config[TdPrepConfigKeys.BILATERAL][2])
        self.debug.addImage("bilateral", image)
        # 高反差保留
        image = tcomm.tdHighConstract(image, self.config[TdPrepConfigKeys.GAUSS_SIZE])
        self.debug.addImage("high constract", image)
        # 分离字体形式
        blackchars, brightchars = tcomm.tdCalcHist(image, self.config[TdPrepConfigKeys.BILATERAL][0], \
                                           self.config[TdPrepConfigKeys.BILATERAL][1], \
                                           self.config[TdPrepConfigKeys.BILATERAL][2], \
                                           self.config[TdPrepConfigKeys.OFFSET])

        self.debug.addImage("black chars", blackchars).addImage("bright chars", brightchars)
        return blackchars, brightchars

    def __setConfigItem(self, key, config):
        ''' 设置配置文件单个项目
        '''
        val = config.get(key, None)
        if val is not None:
            if key is TdPrepConfigKeys.DEBUG:
                self.debug.setEnable(val)
            else:
                self.config[key] = val
        return

    def setConfig(self, config):
        ''' 设置配置文件
        '''
        if config is None:
            return
        self.__setConfigItem(TdPrepConfigKeys.TOTAL_PIXELS, config)
        self.__setConfigItem(TdPrepConfigKeys.BILATERAL, config)
        self.__setConfigItem(TdPrepConfigKeys.GAUSS_SIZE, config)
        self.__setConfigItem(TdPrepConfigKeys.OFFSET, config)
        self.__setConfigItem(TdPrepConfigKeys.DEBUG, config)
        return

    def printParams(self, msg):
        ''' 打印当前参数
        '''
        msg = "%s,%s" %(msg, self.config)
        logger.info(msg)

    @property
    def rgb_image(self):
        ''' 图像输入
        '''
        return self.__rgb_image
    @rgb_image.setter
    def rgb_image(self, val):
        if val is None:
            return
        # 缩放图像并获得宽高
        zoom_level = sqrt(val.shape[0] * val.shape[1] / self.total_pixels)
        self.__rgb_image = cv2.resize(val, (int(val.shape[1]/zoom_level), int(val.shape[0]/zoom_level)))
        self.height, self.width = self.__rgb_image.shape[:2] #高，宽=行，列
        # 获得多种灰度图
        self.gray = cv2.cvtColor(self.__rgb_image, cv2.COLOR_RGB2GRAY)
        self.red = self.__rgb_image[:, :, 0]
        self.green = self.__rgb_image[:, :, 1]
        self.blue = self.__rgb_image[:, :, 2]
        return

    @property
    def ret_gray(self):
        ''' 获取灰度图像的预处理结果
        '''
        self.printParams("Do preprocessing Gray")
        self.debug.clear().addImage("Gray", self.gray)
        blackchars, brightchars = self.doPreprocessing(self.gray)
        return self.gray, blackchars, brightchars
    @ret_gray.setter
    def ret_gray(self, val):
        pass

    @property
    def ret_red(self):
        ''' 获取红色通道图像的预处理结果
        '''
        self.printParams("Do preprocessing Red Channel")
        self.debug.clear().addImage("Red", self.red)
        blackchars, brightchars = self.doPreprocessing(self.red)
        return self.red, blackchars, brightchars
    @ret_red.setter
    def ret_red(self, val):
        pass

    @property
    def ret_green(self):
        ''' 获取绿色通道图像的预处理结果
        '''
        self.printParams("Do preprocessing Red Channel")
        self.debug.clear().addImage("Green", self.green)
        blackchars, brightchars = self.doPreprocessing(self.green)
        return self.green, blackchars, brightchars
    @ret_green.setter
    def ret_green(self, val):
        pass

    @property
    def ret_blue(self):
        ''' 获取蓝色通道图像的预处理结果
        '''
        self.printParams("Do preprocessing Red Channel")
        self.debug.clear().addImage("Blue", self.blue)
        blackchars, brightchars = self.doPreprocessing(self.blue)
        return self.blue, blackchars, brightchars
    @ret_blue.setter
    def ret_blue(self, val):
        pass
