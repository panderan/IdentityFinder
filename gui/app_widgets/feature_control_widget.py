#!/usr/bin/python

''' SVC控制面板
'''
from pathlib import Path
import yaml
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtGui import QIcon
import gui.ui.svc_control_ui as svc_ctrl_ui
from conf.config import TdConfig, TdSVCConfigKey, AppSettings


class SVCDisplayCtrlWidget(QWidget):
    ''' SVC控制面板
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = svc_ctrl_ui.Ui_SVCCtrlWidget()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(':/images/icon.png'))
        self.setAttribute(Qt.WA_QuitOnClose, False)

        svc_conf = TdConfig(AppSettings.config_file_path).getSVCConfig()
        self.mconf_path = svc_conf.get(TdSVCConfigKey.MCONF_PATH, None)
        self.ui.linedit_svc_conf_path.setText(str(self.mconf_path))
        if Path(self.mconf_path).exists():
            with open(self.mconf_path, 'r') as f:
                mconf = yaml.load(f, Loader=yaml.FullLoader)
                self.ui.label_config_context.setText(str(mconf))

        self.ui.btn_svc_conf_path.clicked.connect(self.onActionBtnClicked)

    def getConfiguration(self):
        ''' 获得配置信息
        '''
        svc_conf = {TdSVCConfigKey.MCONF_PATH: self.mconf_path}
        return svc_conf

    def onActionBtnClicked(self):
        ''' 选择新的 MODEL 配置文件
        '''
        fname, _ = QFileDialog.getOpenFileName(self, "Open file", \
                                        '~', "SVC Model Config Files (*.model)")
        if len(fname) > 5:
            self.mconf_path = fname
