#!/usr/bin/env python

''' 利用特征再判断
'''
from enum import Enum
from pathlib import Path
import yaml
import joblib
from tdlib.features.drlbp import TdFeatureDRLBP
from tdlib.common import zoomImage

class SamplePreMethod(Enum):
    ''' 样本前处理方法
    '''
    EQU_SCALE = 0
    MAX = 1

class TdSVC:
    ''' 分类
    '''
    def __init__(self):
        self.trained = False
        self.drlbp = None
        self.svc = None
        self.method = None
        self.quantity = None

    def init(self, mconf_path):
        ''' 初始化 SVC 模型
        '''
        if mconf_path is None or not Path(mconf_path).exists():
            return False
        with open(mconf_path, "r") as f:
            mconf = yaml.load(f, Loader=yaml.FullLoader)
        self.svc = joblib.load(mconf['mpath'])
        drlbp_point, drlbp_radius, drlbp_occupied, drlbp_k_c = mconf['drlbp']
        self.drlbp = TdFeatureDRLBP(drlbp_point, drlbp_radius, drlbp_occupied, drlbp_k_c)
        self.drlbp.k = mconf['k']
        options = {"equScale": SamplePreMethod.EQU_SCALE}
        self.method = options.get(mconf['method'], SamplePreMethod.EQU_SCALE)
        self.quantity = mconf['quantity']
        return True

    def predict(self, gimg):
        ''' 预测
        '''
        if self.svc is None:
            return None
        if self.method is SamplePreMethod.EQU_SCALE:
            gimg = zoomImage(gimg, self.quantity)
        ft = self.drlbp.getDRLBP(gimg)
        pred = self.svc.predict(ft.reshape(1, -1))
        if ft is None or pred is None:
            return None
        return bool(pred[0])
