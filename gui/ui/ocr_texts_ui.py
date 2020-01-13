# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ocr_texts.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OCRTextsDialog(object):
    def setupUi(self, OCRTextsDialog):
        OCRTextsDialog.setObjectName("OCRTextsDialog")
        OCRTextsDialog.resize(483, 354)
        self.verticalLayout = QtWidgets.QVBoxLayout(OCRTextsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textedit_ocr_texts = QtWidgets.QTextEdit(OCRTextsDialog)
        self.textedit_ocr_texts.setReadOnly(True)
        self.textedit_ocr_texts.setObjectName("textedit_ocr_texts")
        self.verticalLayout.addWidget(self.textedit_ocr_texts)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, 0, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_ocr_texts = QtWidgets.QPushButton(OCRTextsDialog)
        self.btn_ocr_texts.setObjectName("btn_ocr_texts")
        self.horizontalLayout.addWidget(self.btn_ocr_texts)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(OCRTextsDialog)
        QtCore.QMetaObject.connectSlotsByName(OCRTextsDialog)

    def retranslateUi(self, OCRTextsDialog):
        _translate = QtCore.QCoreApplication.translate
        OCRTextsDialog.setWindowTitle(_translate("OCRTextsDialog", "OCR Text"))
        self.btn_ocr_texts.setText(_translate("OCRTextsDialog", "OK"))
