#!/usr/bin/python

'''
预处理控制面板
'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
import gui.ui.preprocess_control_ui as prep_ctrl_ui
from conf.config import TdConfig, TdPrepConfigKeys, AppSettings

class PreprocessDisplayCtrlWidget(QWidget):
    '''
    预处理控制面板
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = prep_ctrl_ui.Ui_PrepCtrlWidget()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(':/images/icon.png'))
        self.setAttribute(Qt.WA_QuitOnClose, False)

        prep_conf = TdConfig(AppSettings.config_file_path).getPrepConfig()
        self.ui.linedit_total_pixels.setText(str(prep_conf[TdPrepConfigKeys.TOTAL_PIXELS]))
        self.ui.spinbox_bilateral_arg1.setValue(prep_conf[TdPrepConfigKeys.BILATERAL][0])
        self.ui.spinbox_bilateral_arg2.setValue(prep_conf[TdPrepConfigKeys.BILATERAL][1])
        self.ui.spinbox_bilateral_arg3.setValue(prep_conf[TdPrepConfigKeys.BILATERAL][2])
        self.ui.spinbox_gaussian_size.setValue(prep_conf[TdPrepConfigKeys.GAUSS_SIZE])
        self.ui.dspinbox_offset.setValue(prep_conf[TdPrepConfigKeys.OFFSET])
        return

    def getConfiguration(self):
        '''
        获得配置信息
        '''
        prep_conf = {TdPrepConfigKeys.TOTAL_PIXELS: int(self.ui.linedit_total_pixels.text()),
                     TdPrepConfigKeys.BILATERAL: [self.ui.spinbox_bilateral_arg1.value(), \
                                                  self.ui.spinbox_bilateral_arg2.value(), \
                                                  self.ui.spinbox_bilateral_arg3.value()],
                     TdPrepConfigKeys.GAUSS_SIZE: self.ui.spinbox_gaussian_size.value(),
                     TdPrepConfigKeys.OFFSET: self.ui.dspinbox_offset.value(),
                     TdPrepConfigKeys.DEBUG: self.ui.checkbox_show_verbose.isChecked(),
                     TdPrepConfigKeys.DEBUG_SOURCE: self.ui.combo_source.currentText()}
        return prep_conf
