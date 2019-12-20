#!/usr/bin/python


''' 连通域提取控制面板
'''

import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
import gui.ui.merging_textline_control_ui as merge_ctrl_ui
from tdlib.filters import TdFilterCheckType
from tdlib.location import MergingStrategy
from conf.config import TdConfig, TdMergeTLConfig, TdFilterConfig, AppSettings, TdMergeTLConfigKey, TdFilterConfigKey

logger = logging.getLogger(__name__)


class MergeDisplayCtrlWidget(QWidget):
    ''' 连通域提取控制面板
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = merge_ctrl_ui.Ui_MergeCtrlWidget()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(':/images/icon.png'))
        self.setAttribute(Qt.WA_QuitOnClose, False)
        # 填充 MergeTLE 参数
        merge_conf = TdConfig(AppSettings.config_file_path).getMergeTLConfig()
        self.ui.linedit_combined_area_size_lim.setText(str(merge_conf[TdMergeTLConfigKey.COMBINED_AREA_SIZE_LIM]))
        self.ui.dspinbox_overlap_ratio.setValue(merge_conf[TdMergeTLConfigKey.OVERLAP_RATIO])
        self.ui.dspinbox_distance.setValue(merge_conf[TdMergeTLConfigKey.DISTANCE])
        self.ui.dspinbox_combined_aspect_ratio_low.setValue(merge_conf[TdMergeTLConfigKey.COMBINED_ASPECT_RATIO_LIM][0])
        self.ui.dspinbox_combined_aspect_ratio_high.setValue(merge_conf[TdMergeTLConfigKey.COMBINED_ASPECT_RATIO_LIM][1])
        strategy_dict = {"horizon": MergingStrategy.HORIZON.value-1,
                         "vertical": MergingStrategy.VERTICAL.value-1}
        self.ui.combobox_strategy.setCurrentIndex(strategy_dict.get(merge_conf[TdMergeTLConfigKey.STRATEGY], 0))
        self.ui.linedit_scope_lim.setText(str(merge_conf[TdMergeTLConfigKey.SCOPE_LIM]))
        self.initConnects()
        return

    def initConnects(self):
        ''' 初始化信号与槽的连接
        '''
        return

    def getConfiguration(self):
        ''' 获得配置信息
        Args:
            flag: 0 获取 MergingTL 参数
                  1 获取 Filter 参数
        '''
        megconf = TdMergeTLConfig()
        megconf.setConfigItem(TdMergeTLConfigKey.COMBINED_AREA_SIZE_LIM, \
                              int(self.ui.linedit_combined_area_size_lim.text())
                              )
        megconf.setConfigItem(TdMergeTLConfigKey.COMBINED_ASPECT_RATIO_LIM, \
                              [self.ui.dspinbox_combined_aspect_ratio_low.value(), \
                               self.ui.dspinbox_combined_aspect_ratio_high.value() \
                              ])
        megconf.setConfigItem(TdMergeTLConfigKey.OVERLAP_RATIO, self.ui.dspinbox_overlap_ratio.value())
        megconf.setConfigItem(TdMergeTLConfigKey.DISTANCE, self.ui.dspinbox_distance.value())
        megconf.setConfigItem(TdMergeTLConfigKey.STRATEGY, self.ui.combobox_strategy.currentText())
        megconf.setConfigItem(TdMergeTLConfigKey.VERBOSE, self.ui.checkbox_show_verbsoe.isChecked())
        megconf.setConfigItem(TdMergeTLConfigKey.SCOPE_LIM, int(self.ui.linedit_scope_lim.text()))
        return megconf.getConfig()
