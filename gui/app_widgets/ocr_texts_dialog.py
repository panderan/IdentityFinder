#!/usr/bin/python

''' 弹窗显示OCR识别
'''
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from gui.ui.ocr_texts_ui import Ui_OCRTextsDialog

class OCRTextsDialog(QDialog):
    ''' 弹窗显示指定图像
    '''
    def __init__(self, textlist="", parent=None):
        super().__init__(parent)
        self.ui = Ui_OCRTextsDialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_QuitOnClose, False)
        text = ""
        for i, txt in enumerate(textlist):
            if i > 0:
                text = text + "\n"
            text = text + txt
        self.ui.textedit_ocr_texts.setText(text)
        self.setWindowIcon(QIcon(':/images/ocr.png'))

    def onAction_Btn_OK(self):
        ''' 关闭窗口
        '''
        self.close()
