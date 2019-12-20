#!/usr/bin/python

''' Preprocess Display Widget
'''

from tdlib.preprocessing import TdPreprocessing
from gui.app_widgets.basic_display_widget import BasicDisplayWidget
from gui.app_widgets.preprocess_control_widget import PreprocessDisplayCtrlWidget
import gui.app_widgets.common as apw_comm
from gui.app_widgets.verbose_show_widget import VerboseDisplayWidget
from conf.config import TdConfig, TdPrepConfigKeys, AppSettings


class PreprocessDisplayWidget(BasicDisplayWidget):
    ''' 用于显示预处理图像的 Widget 控件
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_panel = None
        self.preprocesser = TdPreprocessing()
        self.cur_config = {}
        self.dr_widget = None
        return

    def paintEvent(self, e):
        ''' 重载绘制函数
        '''
        super().paintEvent(e)
        return

    def doPreprocess(self):
        ''' 进行预处理
        '''
        # 获取参数,进行预处理
        config = self.control_panel.getConfiguration() \
                 if self.control_panel is not None else \
                 TdConfig(AppSettings.config_file_path).getPrepConfig()
        self.preprocesser.setConfig(config)
        self.showVerbose(config)

        # 显示预处理结果

        self.cur_config = config
        return

    def openControlPanel(self):
        ''' 打开参数控制面板
        '''
        if self.control_panel is None:
            self.control_panel = PreprocessDisplayCtrlWidget()
            self.control_panel.ui.btn_ok.clicked.connect(self.doPreprocess)
        self.control_panel.show()
        return

    def setImage(self, qimage):
        ''' 载入图像
        '''
        self.setDisplayQImage(qimage)
        self.preprocesser.rgb_image = apw_comm.img_qt2cv(qimage)
        return

    def showVerbose(self, config):
        ''' 显示 Debug 信息
        '''
        verbose_data_dict = {}
        source = config.get(TdPrepConfigKeys.DEBUG_SOURCE, None)
        if source is None or source == "RGB Image":
            return
        elif source == "Gray":
            retpreped = self.preprocesser.ret_gray
        elif source == "Red Channel":
            retpreped = self.preprocesser.ret_red
        elif source == "Green Channel":
            retpreped = self.preprocesser.ret_green
        elif source == "Blue Channel":
            retpreped = self.preprocesser.ret_blue
        else:
            return
        if not config.get(TdPrepConfigKeys.DEBUG, False):
            verbose_data_dict = {source: retpreped[0],
                                 "Black Chars": retpreped[1],
                                 "Bright Chars": retpreped[2]}
        else:
            for item in self.preprocesser.debug.data:
                verbose_data_dict[item[0]] = item[1]

        if self.dr_widget is None:
            self.dr_widget = VerboseDisplayWidget()

        self.dr_widget.setPrepVerboseData(verbose_data_dict)
        self.dr_widget.show()
