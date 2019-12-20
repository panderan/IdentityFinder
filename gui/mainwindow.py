#!/usr/bin/python

'''
mainwindow.py
'''
import logging
from PyQt5.QtCore import Qt, QFile, QIODevice, QTextStream
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QLabel
from PyQt5.QtGui import QImage, QIcon
import gui.ui.app_ui as ui
import gui.resources.resources
from gui.app_widgets.preprocess_display_widget import PreprocessDisplayWidget
from gui.app_widgets.extract_display_widget import ExtractDisplayWidget
from gui.app_widgets.merging_display_widget import MergeDisplayWidget
from conf.config import TdConfig, AppSettings, TdExtractConfigKey
from tdlib.extraction import ExtractDirection

logger = logging.getLogger(__name__)



class AppMainWindow(QMainWindow):
    '''
    AppMainWindow
    '''
    def __init__(self):
        super().__init__()
        self.strings = {}
        self.default_display_widget = None
        self.preprocess_display_widget = None
        self.extract_display_widget = None
        self.merging_display_widget = None
        self.ldp_display_widget = None
        # 建立主窗体
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(':/images/icon.png'))
        self.default_display_widget = self.ui.display_widget

        self.initConnects()
        self.initResources()

        self.statusbar_label_confile = QLabel()
        self.statusbar_label_curstage = QLabel()
        self.ui.statusbar.addPermanentWidget(self.statusbar_label_curstage)
        self.ui.statusbar.addPermanentWidget(self.statusbar_label_confile)
        self.ui.toolBar.setVisible(False)

        self.createPrepDisplayWidget()
        self.createExtractDisplayWidget()
        self.createMergeDisplayWidget()
        self.createIdentifyWithFeatureDisplayWidget()

        self.onActionIdentifyWithFeature()
        self.updateStatusBar()
        return

    def initConnects(self):
        '''
        初始化信号和槽
        '''
        self.ui.action_about.triggered.connect(self.onActionAbout)
        self.ui.action_open.triggered.connect(self.onActionOpen)
        self.ui.action_open_current_control_panel.triggered.connect(self.onActionOpenCurrentControlPanel)
        self.ui.action_preprocessing.triggered.connect(self.onActionPreprocessing)
        self.ui.action_extract_connect_domain.triggered.connect(self.onActionExtratConnectDomain)
        self.ui.action_merging_text_line.triggered.connect(self.onActionMergingTextLine)
        self.ui.action_identify_with_feature.triggered.connect(self.onActionIdentifyWithFeature)
        self.ui.action_load_config.triggered.connect(self.onActionLoadConf)
        return

    def initResources(self):
        '''
        初始化资源文件
        '''
        strfile = QFile(':/string/strings')
        strfile.open(QIODevice.ReadOnly | QIODevice.Text)
        ts = QTextStream(strfile)
        key, value = "", ""
        while not ts.atEnd():
            line = ts.readLine()
            if len(line) < 1:
                continue
            if line[0] == '@':
                if key != "":
                    self.strings[key] = value
                    key, value = "", ""
                key = line[1:]
            else:
                value += line
        self.strings[key] = value
        strfile.close()
        return

    def updateStatusBar(self):
        ''' 更新状态栏信息
        '''
        self.statusbar_label_confile.setText(AppSettings.config_file_path.split('/')[-1])
        self.statusbar_label_curstage.setText(AppSettings.curstage)

    def onActionAbout(self):
        ''' About 响应函数
        '''
        QMessageBox.about(self, "About", self.strings["ABOUT"])
        return

    def onActionOpen(self):
        ''' Open 响应函数
        '''
        fname, _ = QFileDialog.getOpenFileName(self, "Open file", \
                                        '~', "Image files (*.jpg *.gif *.png)")
        if fname == '':
            return
        input_image = QImage(fname).convertToFormat(QImage.Format_RGB32)
        self.preprocess_display_widget.setImage(input_image)
        return

    def onActionOpenCurrentControlPanel(self):
        '''
        OpenCurrentControlPanel 响应函数
        '''
        self.ui.display_widget.openControlPanel()
        return

    def onActionLoadConf(self):
        ''' 载入配置文件
        '''
        fname, _ = QFileDialog.getOpenFileName(self, "Open Config file", \
                                        '~', "config files (*.yaml)")
        AppSettings.config_file_path = fname
        if self.preprocess_display_widget.control_panel is not None:
            self.preprocess_display_widget.control_panel.close()
        if self.extract_display_widget.control_panel is not None:
            self.extract_display_widget.control_panel.close()
        if self.merging_display_widget.control_panel is not None:
            self.merging_display_widget.control_panel.close()
        if self.ldp_display_widget.control_panel is not None:
            self.ldp_display_widget.control_panel.close()
        self.updateStatusBar()
        return

    def _onlyShow(self, tgtname):
        ''' 只显示某一模块的 widget
        '''
        data = [{'name':"prep",
                 'obj': self.preprocess_display_widget,
                 'checked_obj':self.ui.action_preprocessing},
                {'name':"extract",
                 'obj': self.extract_display_widget,
                 'checked_obj':self.ui.action_extract_connect_domain},
                {'name':"merge",
                 'obj': self.merging_display_widget,
                 'checked_obj':self.ui.action_merging_text_line},
                {'name':"feature",
                 'obj': self.ldp_display_widget,
                 'checked_obj':self.ui.action_identify_with_feature}]
        for item in data:
            if item['name'] == tgtname:
                item['obj'].show()
                item['checked_obj'].setChecked(True)
            else:
                if item['obj'] is not None:
                    item['obj'].hide()
                item['checked_obj'].setChecked(False)

    def createPrepDisplayWidget(self):
        ''' 创建 Prep Display Widget
        '''
        if self.preprocess_display_widget is None:
            self.preprocess_display_widget = PreprocessDisplayWidget(self)
            self.preprocess_display_widget.setSizePolicy(self.default_display_widget.sizePolicy())
            self.preprocess_display_widget.setObjectName("prep_display_widget")
            self.preprocess_display_widget.hide()

    def createExtractDisplayWidget(self):
        ''' 创建 Extract Display Widget
        '''
        if self.extract_display_widget is None:
            self.extract_display_widget = ExtractDisplayWidget(self)
            self.extract_display_widget.setSizePolicy(self.default_display_widget.sizePolicy())
            self.extract_display_widget.setObjectName("extract_display_widget")
            self.extract_display_widget.requireData.connect(self.onActionExtractorRequireData, Qt.DirectConnection)
            self.extract_display_widget.hide()

    def createMergeDisplayWidget(self):
        ''' 创建 Merge Display Widget
        '''
        if self.merging_display_widget is None:
            self.merging_display_widget = MergeDisplayWidget(self)
            self.merging_display_widget.setSizePolicy(self.default_display_widget.sizePolicy())
            self.merging_display_widget.setObjectName("merge_display_widget")
            self.merging_display_widget.requireData.connect(self.onActionMergerRequireData, Qt.DirectConnection)
            self.merging_display_widget.hide()

    def createIdentifyWithFeatureDisplayWidget(self):
        ''' 创建 IdentifyWithFeature 窗体
        '''
        if self.ldp_display_widget is None:
            self.ldp_display_widget = MergeDisplayWidget(self)
            self.ldp_display_widget.setSizePolicy(self.default_display_widget.sizePolicy())
            self.ldp_display_widget.setObjectName("feature_display_widget")
            self.ldp_display_widget.hide()

    def onActionPreprocessing(self):
        ''' Stage->Preprocessing 菜单响应函数，将预处理窗口设置为当前窗口
        '''
        self.createPrepDisplayWidget()
        old_display_widget_item = self.ui.verticalLayout.itemAt(0)
        self.ui.verticalLayout.removeItem(old_display_widget_item)
        self.ui.verticalLayout.insertWidget(0, self.preprocess_display_widget)
        self.ui.display_widget = self.preprocess_display_widget
        self.statusbar_label_curstage.setText("preprocessing")
        self._onlyShow("prep")
        return

    def onActionExtratConnectDomain(self):
        ''' Stage->Extract Connect Domain 菜单响应函数，将连通域提取窗口设置为当前窗口
        '''
        self.createExtractDisplayWidget()
        old_display_widget_item = self.ui.verticalLayout.itemAt(0)
        self.ui.verticalLayout.removeItem(old_display_widget_item)
        self.ui.verticalLayout.insertWidget(0, self.extract_display_widget)
        self.ui.display_widget = self.extract_display_widget
        self.statusbar_label_curstage.setText("extract")
        self._onlyShow("extract")
        return

    def onActionMergingTextLine(self):
        ''' Stage->Merging Text Line 菜单响应函数，将文本行合并窗口设置为当前窗口
        '''
        self.createMergeDisplayWidget()
        old_display_widget_item = self.ui.verticalLayout.itemAt(0)
        self.ui.verticalLayout.removeItem(old_display_widget_item)
        self.ui.verticalLayout.insertWidget(0, self.merging_display_widget)
        self.ui.display_widget = self.merging_display_widget
        self.statusbar_label_curstage.setText("merging")
        self._onlyShow("merge")
        return

    def onActionIdentifyWithFeature(self):
        ''' Stage->Identify with Feature 菜单响应函数，将特征鉴别窗口设置为当前窗口
        '''
        self.createIdentifyWithFeatureDisplayWidget()
        old_display_widget_item = self.ui.verticalLayout.itemAt(0)
        self.ui.verticalLayout.removeItem(old_display_widget_item)
        self.ui.verticalLayout.insertWidget(0, self.ldp_display_widget)
        self.ui.display_widget = self.ldp_display_widget
        self.statusbar_label_curstage.setText("location")
        self._onlyShow("feature")
        return

    def onActionExtractorRequireData(self, srcs, extconf):
        ''' 获取 Extracter 所需的数据
        Args:
            srcs 源图像
            extconf 配置信息
        '''
        # 设置预处理
        config = TdConfig(AppSettings.config_file_path).getPrepConfig() \
                 if self.preprocess_display_widget.control_panel is None else \
                 self.preprocess_display_widget.control_panel.getConfiguration()
        self.preprocess_display_widget.preprocesser.setConfig(config)

        # 初始化配置
        posi_extconf = extconf.copy()
        nega_extconf = extconf.copy()
        posi_extconf[TdExtractConfigKey.DIRECTION] = ExtractDirection.Positive
        nega_extconf[TdExtractConfigKey.DIRECTION] = ExtractDirection.Negitive

        # 准备预处理后图像
        images, image = [], []
        for src in srcs:
            image.clear()
            grayname, chartype = src.split('.')
            if grayname == "Gray":
                ret = self.preprocess_display_widget.preprocesser.ret_gray
            elif grayname == "Red":
                ret = self.preprocess_display_widget.preprocesser.ret_red
            elif grayname == "Green":
                ret = self.preprocess_display_widget.preprocesser.ret_green
            elif grayname == "Blue":
                ret = self.preprocess_display_widget.preprocesser.ret_blue
            else:
                ret = None

            if chartype == "Both" or chartype == "Black":
                image.append({'name':"%s.Black"%grayname,
                              'image':ret[1],
                              'conf':posi_extconf})
            if chartype == "Both" or chartype == "Bright":
                image.append({'name':"%s.Bright"%grayname,
                              'image':ret[2],
                              'conf':nega_extconf})
            images.extend(image.copy())

        self.extract_display_widget.input_images = images
        msg = "Data is fed for extractor"
        logger.info(msg)

    def onActionMergerRequireData(self):
        ''' 获取 Merger 所需的数据
        '''
        self.merging_display_widget.input_image = self.extract_display_widget.getResult()
        self.merging_display_widget.color_image = self.preprocess_display_widget.preprocesser.rgb_image
        msg = "Data is fed for merger"
        logger.info(msg)
