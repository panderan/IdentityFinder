#!/usr/bin/python

''' SVC Display Widget
'''
import logging
import cv2
from PyQt5.QtCore import pyqtSignal
from tdlib.location import TdMergingTextLine, TdMergingOverlap
from tdlib.common import crop_rect
from tdlib.svc import TdSVC
from gui.app_widgets.basic_display_widget import BasicDisplayWidget
from gui.app_widgets.feature_control_widget import SVCDisplayCtrlWidget
from conf.config import TdConfig, AppSettings, TdSVCConfigKey

logger = logging.getLogger(__name__)


class SVCDisplayWidget(BasicDisplayWidget):
    ''' 用于显示文本行合并图像的 Widget 控件
    '''

    requireData = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_panel = None
        self.svc = TdSVC()
        self.dr_widget = None
        self.input_data = []
        self.output_data = []
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
        svcconf = self.control_panel.getConfiguration() \
                  if self.control_panel is not None else \
                  TdConfig(AppSettings.config_file_path).getSVCConfig()
        ret = self.svc.init(svcconf.get(TdSVCConfigKey.MCONF_PATH, None))
        if not ret:
            return False

        # 获取输入数据
        logger.info("SVC require datas.")
        self.requireData.emit()
        logger.info("SVC tell data was recevied")

        # SVC 检测过滤
        final_tl = []
        for item in self.input_data[0]:
            tl = []
            name, bg_image, tlregions = item
            for region in tlregions:
                sample, _ = crop_rect(bg_image, region)
                ret = self.svc.predict(sample)
                if ret:
                    tl.append(region)
            final_tl.append((name, tlregions, tl))

        # 最终合并
        ret_final_mtl, ret_final_stl = [], []
        for item in final_tl:
            name, mtl, stl = item
            ret_final_mtl.extend(mtl)
            ret_final_stl.extend(stl)
        merger = TdMergingOverlap()
        merger.setConfig(TdConfig(AppSettings.config_file_path).getMergeTLConfig())
        tlsin1 = merger.mergeTextLine(ret_final_stl)
        self.output_data = (ret_final_mtl, ret_final_stl, tlsin1)

        # 显示结果
        rgb_image = self.input_data[1].copy()
        rgb_image = TdMergingTextLine.drawRegions(rgb_image, (255, 255, 255), cv2.LINE_4, ret_final_mtl)
        rgb_image = TdMergingTextLine.drawRegions(rgb_image, (0, 255, 0), cv2.LINE_4, tlsin1)
        self.setDisplayCvImage(rgb_image)
        return self.output_data


    def openControlPanel(self):
        ''' 打开参数控制面板
        '''
        if self.control_panel is None:
            self.control_panel = SVCDisplayCtrlWidget()
            self.control_panel.ui.btn_ok.clicked.connect(self.doPreprocess)
        self.control_panel.show()
        return

    def setImage(self, qimage):
        ''' 载入图像
        '''
        self.setDisplayQImage(qimage)
        return
