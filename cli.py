#!/usr/bin/env python

''' text-detection 命令行程序(CLI)
'''

import logging
import sys
import getopt
from enum import Enum
from math import floor, ceil, sqrt
import numpy as np
import cv2
import matplotlib.pyplot as plt
from tdlib.preprocessing import TdPreprocessing
from tdlib.extraction import TdExtractConnectDomain, ExtractDirection
from tdlib.filters import TdFilter
from tdlib.morphops import TdMorphOperator
from tdlib.location import TdMergingTextLine
from tdlib.common import crop_rect
from conf.config import TdConfig, TdExtractConfigKey


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

class CliSaveOptions(Enum):
    ''' 保存选项
    '''
    NONE = 0
    MERGE = 1

class CliGrayType(Enum):
    ''' Cli Gray Type
    '''
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
        self.show_opts = []
        self.makesample = False
        self.save_option = CliSaveOptions.NONE

        self.preprocessing = TdPreprocessing()
        self.extracter = TdExtractConnectDomain()
        self.filter = TdFilter()
        self.merger = TdMergingTextLine()

        self.config = TdConfig()
        self.morpher = TdMorphOperator()

    def run(self):
        ''' 运行命令
        '''
        # 解析命令行参数
        self.parseArgs()
        logger.info("CLI RUN, Image:%s", self.image_path)

        # 加载配置
        self.config.loadConfigFromFile(self.config_file_path)

        # 读取输入
        input_image = cv2.imread(self.image_path)
        rgb_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

        # 预处理
        self.prepFunc(rgb_image)

        # 连通域提取
        binarizes = self.extractFunc()

        # 形态学优化
        regionlist = self.morphFunc(binarizes)

        # 文本行合并
        tlregionlist = self.mergingFunc(regionlist)
        self.makeSVCSample(tlregionlist)

    def parseArgs(self):
        ''' 解析命令行参数
        '''
        try:
            opts, _ = getopt.getopt(sys.argv[1:], "i:", \
                            ["show=", "config=", "gray=", "makesample", "save=", "debug=", "help"])
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
                arguments = arg.split(',')
                options = {"prep": CliShowOptions.SHOW_PREP,
                           "extract": CliShowOptions.SHOW_EXTRACT,
                           "morph": CliShowOptions.SHOW_MORPH,
                           "merge": CliShowOptions.SHOW_MERGE,
                           "feature": CliShowOptions.SHOW_FEATURE}
                self.show_opts = [options.get(i, CliShowOptions.SHOW_NONE) for i in arguments]
            elif cmd in '--gray':
                arguments = arg.split(',')
                options = {"gray": CliGrayType.GRAY,
                           "blue": CliGrayType.BLUE,
                           "green": CliGrayType.GREEN,
                           "red": CliGrayType.RED}
                self.gray_type = [options.get(i, CliGrayType.GRAY) for i in arguments]
            elif cmd in '--debug':
                arguments = arg.split(',')
                if 'prep' in arguments:
                    self.preprocessing.debug.setEnable(True)
            elif cmd in '--makesample':
                self.makesample = True
            elif cmd in '--save':
                if arg == 'merge':
                    self.save_option = CliSaveOptions.MERGE
            else:
                usage()
                sys.exit(1)

    def showPrep(self):
        ''' 显示预处理结果
        '''
        if CliShowOptions.SHOW_PREP not in self.show_opts:
            return
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
                cols = np.uint8(np.ceil(sqrt(total)))
                rows = np.uint8(np.floor(sqrt(total)))
                for i in range(1, total+1):
                    plt.subplot(rows*100 + cols*10 + i)
                    plt.title(data[i-1][0])
                    plt.imshow(data[i-1][1], "gray")
            plt.show()

    def showExtract(self, binarizes):
        ''' 显示连通域提取结果
        '''
        if CliShowOptions.SHOW_EXTRACT not in self.show_opts:
            return
        total = len(binarizes)
        rows, cols = int(floor(sqrt(total))), int(ceil(sqrt(total)))
        for i, binarized in enumerate(binarizes):
            plt.subplot(rows*100+cols*10+i+1)
            plt.title(binarized[0])
            plt.imshow(binarized[1], "gray")
        plt.show()

    def showMorph(self, regionlist):
        ''' 显示形态学处理结果
        '''
        if CliShowOptions.SHOW_MORPH not in self.show_opts:
            return
        self.show_opts.append(CliShowOptions.SHOW_EXTRACT)
        binarizes = []
        for regiondata in regionlist:
            binarized = self.morpher.getMaskImage(regiondata[1], regiondata[2])
            binarizes.append((regiondata[0], binarized))
        self.showExtract(binarizes)

    def showMerging(self, tlregionlist):
        ''' 显示文本行合并结果
        '''
        if CliShowOptions.SHOW_MERGE not in self.show_opts and self.save_option is not CliSaveOptions.MERGE:
            return

        rgb_image = self.preprocessing.rgb_image.copy()
        for item in tlregionlist:
            rgb_image = TdMergingTextLine.drawRegions(rgb_image, (255, 255, 255), cv2.LINE_4, item[-1])
            if CliShowOptions.SHOW_MERGE in self.show_opts:
                plt.imshow(rgb_image)
                plt.show()
            if self.save_option is CliSaveOptions.MERGE:
                bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite("data/save/"+self.image_name+"-"+item[0]+".jpg", bgr_image)

    def prepFunc(self, rgb_image):
        ''' 图像预处理
        '''
        self.preprocessing.setConfig(self.config.getPrepConfig())
        self.preprocessing.rgb_image = rgb_image
        self.showPrep()

    def extractFunc(self):
        ''' 连通域提取
        '''
        binarizes = []
        config = self.config.getExtractConfig()
        positive_conf = config.copy()
        positive_conf[TdExtractConfigKey.DIRECTION] = ExtractDirection.Positive
        negative_conf = config.copy()
        negative_conf[TdExtractConfigKey.DIRECTION] = ExtractDirection.Negitive
        ext_flt = self.filter.setConfig(self.config.getFilterConfig("extract"))
        for src in config[TdExtractConfigKey.SRCS]:
            grayname, chartype = src.split('.')

            if grayname == "Gray":
                gray = self.preprocessing.ret_gray
            elif grayname == "Red":
                gray = self.preprocessing.ret_red
            elif grayname == "Green":
                gray = self.preprocessing.ret_green
            elif grayname == "Blue":
                gray = self.preprocessing.ret_blue
            else:
                sys.exit()

            if chartype in ["Black", "Both"]:
                image = [{'name':grayname,
                          'image':gray[1],
                          'conf': positive_conf}]
                binarized = self.extracter.extract_with_labels_for_images(image, ext_flt)
                binarizes.append((src, binarized, gray[1]))
            if chartype in ["Bright", "Both"]:
                image = [{'name':grayname,
                          'image':gray[2],
                          'conf': negative_conf}]
                binarized = self.extracter.extract_with_labels_for_images(image, ext_flt)
                binarizes.append((src, binarized, gray[2]))

        self.showExtract(binarizes)
        return binarizes

    def morphFunc(self, binarizes):
        ''' 形态学处理
        '''
        regionlist = []
        mph_flt = self.filter.setConfig(self.config.getFilterConfig("morph"))
        for binarized in binarizes:
            regions = self.morpher.morph_operation(binarized[1], binarized[2], mph_flt)
            regionlist.append(((binarized[0], binarized[1], regions.copy())))
        self.showMorph(regionlist)
        return regionlist

    def mergingFunc(self, regionlist):
        ''' 文本行合并
        '''
        tlregionlist = []
        config = self.config.getMergeTLConfig()
        self.merger.setConfig(config)
        for name, binarized, regions in regionlist:
            self.merger.printParams(name)
            tl_regions = self.merger.mergeTextLine(regions)
            tlregionlist.append((name, binarized, tl_regions))
        self.showMerging(tlregionlist)
        return tlregionlist

    def makeSVCSample(self, tlregionlist):
        ''' 生成特征分类样本
        '''
        if self.makesample is False:
            return

        plt.ion()
        i = 0
        for item in tlregionlist:
            bg_image = self.preprocessing.getRet(item[0])[-1]
            for region in item[-1]:
                sample, _ = crop_rect(bg_image, region)
                plt.imshow(sample, "gray")
                plt.pause(0.2)
                judge = input("is text region? : ")
                judge = 'Y' if judge == 'Y' else 'N'
                cv2.imwrite("data/Model/" + self.image_name + str(i) + "-" + judge + ".jpg", sample)
                i += 1
        plt.ioff()
        sys.exit(0)


if __name__ == '__main__':
    app = Cli()
    app.run()
