#!/usr/bin/python

''' Merge Display Widget
'''
import logging
from copy import deepcopy
import cv2
from PyQt5.QtCore import pyqtSignal
from tdlib.morphops import TdMorphOperator
from tdlib.filters import TdFilter
from tdlib.location import TdMergingTextLine
from gui.app_widgets.basic_display_widget import BasicDisplayWidget
from gui.app_widgets.merging_control_widget import MergeDisplayCtrlWidget
from gui.app_widgets.verbose_show_widget import VerboseDisplayWidget
from conf.config import TdConfig, AppSettings, TdMergeTLConfigKey

logger = logging.getLogger(__name__)


class MergeDisplayWidget(BasicDisplayWidget):
    ''' 用于显示文本行合并图像的 Widget 控件
    '''

    requireData = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_panel = None
        self.filter = TdFilter()
        self.morpher = TdMorphOperator()
        self.merger = TdMergingTextLine()
        self.cur_config = {}
        self.dr_widget = None
        self.input_image = []
        self.output_data = []
        self.color_image = None
        return

    def paintEvent(self, e):
        ''' 重载绘制函数
        '''
        super().paintEvent(e)
        return

    def doPreprocess(self):
        ''' 进行预处理
        '''
        # 获取参数，进行预处理
        megconf = self.getConfig()
        self.merger.setConfig(megconf)

        # 获取输入数据
        logger.info("Merger require datas.")
        self.requireData.emit()
        logger.info("Merger tell data was recevied")

        # 合并文本行
        self.output_data, verboses_data = [], []
        for name, binarized_image, regions in self.input_image:
            if megconf[TdMergeTLConfigKey.VERBOSE]:
                self.merger.debug.enableDebug(self.color_image.shape)
                self.merger.debug.setBgColorImage(self.color_image)
            self.merger.printParams(name)
            tl_regions = self.merger.mergeTextLine(regions)
            self.output_data.append((name, binarized_image, tl_regions))
            if megconf[TdMergeTLConfigKey.VERBOSE]:
                verboses_data.append(deepcopy(self.merger.debug))

        # 显示处理结果
        if megconf[TdMergeTLConfigKey.VERBOSE] and self.merger.debug is not None:
            if self.dr_widget is None:
                self.dr_widget = VerboseDisplayWidget()
            for data in verboses_data:
                self.dr_widget.setMergeVerboseData(data)
                self.dr_widget.show()

        # 绘制中间结果
        result_image = self.color_image.copy()
        for item in self.output_data:
            result_image = TdMergingTextLine.drawRegions(result_image, (255, 255, 255), cv2.LINE_4, item[-1])
        self.setDisplayCvImage(result_image)
        return

    def openControlPanel(self):
        ''' 打开参数控制面板
        '''
        if self.control_panel is None:
            self.control_panel = MergeDisplayCtrlWidget()
            self.control_panel.ui.btn_ok.clicked.connect(self.doPreprocess)
        self.control_panel.show()
        return

    def getConfig(self):
        ''' 获取配置
        '''
        megconf = self.control_panel.getConfiguration() \
                  if self.control_panel is not None else \
                  TdConfig(AppSettings.config_file_path).getMergeTLConfig()
        return megconf

    def setImage(self, qimage):
        ''' 载入图像
        '''
        self.setDisplayQImage(qimage)
        return

    def getResult(self):
        ''' 获得输出
        '''
        self.doPreprocess()
        return self.output_data
