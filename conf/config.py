#!/usr/bin/env python

''' 读取配置文件
'''

import sys
from enum import Enum
import yaml


class TdPrepConfigKeys(Enum):
    ''' 预处理配置的Keys
    '''
    TOTAL_PIXELS = 0    # 总像素量
    BILATERAL = 1       # 双边滤波参数
    GAUSS_SIZE = 2      # 高斯模板大小
    OFFSET = 3          # 字体类型偏移
    DEBUG = 4
    DEBUG_SOURCE = 5

class TdPrepConfig:
    ''' 预处理参数
    '''
    def __init__(self, yaml_config=None):
        self.prep_configs = {
            TdPrepConfigKeys.TOTAL_PIXELS: 0,
            TdPrepConfigKeys.BILATERAL: [21, 21, 21],
            TdPrepConfigKeys.GAUSS_SIZE: 255,
            TdPrepConfigKeys.OFFSET: 10
        }
        if yaml_config is not None:
            self.setConfig(yaml_config)

    def setConfig(self, configs):
        ''' 设置配置文件
        '''
        yaml_data = configs['prep']
        TdPrepConfig.setConfigItem(self, TdPrepConfigKeys.TOTAL_PIXELS, int(yaml_data.get('total_pixels', 0)))
        TdPrepConfig.setConfigItem(self, TdPrepConfigKeys.BILATERAL, yaml_data.get('bilateral', 0.0))
        TdPrepConfig.setConfigItem(self, TdPrepConfigKeys.GAUSS_SIZE, int(yaml_data.get('gauss_size', 0)))
        TdPrepConfig.setConfigItem(self, TdPrepConfigKeys.OFFSET, float(yaml_data.get('offset', 0)))

    def setConfigItem(self, conf_key, value):
        ''' 设置单个参数
        '''
        if conf_key is not None:
            self.prep_configs[conf_key] = value
            return True
        return False

    def getConfig(self):
        ''' 获取配置
        '''
        return self.prep_configs


class TdExtractConfigKey(Enum):
    ''' Extract Keys
    '''
    DELTA = 0
    SRCS = 1
    AREA_MAX = 2
    AREA_MIN = 3
    VARIATION = 4
    DIRECTION = 5
    VERBOSE = 6
    VERBOSE_MORPH = 7

class TdExtractConfig:
    ''' 连通域提取参数
    '''
    def __init__(self):
        self.ext_configs = {
            TdExtractConfigKey.DELTA: 0,
            TdExtractConfigKey.SRCS: ['Gray.Both'],
            TdExtractConfigKey.AREA_MAX: 0,
            TdExtractConfigKey.AREA_MIN: 0,
            TdExtractConfigKey.VARIATION: 0.0,
            TdExtractConfigKey.DIRECTION: None,
            TdExtractConfigKey.VERBOSE: False,
            TdExtractConfigKey.VERBOSE_MORPH: False,

        }

    def setConfig(self, configs):
        ''' 设置参数
        '''
        yaml_data = configs['extract']
        TdExtractConfig.setConfigItem(self, TdExtractConfigKey.DELTA, int(yaml_data.get('delta', 0)))
        TdExtractConfig.setConfigItem(self, TdExtractConfigKey.SRCS, yaml_data.get('srcs', ["Gray.Both"]))
        TdExtractConfig.setConfigItem(self, TdExtractConfigKey.AREA_MIN, int(yaml_data.get('area_lim', [0, 0])[0]))
        TdExtractConfig.setConfigItem(self, TdExtractConfigKey.AREA_MAX, int(yaml_data.get('area_lim', [0, 0])[1]))
        TdExtractConfig.setConfigItem(self, TdExtractConfigKey.VARIATION, float(yaml_data.get('variation', 0.0)))

    def setConfigItem(self, key, value):
        ''' 设置单个参数
        '''
        if self.ext_configs.get(key, None) is not None:
            self.ext_configs[key] = value
            return True
        return False

    def getConfig(self):
        ''' 获取配置参数
        '''
        return self.ext_configs



