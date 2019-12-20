#!/usr/bin/python


''' 连通域提取控制面板
'''

import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.QtGui import QIcon
import gui.ui.extract_control_ui as extract_ctrl_ui
from tdlib.filters import TdFilterCheckType
from tdlib.extraction import ExtractDirection
from conf.config import TdConfig, TdExtractConfig, TdFilterConfig, TdExtractConfigKey, TdFilterConfigKey, AppSettings

logger = logging.getLogger(__name__)


class ExtractDisplayCtrlWidget(QWidget):
    ''' 连通域提取控制面板
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = extract_ctrl_ui.Ui_ExtractCtrlWidget()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(':/images/icon.png'))
        self.setAttribute(Qt.WA_QuitOnClose, False)

        extract_conf = TdConfig(AppSettings.config_file_path).getExtractConfig()
        self.ui.spinbox_mser_delta.setValue(extract_conf[TdExtractConfigKey.DELTA])
        self.ui.spinbox_mser_area_high.setValue(extract_conf[TdExtractConfigKey.AREA_MAX])
        self.ui.spinbox_mser_area_low.setValue(extract_conf[TdExtractConfigKey.AREA_MIN])
        self.ui.dspinbox_mser_variation.setValue(extract_conf[TdExtractConfigKey.VARIATION])
        for src in extract_conf[TdExtractConfigKey.SRCS]:
            self.ui.listWidget.addItem(QListWidgetItem(src))

        filter_conf = TdConfig(AppSettings.config_file_path).getFilterConfig('extract')
        self.ui.spinbox_filter_area_lim.setValue(filter_conf[TdFilterConfigKey.AREA_LIM])
        self.ui.spinbox_filter_perimeter_low.setValue(filter_conf[TdFilterConfigKey.PERIMETER_LIM][0])
        self.ui.spinbox_filter_perimeter_high.setValue(filter_conf[TdFilterConfigKey.PERIMETER_LIM][1])
        self.ui.dspinbox_filter_aspect_ratio_low.setValue(filter_conf[TdFilterConfigKey.ASPECT_RATIO_LIM][0])
        self.ui.dspinbox_filter_aspect_ratio_high.setValue(filter_conf[TdFilterConfigKey.ASPECT_RATIO_LIM][1])
        self.ui.checkbox_filter_abs_aspect_ratio.setChecked(filter_conf[TdFilterConfigKey.ASPECT_RATIO_GT1])
        self.ui.dspinbox_filter_occupation_low.setValue(filter_conf[TdFilterConfigKey.OCCUPATION_LIM][0])
        self.ui.dspinbox_filter_occupation_high.setValue(filter_conf[TdFilterConfigKey.OCCUPATION_LIM][1])
        self.ui.dspinbox_filter_compactness_low.setValue(filter_conf[TdFilterConfigKey.COMPACTNESS_LIM][0])
        self.ui.dspinbox_filter_compactness_high.setValue(filter_conf[TdFilterConfigKey.COMPACTNESS_LIM][1])
        self.ui.spinbox_filter_width_low.setValue(filter_conf[TdFilterConfigKey.WIDTH_LIM][0])
        self.ui.spinbox_filter_width_high.setValue(filter_conf[TdFilterConfigKey.WIDTH_LIM][1])
        self.ui.spinbox_filter_height_low.setValue(filter_conf[TdFilterConfigKey.HEIGHT_LIM][0])
        self.ui.spinbox_filter_height_high.setValue(filter_conf[TdFilterConfigKey.HEIGHT_LIM][1])
        self.setEnabledForFilter(filter_conf[TdFilterConfigKey.FLAG])
        self.initConnects()
        return

    def initConnects(self):
        ''' 初始化信号与槽的连接
        '''
        self.ui.checkbox_filter_area_lim.stateChanged.connect(self.onActionCheckboxFilterAreaLim)
        self.ui.checkbox_filter_perimeter_lim.stateChanged.connect(self.onActionCheckboxFilterPerimeterLim)
        self.ui.checkbox_filter_aspect_ratio_lim.stateChanged.connect(self.onActionCheckboxFilterAspectRatioLim)
        self.ui.checkbox_filter_occupation_lim.stateChanged.connect(self.onActionCheckboxFilterOccupationLim)
        self.ui.checkbox_filter_compactness_lim.stateChanged.connect(self.onActionCheckboxFilterCompactnessLim)
        self.ui.checkbox_filter_width_lim.stateChanged.connect(self.onActionCheckboxFilterWidthLim)
        self.ui.checkbox_filter_height_lim.stateChanged.connect(self.onActionCheckboxFilterHeightLim)
        self.ui.btn_mser_srcs_add.clicked.connect(self.onActionBtnMserSrcsAddClicked)
        self.ui.btn_mser_srcs_del.clicked.connect(self.onActionBtnMserSrcsDelClicked)

    def getConfiguration(self, flag=0):
        ''' 获得配置信息
        '''
        if flag == 0:
            extconf = TdExtractConfig()
            extconf.setConfigItem(TdExtractConfigKey.DELTA, self.ui.spinbox_mser_delta.value())
            extconf.setConfigItem(TdExtractConfigKey.AREA_MIN, self.ui.spinbox_mser_area_low.value())
            extconf.setConfigItem(TdExtractConfigKey.AREA_MAX, self.ui.spinbox_mser_area_high.value())
            extconf.setConfigItem(TdExtractConfigKey.VARIATION, self.ui.dspinbox_mser_variation.value())
            extconf.setConfigItem(TdExtractConfigKey.VERBOSE, self.ui.checkbox_mser_show_verbose.isChecked())
            extconf.setConfigItem(TdExtractConfigKey.VERBOSE_MORPH, self.ui.checkbox_morph_verbose.isChecked())
            srcs = []
            for i in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(i)
                srcs.append(item.text())
            extconf.setConfigItem(TdExtractConfigKey.SRCS, srcs)
            return extconf.ext_configs
        else:
            fltconf = TdFilterConfig()
            fltconf.setConfigItem('default', TdFilterConfigKey.AREA_LIM, self.ui.spinbox_filter_area_lim.value())
            fltconf.setConfigItem('default', TdFilterConfigKey.PERIMETER_LIM, [self.ui.spinbox_filter_perimeter_low.value(), self.ui.spinbox_filter_perimeter_high.value()])
            fltconf.setConfigItem('default', TdFilterConfigKey.ASPECT_RATIO_LIM, [self.ui.dspinbox_filter_aspect_ratio_low.value(), self.ui.dspinbox_filter_aspect_ratio_high.value()])
            fltconf.setConfigItem('default', TdFilterConfigKey.ASPECT_RATIO_GT1, self.ui.checkbox_filter_abs_aspect_ratio.isChecked())
            fltconf.setConfigItem('default', TdFilterConfigKey.OCCUPATION_LIM, [self.ui.dspinbox_filter_occupation_low.value(), self.ui.dspinbox_filter_occupation_high.value()])
            fltconf.setConfigItem('default', TdFilterConfigKey.COMPACTNESS_LIM, [self.ui.dspinbox_filter_compactness_low.value(), self.ui.dspinbox_filter_compactness_high.value()])
            fltconf.setConfigItem('default', TdFilterConfigKey.WIDTH_LIM, [self.ui.spinbox_filter_width_low.value(), self.ui.spinbox_filter_width_high.value()])
            fltconf.setConfigItem('default', TdFilterConfigKey.HEIGHT_LIM, [self.ui.spinbox_filter_height_low.value(), self.ui.spinbox_filter_height_high.value()])
            flt_flag = []
            if self.ui.checkbox_filter_area_lim.isChecked():
                flt_flag.append(TdFilterCheckType.AREA)
            if self.ui.checkbox_filter_width_lim.isChecked():
                flt_flag.append(TdFilterCheckType.WIDTH)
            if self.ui.checkbox_filter_height_lim.isChecked():
                flt_flag.append(TdFilterCheckType.HEIGHT)
            if self.ui.checkbox_filter_perimeter_lim.isChecked():
                flt_flag.append(TdFilterCheckType.PERIMETER)
            if self.ui.checkbox_filter_aspect_ratio_lim.isChecked():
                flt_flag.append(TdFilterCheckType.ASPECTRATIO)
            if self.ui.checkbox_filter_occupation_lim.isChecked():
                flt_flag.append(TdFilterCheckType.OCCUPIEDRATIO)
            if self.ui.checkbox_filter_compactness_lim.isChecked():
                flt_flag.append(TdFilterCheckType.COMPACTNESS)
            fltconf.setConfigItem('default', TdFilterConfigKey.FLAG, flt_flag)
            return fltconf.flt_configs.get('default', None)

    def setEnabledForFilter(self, flag):
        ''' Filter 参数启用/禁用控制
        '''
        self.ui.checkbox_filter_area_lim.setChecked(bool(TdFilterCheckType.AREA in flag))
        self.ui.spinbox_filter_area_lim.setEnabled(bool(TdFilterCheckType.AREA in flag))
        self.ui.checkbox_filter_perimeter_lim.setChecked(bool(TdFilterCheckType.PERIMETER in flag))
        self.ui.spinbox_filter_perimeter_low.setEnabled(bool(TdFilterCheckType.PERIMETER in flag))
        self.ui.spinbox_filter_perimeter_high.setEnabled(bool(TdFilterCheckType.PERIMETER in flag))
        self.ui.checkbox_filter_aspect_ratio_lim.setChecked(bool(TdFilterCheckType.ASPECTRATIO in flag))
        self.ui.dspinbox_filter_aspect_ratio_low.setEnabled(bool(TdFilterCheckType.ASPECTRATIO in flag))
        self.ui.dspinbox_filter_aspect_ratio_high.setEnabled(bool(TdFilterCheckType.ASPECTRATIO in flag))
        self.ui.checkbox_filter_occupation_lim.setChecked(bool(TdFilterCheckType.OCCUPIEDRATIO in flag))
        self.ui.dspinbox_filter_occupation_low.setEnabled(bool(TdFilterCheckType.OCCUPIEDRATIO in flag))
        self.ui.dspinbox_filter_occupation_high.setEnabled(bool(TdFilterCheckType.OCCUPIEDRATIO in flag))
        self.ui.checkbox_filter_compactness_lim.setChecked(bool(TdFilterCheckType.COMPACTNESS in flag))
        self.ui.dspinbox_filter_compactness_low.setEnabled(bool(TdFilterCheckType.COMPACTNESS in flag))
        self.ui.dspinbox_filter_compactness_high.setEnabled(bool(TdFilterCheckType.COMPACTNESS in flag))
        self.ui.checkbox_filter_width_lim.setChecked(bool(TdFilterCheckType.WIDTH in flag))
        self.ui.spinbox_filter_height_low.setEnabled(bool(TdFilterCheckType.WIDTH in flag))
        self.ui.spinbox_filter_height_high.setEnabled(bool(TdFilterCheckType.WIDTH in flag))
        self.ui.checkbox_filter_height_lim.setChecked(bool(TdFilterCheckType.HEIGHT in flag))
        self.ui.spinbox_filter_height_low.setEnabled(bool(TdFilterCheckType.HEIGHT in flag))
        self.ui.spinbox_filter_height_high.setEnabled(bool(TdFilterCheckType.HEIGHT in flag))

    def setEnabledForFilterSWT(self, bflag=None):
        ''' SWT Filter 参数启用/禁用控制
        '''
        pass

    def onActionCheckboxFilterAreaLim(self, state):
        ''' 响应 CheckBox Filter Area
        '''
        self.ui.spinbox_filter_area_lim.setEnabled(bool(state))

    def onActionCheckboxFilterPerimeterLim(self, state):
        ''' 响应 Checkbox Filter Perimeter Lim
        '''
        self.ui.spinbox_filter_perimeter_low.setEnabled(bool(state))
        self.ui.spinbox_filter_perimeter_high.setEnabled(bool(state))

    def onActionCheckboxFilterAspectRatioLim(self, state):
        ''' 响应 Checkbox Filter Aspect Ratio Lim
        '''
        self.ui.dspinbox_filter_aspect_ratio_low.setEnabled(bool(state))
        self.ui.dspinbox_filter_aspect_ratio_high.setEnabled(bool(state))
        self.ui.checkbox_filter_abs_aspect_ratio.setEnabled(bool(state))

    def onActionCheckboxFilterOccupationLim(self, state):
        ''' 响应 Checkbox Filter Occupation Lim
        '''
        self.ui.dspinbox_filter_occupation_low.setEnabled(bool(state))
        self.ui.dspinbox_filter_occupation_high.setEnabled(bool(state))

    def onActionCheckboxFilterCompactnessLim(self, state):
        ''' 响应 Checkbox Filter Compactness Lim
        '''
        self.ui.dspinbox_filter_compactness_low.setEnabled(bool(state))
        self.ui.dspinbox_filter_compactness_high.setEnabled(bool(state))

    def onActionCheckboxFilterWidthLim(self, state):
        ''' 响应 Checkbox Filter Width Lim
        '''
        self.ui.spinbox_filter_width_low.setEnabled(bool(state))
        self.ui.spinbox_filter_width_high.setEnabled(bool(state))

    def onActionCheckboxFilterHeightLim(self, state):
        ''' 响应 Checkbox Filter Height Lim
        '''
        self.ui.spinbox_filter_height_low.setEnabled(bool(state))
        self.ui.spinbox_filter_height_high.setEnabled(bool(state))

    def onActionCheckboxFilterSwtFilterEnable(self, state):
        ''' 响应 Checkbox Filter Swt Filter Enable
        '''
        pass

    def onActionBtnMserSrcsAddClicked(self):
        ''' 注释
        '''
        grayname = self.ui.combobox_mser_srcs_gray.currentText()
        chartype = self.ui.combobox_mser_srcs_chartype.currentText()
        name = "%s.%s"%(grayname, chartype)
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            if name == item.text():
                return
        self.ui.listWidget.addItem(QListWidgetItem("%s.%s"%(grayname, chartype)))

    def onActionBtnMserSrcsDelClicked(self):
        ''' 注释
        '''
        row = self.ui.listWidget.currentRow()
        self.ui.listWidget.takeItem(row)
