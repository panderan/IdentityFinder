#!/usr/bin/python

'''
预处理控制面板
'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
import gui.ui.preprocess_control_ui as prep_ctrl_ui
from tdlib.preprocessing import TdPrepHatDirection
from conf.config import TdConfig

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

        prep_conf = TdConfig().getPrepConfig()
        self.ui.linedit_total_pixels.setText(str(prep_conf["total_pixels"]))
        self.ui.spinbox_gama.setValue(prep_conf["gamma"])
        self.ui.spinbox_guass_blur_size.setValue(prep_conf["gauss_blur_size"])
        self.ui.spinbox_struct_element_size.setValue(prep_conf["struct_element_size"])
        self.ui.spinbox_sigmod_center.setValue(prep_conf['sigmod_center'])
        self.ui.spinbox_sigmod_zoom.setValue(prep_conf['sigmod_zoom'])
        self.ui.spinbox_canny_max.setValue(prep_conf["canny_max"])
        self.ui.spinbox_canny_min.setValue(prep_conf["canny_min"])
        self.ui.checkbox_sobel_y.setChecked(prep_conf['sobel'])
        flag = True if prep_conf['hat'] & TdPrepHatDirection.TOPHAT.value else False
        self.ui.checkbox_top_hat.setChecked(flag)
        flag = True if prep_conf['hat'] & TdPrepHatDirection.BACKHAT.value else False
        self.ui.checkbox_back_hat.setChecked(flag)
        return

    def getConfiguration(self):
        '''
        获得配置信息
        '''
        config = {}
        config['total_pixels'] = int(self.ui.linedit_total_pixels.text())
        config['source'] = self.ui.combo_sources.currentText()
        config['struct_element_size'] = self.ui.spinbox_struct_element_size.value()
        config['gauss_blur_size'] = self.ui.spinbox_guass_blur_size.value()
        config['gamma'] = self.ui.spinbox_gama.value()
        config['canny_max'] = self.ui.spinbox_canny_max.value()
        config['canny_min'] = self.ui.spinbox_canny_min.value()
        config['sigmod_center'] = self.ui.spinbox_sigmod_center.value()
        config['sigmod_zoom'] = self.ui.spinbox_sigmod_zoom.value()
        config['sobel'] = self.ui.checkbox_sobel_y.isChecked()
        config['show_verbose'] = self.ui.checkbox_show_verbose.isChecked()
        ret = TdPrepHatDirection.TOPHAT.value if self.ui.checkbox_top_hat.isChecked() else 0
        ret += TdPrepHatDirection.BACKHAT.value if self.ui.checkbox_back_hat.isChecked() else 0
        config['hat'] = ret
        return config