class MergingStrategy(Enum):
    ''' 策略标识
    '''
    HORIZON = 1
    VERTICAL = 2
    OPTIMAL = 3

class MergingPositionRatio(Enum):
    ''' 位置比率类型
    '''
    IDCARD = 1
    CAR_PLATE = 2
    CONSTANT = 3

class TdMergeTLConfigKey(Enum):
    ''' TdMergeTLConfigKey
    '''
    COMBINED_AREA_SIZE_LIM = 0
    COMBINED_ASPECT_RATIO_LIM = 1
    OVERLAP_RATIO = 2
    DISTANCE = 3
    STRATEGY = 4
    SCOPE_LIM = 5
    POSITION_RATIO = 6
    POSITION_RATIO_CONSTANT = 7
    VERBOSE = 8

class TdMergeTLConfig:
    ''' 文本行合并参数
    '''
    def __init__(self):
        self.meg_configs = {
            TdMergeTLConfigKey.COMBINED_AREA_SIZE_LIM: 0,
            TdMergeTLConfigKey.COMBINED_ASPECT_RATIO_LIM: [0.0, 0.0],
            TdMergeTLConfigKey.OVERLAP_RATIO: 0.25,
            TdMergeTLConfigKey.DISTANCE: 0.0,
            TdMergeTLConfigKey.STRATEGY: MergingStrategy.HORIZON,
            TdMergeTLConfigKey.SCOPE_LIM: 0,
            TdMergeTLConfigKey.POSITION_RATIO: MergingPositionRatio.CONSTANT,
            TdMergeTLConfigKey.POSITION_RATIO_CONSTANT: 0.0,
            TdMergeTLConfigKey.VERBOSE: False
        }

    def setConfig(self, configs):
        ''' 设置配置
        '''
        yaml_data = configs['merge']
        TdMergeTLConfig.setConfigItem(self, TdMergeTLConfigKey.COMBINED_AREA_SIZE_LIM, int(yaml_data.get('combined_area_size_lim', 0)))
        TdMergeTLConfig.setConfigItem(self, TdMergeTLConfigKey.COMBINED_ASPECT_RATIO_LIM, [float(v) for v in yaml_data.get('combined_aspect_ratio_lim', [0.0, 0.0])])
        TdMergeTLConfig.setConfigItem(self, TdMergeTLConfigKey.OVERLAP_RATIO, float(yaml_data.get('overlap_ratio', 0)))
        TdMergeTLConfig.setConfigItem(self, TdMergeTLConfigKey.DISTANCE, float(yaml_data.get('distance', 0)))
        TdMergeTLConfig.setConfigItem(self, TdMergeTLConfigKey.STRATEGY, yaml_data.get('strategy', "horizon"))
        TdMergeTLConfig.setConfigItem(self, TdMergeTLConfigKey.SCOPE_LIM, yaml_data.get('scope_lim', 0))
        TdMergeTLConfig.setConfigItem(self, TdMergeTLConfigKey.POSITION_RATIO, yaml_data.get('position_ratio', ("constant", 0.6)))

    def setConfigItem(self, key, value):
        ''' 设置单个参数
        '''
        if self.meg_configs.get(key, None) is not None:
            if key is TdMergeTLConfigKey.STRATEGY:
                options = {"horizon": MergingStrategy.HORIZON,
                           "vertical": MergingStrategy.VERTICAL
                          }
                value = options.get(value, MergingStrategy.OPTIMAL)
            if key is TdMergeTLConfigKey.POSITION_RATIO:
                options = {"ID Card": MergingPositionRatio.IDCARD,
                           "Car Plate": MergingPositionRatio.CAR_PLATE,
                           "Constant": MergingPositionRatio.CONSTANT
                          }
                self.meg_configs[TdMergeTLConfigKey.POSITION_RATIO_CONSTANT] = value[-1]
                value = options.get(value[0], MergingPositionRatio.CONSTANT)
            # 设置键值对
            self.meg_configs[key] = value
            return True
        return False

    def getConfig(self):
        ''' 获取配置
        '''
        return self.meg_configs


