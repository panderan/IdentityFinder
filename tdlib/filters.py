#!/usr/bin/env python

'''
    @package text_detection

    @file filter.py
    几何条件过滤类

    @author panderan@163.com
'''

import logging
import math
from enum import Enum
import cv2
import numpy as np
from conf.config import TdFilterConfigKey, TdFilterCheckType


logger = logging.getLogger(__name__)



class TdFilterDebugData:
    ''' Debug 数据
    '''
    def __init__(self):
        self.data = []
        self.enable = False

    def initDebugData(self):
        ''' 初始化 Debug 数据
        '''
        self.data = {"area":None,
                     "width":None,
                     "height":None,
                     "perimeter":None,
                     "aspect_ratio":None,
                     "occupation_ratio":None,
                     "compactness":None}

    def setEnable(self, flag):
        ''' 注释
        '''
        self.enable = bool(flag)

    def fillDebugData(self, key, value, lim):
        ''' 填充 Debug 数据
        '''
        if self.enable:
            self.data[key] = {"value":value, "lim":lim, "result":True}

    def markDebugDataResult(self, key, flag=False):
        ''' 修改 Debug 数据中的 Result 值
        '''
        if self.enable and self.data[key] is not None:
            self.data[key]['result'] = flag


class TdFilter:
    ''' 简单特征过滤
    '''
    def __init__(self, gray_image=None):
        self.flag = None
        self.area_lim = 0
        self.perimeter_lim = [12, 200]
        self.aspect_ratio_lim = [1.0, 15.0]
        self.aspect_ratio_gt1 = True
        self.occupation_lim = [0.15, 0.90]
        self.compactness_lim = [3e-3, 1e-1]
        self.width_lim = [0, 800]
        self.height_lim = [0, 800]

        self.swt = None
        self.swt_total_cnt = [0, 30]
        self.swt_mode = [1.5, 999.0]
        self.swt_mode_cnt = 3
        self.swt_mean = [2.0, 5.0]
        self.swt_std = [0.5, 2.5]
        self.swt_val_range = [0, 255]

        self.canny_image = None
        self.gray_image = gray_image
        self.debug = TdFilterDebugData()

    def validate(self, region, bbox):
        ''' 验证单个选区是否满足条件
        Args:
            region: MSER 提取的选区所有像素点列表
            bbox: MSER 提取的选区外接矩形 BoundingBox
        Returns:
            True 满足
            False 不满足
        '''
        self.debug.initDebugData()

        # 面积过滤
        if  TdFilterCheckType.AREA in self.flag:
            self.debug.fillDebugData("area", bbox[2]*bbox[3], self.area_lim)
            if bbox[2]*bbox[3] < self.area_lim:
                self.debug.markDebugDataResult("area", False)
                return False

        # 长宽度过滤
        if  TdFilterCheckType.WIDTH in self.flag:
            self.debug.fillDebugData("width", bbox[2], self.width_lim)
            if bbox[2] < self.width_lim[0] or bbox[2] > self.width_lim[1]:
                self.debug.markDebugDataResult("width", False)
                return False

        if  TdFilterCheckType.HEIGHT in self.flag:
            self.debug.fillDebugData("height", bbox[3], self.height_lim)
            if bbox[3] < self.height_lim[0] or bbox[3] > self.height_lim[1]:
                self.debug.markDebugDataResult("height", False)
                return False

        # 周长
        if  TdFilterCheckType.PERIMETER in self.flag:
            retval = self.getPerimeter(bbox)
            self.debug.fillDebugData("perimeter", retval, self.perimeter_lim)
            if retval < self.perimeter_lim[0] or retval > self.perimeter_lim[1]:
                self.debug.markDebugDataResult("perimeter", False)
                return False

        # 横纵比
        if  TdFilterCheckType.ASPECTRATIO in self.flag:
            retval = self.getAspectRatio(region)
            self.debug.fillDebugData("aspect_ratio", retval, self.aspect_ratio_lim)
            if retval < self.aspect_ratio_lim[0] or retval > self.aspect_ratio_lim[1]:
                self.debug.markDebugDataResult("aspect_ratio", False)
                return False

        # 占用率
        if  TdFilterCheckType.OCCUPIEDRATIO in self.flag:
            retval = self.getOccurpiedRatio(region, bbox)
            self.debug.fillDebugData("occupation_ratio", retval, self.occupation_lim)
            if retval < self.occupation_lim[0] or retval > self.occupation_lim[1]:
                self.debug.markDebugDataResult("occupation_ratio", False)
                return False

        # 紧密度
        if  TdFilterCheckType.COMPACTNESS in self.flag:
            retval = self.getCompactness(region, bbox)
            self.debug.fillDebugData("compactness", retval, self.compactness_lim)
            if retval < self.compactness_lim[0] or retval > self.compactness_lim[1]:
                self.debug.markDebugDataResult("compactness", False)
                return False
        return True

    def getRealArea(self, region):
        ''' 获取选区面积
        '''
        return len(region)

    def getPerimeter(self, bbox):
        ''' 获取选区周长
        '''
        tmp = self.canny_image[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]]
        return len(np.where(tmp != 0)[0])

    def getAspectRatio(self, region):
        ''' 获取选区横纵比
        '''
        box = np.int32(cv2.boxPoints(cv2.minAreaRect(region)))
        p0 = np.array(box[-1])
        p1 = np.array(box[0])
        p2 = np.array(box[1])
        l1 = p1-p0
        l2 = p1-p2
        h = l1
        w = l2

        if (l1[0] == 0 and l1[1] == 0)\
            or (l2[0] == 0 and l2[1] == 0):
            return 9999

        angle = math.asin(l1[1]/math.hypot(l1[0], l1[1]))
        if angle > -math.pi/4 and angle < math.pi/4:
            w = l1
            h = l2

        dw = math.hypot(w[0], w[1])+1
        dh = math.hypot(h[0], h[1])+1

        ratio = dw/dh
        if self.aspect_ratio_gt1 and ratio < 1.0:
            ratio = 1.0 / ratio

        return ratio

    def getOccurpiedRatio(self, region, bbox):
        ''' 获取选区占有率
        '''
        return float(self.getRealArea(region)) / (float(bbox[2]) * float(bbox[3]))

    def getCompactness(self, region, bbox):
        ''' 获取选区紧密度
        '''
        if self.getPerimeter(bbox) > 0:
            return float(self.getRealArea(region)) / float(self.getPerimeter(bbox)**2)
        return 0

    def __setConfigItem(self, keystr, config):
        ''' 设置单个参数
        '''
        try:
            if keystr is TdFilterConfigKey.FLAG:
                self.flag = config[TdFilterConfigKey.FLAG]
            elif keystr is TdFilterConfigKey.AREA_LIM:
                self.area_lim = config[TdFilterConfigKey.AREA_LIM]
            elif keystr is TdFilterConfigKey.PERIMETER_LIM:
                self.perimeter_lim = config[TdFilterConfigKey.PERIMETER_LIM]
            elif keystr is TdFilterConfigKey.ASPECT_RATIO_LIM:
                self.aspect_ratio_lim = config[TdFilterConfigKey.ASPECT_RATIO_LIM]
            elif keystr is TdFilterConfigKey.ASPECT_RATIO_GT1:
                self.aspect_ratio_gt1 = config[TdFilterConfigKey.ASPECT_RATIO_GT1]
            elif keystr is TdFilterConfigKey.OCCUPATION_LIM:
                self.occupation_lim = config[TdFilterConfigKey.OCCUPATION_LIM]
            elif keystr is TdFilterConfigKey.COMPACTNESS_LIM:
                self.compactness_lim = config[TdFilterConfigKey.COMPACTNESS_LIM]
            elif keystr is TdFilterConfigKey.WIDTH_LIM:
                self.width_lim = config[TdFilterConfigKey.WIDTH_LIM]
            elif keystr is TdFilterConfigKey.HEIGHT_LIM:
                self.height_lim = config[TdFilterConfigKey.HEIGHT_LIM]
            else:
                pass
        except KeyError:
            pass
        return None

    def setConfig(self, config):
        ''' 设置参数
        '''
        self.__setConfigItem(TdFilterConfigKey.FLAG, config)
        self.__setConfigItem(TdFilterConfigKey.AREA_LIM, config)
        self.__setConfigItem(TdFilterConfigKey.PERIMETER_LIM, config)
        self.__setConfigItem(TdFilterConfigKey.ASPECT_RATIO_LIM, config)
        self.__setConfigItem(TdFilterConfigKey.ASPECT_RATIO_GT1, config)
        self.__setConfigItem(TdFilterConfigKey.OCCUPATION_LIM, config)
        self.__setConfigItem(TdFilterConfigKey.COMPACTNESS_LIM, config)
        self.__setConfigItem(TdFilterConfigKey.WIDTH_LIM, config)
        self.__setConfigItem(TdFilterConfigKey.HEIGHT_LIM, config)
        self.printParams()
        return self

    def printParams(self):
        ''' 打印当前参数
        '''
        params = {TdFilterConfigKey.FLAG.name: self.flag,
                  TdFilterConfigKey.AREA_LIM.name: self.area_lim,
                  TdFilterConfigKey.PERIMETER_LIM.name: self.perimeter_lim,
                  TdFilterConfigKey.ASPECT_RATIO_LIM.name: self.aspect_ratio_lim,
                  TdFilterConfigKey.ASPECT_RATIO_GT1.name: self.aspect_ratio_gt1,
                  TdFilterConfigKey.OCCUPATION_LIM.name: self.occupation_lim,
                  TdFilterConfigKey.COMPACTNESS_LIM.name: self.compactness_lim,
                  TdFilterConfigKey.WIDTH_LIM.name: self.width_lim,
                  TdFilterConfigKey.HEIGHT_LIM.name: self.height_lim}
        msg = "Filter Params %s" % params
        logger.info(msg)

    @property
    def gray_image(self):
        ''' 灰度图像
        '''
        return self.__gray_image
    @gray_image.setter
    def gray_image(self, val):
        if val is not None:
            self.__gray_image = val
            v = np.median(self.__gray_image)
            lower = int(max(0, (1.0 - 0.33) * v))
            upper = int(min(255, (1.0 + 0.33) * v))
            self.canny_image = cv2.Canny(self.__gray_image, lower, upper)
        else:
            self.__gray_image = None
            self.canny_image = None

    def validateBoxPoints(self, pbox):
        ''' 验证单个选区是否满足条件
        Args:
            region: MSER 提取的选区所有像素点列表
            pbox: 矩形角点 box points
        Returns:
            True 满足
            False 不满足
        '''
        robox = cv2.minAreaRect(pbox)
        return self.validateRoRect(robox)

    def validateRoRect(self, robox):
        ''' 验证单个选区是否满足条件
        Args:
            region: MSER 提取的选区所有像素点列表
            robox: 矩形角点 rotate box
        Returns:
            True 满足
            False 不满足
        '''
        cntr_x, cntr_y = robox[0]
        width, height = robox[1]
        bbox = np.int32((cntr_x-width/2, cntr_y-height/2, width, height))
        target_check_type = [TdFilterCheckType.AREA,
                             TdFilterCheckType.WIDTH,
                             TdFilterCheckType.HEIGHT,
                             TdFilterCheckType.PERIMETER]
        new_flag = [v for v in self.flag if v in target_check_type]
        self.flag = new_flag
        return self.validate(None, bbox)
