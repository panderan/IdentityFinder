#!/usr/bin/env python

''' text-detection 命令行程序(CLI)
'''

import logging
import sys
import getopt
from enum import Enum
import math
import numpy as np
import cv2
import matplotlib.pyplot as plt
from tdlib.preprocessing import TdPreprocessing
from tdlib.extraction import TdExtractConnectDomain
from tdlib.filters import TdFilter
from tdlib.morphops import TdMorphOperator
from tdlib.location import TdMergingTextLine, debugGenerateElectionImage
from tdlib.location import threshold_of_position_ratio_for_idcard
from conf.config import TdConfig


logging.basicConfig(level=logging.INFO, \
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)


def usage():
    ''' 显示帮助信息
    '''
    print("Help message")


class CliShowOptions(Enum):
    ''' 显示选项
    '''
    SHOW_NONE = 0
    SHOW_PREP = 1
    SHOW_EXTRACT = 2
    SHOW_MORPH = 4
    SHOW_MERGE = 8
    SHOW_MERGED = 16
    SHOW_FEATURE = 32
    SHOW_RESULT = 64

class CliGrayType(Enum):
    GRAY = 0
    BLUE = 1
    GREEN = 2
    RED = 3

class Cli:
    ''' text-detection 命令行程序(CLI)
    '''
    def __init__(self):
        self.image_path = None
        self.image_name = None
        self.config_file_path = None
        self.gray_type = None
        self.show_opts = None

        self.preprocessing = TdPreprocessing()
        self.extracter = TdExtractConnectDomain()
        self.filter = TdFilter()
        self.merger = TdMergingTextLine()

        self.config = TdConfig()
        self.morpher = TdMorphOperator()

    def run(self):
        '''
        运行命令
        '''
        # 解析命令行参数
        self.parseArgs()

        # 加载配置
        self.config.loadConfigFromFile(self.config_file_path)

        # 读取输入
        input_image = cv2.imread(self.image_path)
        rgb_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

        # 预处理
        self.preprocessing.setConfig(self.config.getPrepConfig())
        self.preprocessing.rgb_image = rgb_image
        self.showPrep()

        # 连通域提取
        self.extracter.setConfig(self.config.getExtractConfig())
        ext_flt = self.filter.setConfig(self.config.getFilterConfig("extract"))
        _, binarized = self.extracter.extract_with_labels({"name":"Blue", "image":self.preprocessing.blue_channel_preped}, ext_flt)
        if self.show_opts & CliShowOptions.SHOW_EXTRACT.value:
            plt.imshow(binarized, "gray")
            plt.show()

        # 形态学处理
        mph_flt = self.filter.setConfig(self.config.getFilterConfig("morph"))
        regions = self.morpher.morph_operation(binarized, mph_flt)
        if self.show_opts & CliShowOptions.SHOW_MORPH.value:
            verbose_image = self.morpher.getMaskImage(binarized, regions)
            plt.imshow(verbose_image, "gray")
            plt.show()

        # 文本行合并
        self.merger.setConfig(self.config.getMergeTLConfig())
        self.merger.debug.enableDebug(binarized.shape)
        self.merger.get_position_ratio_threshold = threshold_of_position_ratio_for_idcard
        self.merger.mergeTextLine(regions)
        if self.show_opts & CliShowOptions.SHOW_MERGED.value:
            for i in range(self.merger.debug.getTotalElections()):
                image = debugGenerateElectionImage(self.merger.debug, i)
                cv2.namedWindow("Merged", 0)
                cv2.imshow("Merged", image)
                cv2.waitKey(0)

    def parseArgs(self):
        ''' 解析命令行参数
        '''
        try:
            opts, _ = getopt.getopt(sys.argv[1:], "i:", \
                            ["show=", "config=", "gray=", "debug=", "help"])
        except getopt.GetoptError:
            print("argv error")
            sys.exit(1)

        for cmd, arg in opts:
            if cmd in "-i":
                self.image_path = arg
                self.image_name = self.image_path.split('/')[-1][0:-4]
            elif cmd in "--config":
                self.config_file_path = arg
            elif cmd in "--show":
                options = arg.split(',')
                self.show_opts = []
                if "prep" in options:
                    self.show_opts.append(CliShowOptions.SHOW_PREP)
                if "extract" in options:
                    self.show_opts.append(CliShowOptions.SHOW_EXTRACT)
                if "merge" in options:
                    self.show_opts.append(CliShowOptions.SHOW_MERGE)
                if "merged" in options:
                    self.show_opts.append(CliShowOptions.SHOW_MERGED)
                if "feature" in options:
                    self.show_opts.append(CliShowOptions.SHOW_FEATURE)
            elif cmd in '--gray':
                options = arg.split(',')
                self.gray_type = []
                if 'gray' in options:
                    self.gray_type.append(CliGrayType.GRAY)
                if 'blue' in options:
                    self.gray_type.append(CliGrayType.BLUE)
                if 'green' in options:
                    self.gray_type.append(CliGrayType.GREEN)
                if 'red' in options:
                    self.gray_type.append(CliGrayType.RED)
            elif cmd in '--debug':
                options = arg.split(',')
                if 'prep' in options:
                    self.preprocessing.debug.setEnable(True)
            else:
                usage()
                sys.exit(1)

    def showPrep(self):
        ''' 显示预处理结果
        '''
        if CliShowOptions.SHOW_PREP not in self.show_opts:
            return None
        for gray in self.gray_type:
            if gray is CliGrayType.GRAY:
                gray_name = "Gray"
                ret = self.preprocessing.ret_gray
            if gray is CliGrayType.BLUE:
                gray_name = "Blue Channel"
                ret = self.preprocessing.ret_blue
            if gray is CliGrayType.GREEN:
                gray_name = "Green Channel"
                ret = self.preprocessing.ret_green
            if gray is CliGrayType.RED:
                gray_name = "Red Channel"
                ret = self.preprocessing.ret_red

            if not self.preprocessing.debug.enable:
                plt.subplot(131)
                plt.title("Black chars")
                plt.imshow(ret[1], "gray")
                plt.subplot(132)
                plt.imshow(ret[0], "gray")
                plt.title(gray_name)
                plt.subplot(133)
                plt.title("Bright chars")
                plt.imshow(ret[2], "gray")
            else:
                data = self.preprocessing.debug.data
                total = len(data)
                cols = np.uint8(np.ceil(math.sqrt(total)))
                rows = np.uint8(np.floor(math.sqrt(total)))
                for i in range(1, total+1):
                    plt.subplot(rows*100 + cols*10 + i)
                    plt.title(data[i-1][0])
                    plt.imshow(data[i-1][1], "gray")
            plt.show()



if __name__ == '__main__':
    app = Cli()
    app.run()