class TdFilterCheckType(Enum):
    '''
    需要检查的类型
    '''
    AREA = 1
    WIDTH = 2
    HEIGHT = 4
    PERIMETER = 8
    ASPECTRATIO = 16
    OCCUPIEDRATIO = 32
    COMPACTNESS = 64
    SWT = 128

class TdFilterConfigKey(Enum):
    ''' Keys
    '''
    FLAG = 0
    AREA_LIM = 1
    WIDTH_LIM = 2
    HEIGHT_LIM = 3
    PERIMETER_LIM = 4
    ASPECT_RATIO_LIM = 5
    ASPECT_RATIO_GT1 = 6
    OCCUPATION_LIM = 7
    COMPACTNESS_LIM = 8

class TdFilterConfig:
    ''' 过滤器参数
    '''
    def __init__(self):
        self.flt_configs = {
            'default': {
                TdFilterConfigKey.FLAG: [],
                TdFilterConfigKey.AREA_LIM: 0,
                TdFilterConfigKey.WIDTH_LIM: [0, 0],
                TdFilterConfigKey.HEIGHT_LIM: [0, 0],
                TdFilterConfigKey.PERIMETER_LIM: [0, 0],
                TdFilterConfigKey.ASPECT_RATIO_LIM: [0, 0],
                TdFilterConfigKey.ASPECT_RATIO_GT1: True,
                TdFilterConfigKey.OCCUPATION_LIM: [0, 0],
                TdFilterConfigKey.COMPACTNESS_LIM: [0, 0],
            }
        }

    def setConfig(self, configs):
        ''' 设置过滤器配置
        '''
        for fltname in configs['filters'].keys():
            yaml_data = configs['filters'][fltname]
            self.addNewFilter(fltname)
            flag = []
            if "area" in yaml_data.get('flag', 0):
                flag.append(TdFilterCheckType.AREA)
            if "width" in yaml_data.get('flag', 0):
                flag.append(TdFilterCheckType.WIDTH)
            if "height" in yaml_data.get('flag', 0):
                flag.append(TdFilterCheckType.HEIGHT)
            if "perimeter" in yaml_data.get('flag', 0):
                flag.append(TdFilterCheckType.PERIMETER)
            if "aspect_ratio" in yaml_data.get('flag', 0):
                flag.append(TdFilterCheckType.ASPECTRATIO)
            if "occupied_ratio" in yaml_data.get('flag', 0):
                flag.append(TdFilterCheckType.OCCUPIEDRATIO)
            if "compactness" in yaml_data.get('flag', 0):
                flag.append(TdFilterCheckType.COMPACTNESS)
            TdFilterConfig.setConfigItem(self, fltname, TdFilterConfigKey.FLAG, flag)
            TdFilterConfig.setConfigItem(self, fltname, TdFilterConfigKey.AREA_LIM, int(yaml_data.get('area_lim', 0)))
            TdFilterConfig.setConfigItem(self, fltname, TdFilterConfigKey.PERIMETER_LIM, [int(yaml_data.get('perimeter_lim', [0, 0])[0]), int(yaml_data.get('perimeter_lim', [0, 0])[1])])
            TdFilterConfig.setConfigItem(self, fltname, TdFilterConfigKey.ASPECT_RATIO_LIM, [float(yaml_data.get('aspect_ratio_lim', [0, 0])[0]), float(yaml_data.get('aspect_ratio_lim', [0, 0])[1])])
            TdFilterConfig.setConfigItem(self, fltname, TdFilterConfigKey.OCCUPATION_LIM, [float(yaml_data.get('occupation_lim', [0, 0])[0]), float(yaml_data.get('occupation_lim', [0, 0])[1])])
            TdFilterConfig.setConfigItem(self, fltname, TdFilterConfigKey.COMPACTNESS_LIM, [float(yaml_data.get('compactness_lim', [0, 0])[0]), float(yaml_data.get('compactness_lim', [0, 0])[1])])
            TdFilterConfig.setConfigItem(self, fltname, TdFilterConfigKey.WIDTH_LIM, [int(yaml_data.get('width_lim', [0, 0])[0]), int(yaml_data.get('width_lim', [0, 0])[1])])
            TdFilterConfig.setConfigItem(self, fltname, TdFilterConfigKey.HEIGHT_LIM, [int(yaml_data.get('height_lim', [0, 0])[0]), int(yaml_data.get('height_lim', [0, 0])[1])])
            TdFilterConfig.setConfigItem(self, fltname, TdFilterConfigKey.ASPECT_RATIO_GT1, yaml_data.get('aspect_ratio_gt1', True))

    def setConfigItem(self, fltname, key, value):
        ''' 设置单个参数
        '''
        if self.flt_configs.get(fltname, None) is not None:
            sub_config = self.flt_configs[fltname]
            if sub_config.get(key, None) is not None:
                sub_config[key] = value
            return True
        return False

    def addNewFilter(self, fltname):
        ''' 新增 filter
        '''
        newconf = {
            TdFilterConfigKey.FLAG: [],
            TdFilterConfigKey.AREA_LIM: 0,
            TdFilterConfigKey.WIDTH_LIM: [0, 0],
            TdFilterConfigKey.HEIGHT_LIM: [0, 0],
            TdFilterConfigKey.PERIMETER_LIM: [0, 0],
            TdFilterConfigKey.ASPECT_RATIO_LIM: [0, 0],
            TdFilterConfigKey.ASPECT_RATIO_GT1: True,
            TdFilterConfigKey.OCCUPATION_LIM: [0, 0],
            TdFilterConfigKey.COMPACTNESS_LIM: [0, 0],
            'swt': {
                'total_points': 0,
                'mode_lim': 0,
                'mean_lim': [0, 0],
                'std_lim': [0, 0]
            }
        }
        self.flt_configs[fltname] = newconf

    def getConfig(self, keystr):
        ''' 获取过滤器配置
        '''
        return self.flt_configs.get(keystr, None)


