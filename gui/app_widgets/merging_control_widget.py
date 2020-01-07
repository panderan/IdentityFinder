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
from conf.config import TdConfig, TdMergeTLConfig, TdFilterConfig, AppSettings, TdMergeTLConfigKey, TdFilterConfigKey, MergingPositionRatio

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
        self.ui.combobox_strategy.setCurrentIndex(merge_conf[TdMergeTLConfigKey.STRATEGY].value-1)
        self.ui.combobox_position_ratio.setCurrentIndex(merge_conf[TdMergeTLConfigKey.POSITION_RATIO].value-1)
        self.ui.dspinbox_position_ratio.setValue(merge_conf[TdMergeTLConfigKey.POSITION_RATIO_CONSTANT])
        self.ui.dspinbox_position_ratio.setVisible(bool(merge_conf[TdMergeTLConfigKey.POSITION_RATIO] is MergingPositionRatio.CONSTANT))
        self.ui.linedit_scope_lim.setText(str(merge_conf[TdMergeTLConfigKey.SCOPE_LIM]))

        fltr_conf = TdConfig(AppSettings.config_file_path).getFilterConfig("merge")
        self.ui.checkbox_tl_area_lim_enable.setChecked(bool(TdFilterCheckType.AREA in fltr_conf[TdFilterConfigKey.FLAG]))
        self.ui.spinbox_tl_area_lim.setValue(fltr_conf[TdFilterConfigKey.AREA_LIM])

        self.initConnects()
        return

    def initConnects(self):
        ''' 初始化信号与槽的连接
        '''
        self.ui.combobox_position_ratio.activated.connect(self.onActionPositionRatioActivated)

    def getConfiguration(self, flag=0):
        ''' 获得配置信息
        Args:
            flag: 0 获取 MergingTL 参数
                  1 获取 Filter 参数
        '''
        if flag == 0:
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
            megconf.setConfigItem(TdMergeTLConfigKey.POSITION_RATIO, \
                                  (self.ui.combobox_position_ratio.currentText(), \
                                   self.ui.dspinbox_position_ratio.value()
                                  ))
            return megconf.getConfig()
        else:
            fltconf = TdFilterConfig()
            fltconf.setConfigItem('default', TdFilterConfigKey.AREA_LIM, self.ui.spinbox_tl_area_lim.value())
            flt_flag = []
            if self.ui.checkbox_tl_area_lim_enable.isChecked():
                flt_flag.append(TdFilterCheckType.AREA)
            fltconf.setConfigItem('default', TdFilterConfigKey.FLAG, flt_flag)
            return fltconf.flt_configs.get('default', None)

    def onActionPositionRatioActivated(self, idx):
        ''' 更新 Position Ratio 选项
        '''
        self.ui.dspinbox_position_ratio.setVisible(idx == MergingPositionRatio.CONSTANT.value - 1)

