#!/usr/bin/python

''' Extract Display Widget
'''
import logging
from PyQt5.QtCore import pyqtSignal
from tdlib.extraction import TdExtractConnectDomain
from tdlib.filters import TdFilter
from tdlib.morphops import TdMorphOperator
from gui.app_widgets.basic_display_widget import BasicDisplayWidget
from gui.app_widgets.extract_control_widget import ExtractDisplayCtrlWidget
from gui.app_widgets.verbose_show_widget import VerboseDisplayWidget
from conf.config import TdConfig, AppSettings, TdExtractConfigKey
# import gui.app_widgets.common as apw_comm
# from gui.app_widgets.popup_display_widget import DisplayResultWidget


logger = logging.getLogger(__name__)


class ExtractDisplayWidget(BasicDisplayWidget):
    ''' 用于显示连通域提取图像的 Widget 控件
    '''

    requireData = pyqtSignal(list, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_panel = None
        self.extracter = TdExtractConnectDomain()
        self.filter = TdFilter()
        self.morpher = TdMorphOperator()
        self.cur_config = {}
        self.dr_widget = None
        self.input_images = []
        self.output_regionlist = []
        return

    def paintEvent(self, e):
        ''' 重载绘制函数
        '''
        super().paintEvent(e)
        return

    def doPreprocess(self):
        ''' 进行预处理
        '''
        # 获取并设置连通域提取配置参数
        extconf = self.control_panel.getConfiguration(flag=0) \
                  if self.control_panel is not None else  \
                  TdConfig(AppSettings.config_file_path).getExtractConfig()
        fltconf = self.control_panel.getConfiguration(flag=1) \
                  if self.control_panel is not None else \
                  TdConfig(AppSettings.config_file_path).getFilterConfig("extract")
        self.filter.setConfig(fltconf)
        self.extracter.setConfig(extconf)

        # 获取输入数据
        msg = "Extractor require datas. Srcs:%s."%extconf[TdExtractConfigKey.SRCS]
        logger.info(msg)
        self.requireData.emit(extconf[TdExtractConfigKey.SRCS], extconf)
        logger.info("Extractor tell data was recevied")

        # 提取连通域
        binarizes, debug_data = [], []
        self.extracter.debug.setEnable(bool(extconf[TdExtractConfigKey.VERBOSE]))
        self.filter.debug.setEnable(bool(extconf[TdExtractConfigKey.VERBOSE]))
        for image in self.input_images:
            binarized = self.extracter.extract_with_labels_for_images([image], self.filter)
            binarizes.append((image['name'], binarized.copy(), image['image']))
            if extconf[TdExtractConfigKey.VERBOSE] and self.extracter.debug.enable:
                debug_data.extend(self.extracter.debug.data)

        # 显示 MSER 提取结果
        if extconf[TdExtractConfigKey.VERBOSE] and self.extracter.debug.enable:
            if self.dr_widget is None:
                self.dr_widget = VerboseDisplayWidget()
            self.dr_widget.setExtracterVerboseData(debug_data)
            self.dr_widget.show()

        # 获取并设置形态学处理配置参数
        fltconf = self.control_panel.getConfiguration(flag=1) \
                  if self.control_panel is not None else \
                  TdConfig(AppSettings.config_file_path).getFilterConfig("morph")
        self.filter.setConfig(fltconf)

        # 形态学处理
        self.output_regionlist = []
        for binarized in binarizes:
            regions = self.morpher.morph_operation(binarized[1], binarized[2], self.filter)
            self.output_regionlist.append(((binarized[0], binarized[1], regions.copy())))

        # 显示 MORPH 处理结果
        if extconf[TdExtractConfigKey.VERBOSE_MORPH]:
            verbose_data = {}
            for item in self.output_regionlist:
                verbose_data[item[0]] = self.morpher.getMaskImage(item[1], item[2])
            if self.dr_widget is None:
                self.dr_widget = VerboseDisplayWidget()
            self.dr_widget.setPrepVerboseData(verbose_data)
            self.dr_widget.show()
        return

    def openControlPanel(self):
        ''' 打开参数控制面板
        '''
        if self.control_panel is None:
            self.control_panel = ExtractDisplayCtrlWidget()
            self.control_panel.ui.btn_ok.clicked.connect(self.doPreprocess)
        self.control_panel.show()
        return

    def setImage(self, qimage):
        ''' 载入图像
        '''
        self.setDisplayQImage(qimage)
        return

    def getResult(self):
        ''' 获得输出
        '''
        self.doPreprocess()
        return self.output_regionlist