class TdConfig(TdPrepConfig, TdExtractConfig, TdMergeTLConfig, TdFilterConfig):
    ''' 配置文件类
    '''
    def __init__(self, config_file_path=None):
        TdPrepConfig.__init__(self)
        TdExtractConfig.__init__(self)
        TdMergeTLConfig.__init__(self)
        TdFilterConfig.__init__(self)
        if config_file_path is not None:
            self.loadConfigFromFile(config_file_path)

    def getPrepConfig(self):
        ''' 获取预处理参数
        '''
        return TdPrepConfig.getConfig(self)

    def getExtractConfig(self):
        ''' 获取连通域提取参数
        '''
        return TdExtractConfig.getConfig(self)

    def getMergeTLConfig(self):
        ''' 获取文本行合并参数
        '''
        return TdMergeTLConfig.getConfig(self)

    def getFilterConfig(self, keystr):
        ''' 获取过滤器参数
        '''
        return TdFilterConfig.getConfig(self, keystr)

    def loadConfigFromFile(self, config_file_path):
        ''' 加载配置文件
        '''
        try:
            config_file = open(config_file_path, "r")
        except IOError:
            print("Cannot open file %s" % config_file_path)
            sys.exit()
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        config_file.close()
        TdPrepConfig.setConfig(self, config)
        TdExtractConfig.setConfig(self, config)
        TdMergeTLConfig.setConfig(self, config)
        TdFilterConfig.setConfig(self, config)


class AppSettings:
    ''' 程序的运行时设置
    '''
    config_file_path = "conf/default.yaml"
    curstage = "location"
    def __init__(self):
        pass
