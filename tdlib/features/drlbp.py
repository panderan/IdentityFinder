#!/usr/bin/env python

'''
# 提取选区 DLBP 特征类
'''
import os
import math
import re
import numpy as np
import cv2
from skimage import feature


def takeFirst(elem):
    ''' 返回二元组的第一个元素
    '''
    return elem[0]


class TdFeatureTrainingDRLBP:
    ''' DLBP 特征训练类
        用以获取参数 K 的大小
    '''
    def __init__(self, points=8, radius=1, occupied=0.9, k_c=3):
        ''' 构造函数
        Args:
            points 采样点个数
            radius 采样范围半径
            occupied 主要特征占有率
        '''
        self.number_points = points
        self.radius = radius
        self.occupied = occupied
        self.k = 0
        self.k_c = k_c

    def training_k(self, dirpath):
        ''' 见 DLBP Algorithm 2
        Args:
            dirpath 包含训练样本的目录路径
        Return:
            k 主要LBP编码数量
            vtrs LBP特征向量
            labels 标签向量
        '''
        k, vtrs = 0.0, []
        files = os.listdir(dirpath)
        for fname in files:
            fpath = dirpath + '/' + fname
            if not os.path.isfile(fpath):
                continue
            if re.search('jpg$|png$|JPG$|PNG$', fname) is None:
                continue
            i, x = self.calc_k(fpath)
            k += i
            vtrs.append((x, 1 if fname[-5] == 'Y' else 0))
        k = k / len(files)
        return k, vtrs

    def get_lbp(self, gray_image):
        ''' 计算 lbp 特征
        '''
        lbp_image = feature.local_binary_pattern(gray_image, self.number_points, self.radius, method="ror")
        hist_size = int(math.pow(2, self.number_points))
        hist_range = [0, hist_size-1]
        hist = np.histogram(np.int64(lbp_image), hist_size, hist_range)[0].tolist()
        hist.sort(reverse=True)
        return hist

    def calc_k(self, filename):
        ''' 见 DLBP Algorithm 1
        Args:
            filename 样本图像的文件路径
        Return:
            i, hist
        '''
        # 提取 gimg 文件 lbp
        gimg = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        hist = self.get_lbp(gimg)

        # 计算主要LBP值
        acc, total = 0, sum(hist)
        for i, item in enumerate(hist):
            acc += item
            if acc/total > self.occupied:
                return (i, hist)
        return None

    @property
    def k(self):
        ''' 获取k值
        '''
        return self._k + self.k_c
    @k.setter
    def k(self, val):
        self._k = val

class TdFeatureDRLBP(TdFeatureTrainingDRLBP):
    ''' DLBP 特征提取类
        DLBP 特征提取前，需要先训练参数 k
    '''
    def __init__(self, points=8, radius=1, occupied=0.85, k_c=3):
        super().__init__(points, radius, occupied, k_c)

    def getLBPImage(self, gimg):
        ''' 获取 DLBP 图像
        Args:
            gimg 输入的待提取特征的图像
        Return:
            LBP 特征图

        '''
        lbp = feature.local_binary_pattern(gimg, self.number_points, self.radius, method="ror")
        return lbp

    def getDRLBP(self, gimg):
        ''' 获取 DLBP 特征
        Args:
            gimg 输入的待提取特征的图像
        Return:
            DRLBP 特征向量
        '''
        if self.k == 0:
            print("DLBP need training first\n")
            return None

        hist = self.get_lbp(gimg)
        return np.array(hist[:self.k])
