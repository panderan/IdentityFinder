# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'svc_control.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SVCCtrlWidget(object):
    def setupUi(self, SVCCtrlWidget):
        SVCCtrlWidget.setObjectName("SVCCtrlWidget")
        SVCCtrlWidget.setWindowModality(QtCore.Qt.NonModal)
        SVCCtrlWidget.resize(792, 371)
        self.verticalLayout = QtWidgets.QVBoxLayout(SVCCtrlWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_top = QtWidgets.QVBoxLayout()
        self.layout_top.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.layout_top.setContentsMargins(0, -1, -1, -1)
        self.layout_top.setObjectName("layout_top")
        self.label_svc = QtWidgets.QLabel(SVCCtrlWidget)
        self.label_svc.setObjectName("label_svc")
        self.layout_top.addWidget(self.label_svc)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_svc_conf_path = QtWidgets.QLabel(SVCCtrlWidget)
        self.label_svc_conf_path.setMinimumSize(QtCore.QSize(220, 0))
        self.label_svc_conf_path.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_svc_conf_path.setObjectName("label_svc_conf_path")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_svc_conf_path)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.linedit_svc_conf_path = QtWidgets.QLineEdit(SVCCtrlWidget)
        self.linedit_svc_conf_path.setObjectName("linedit_svc_conf_path")
        self.horizontalLayout.addWidget(self.linedit_svc_conf_path)
        self.btn_svc_conf_path = QtWidgets.QPushButton(SVCCtrlWidget)
        self.btn_svc_conf_path.setObjectName("btn_svc_conf_path")
        self.horizontalLayout.addWidget(self.btn_svc_conf_path)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_config_context = QtWidgets.QLabel(SVCCtrlWidget)
        self.label_config_context.setObjectName("label_config_context")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_config_context)
        self.line = QtWidgets.QFrame(SVCCtrlWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.line)
        self.layout_top.addLayout(self.formLayout)
        self.layout_top.setStretch(1, 1)
        self.verticalLayout.addLayout(self.layout_top)
        self.btn_ok = QtWidgets.QPushButton(SVCCtrlWidget)
        self.btn_ok.setObjectName("btn_ok")
        self.verticalLayout.addWidget(self.btn_ok)

        self.retranslateUi(SVCCtrlWidget)
        QtCore.QMetaObject.connectSlotsByName(SVCCtrlWidget)

    def retranslateUi(self, SVCCtrlWidget):
        _translate = QtCore.QCoreApplication.translate
        SVCCtrlWidget.setWindowTitle(_translate("SVCCtrlWidget", "SVC Control Panel"))
        self.label_svc.setText(_translate("SVCCtrlWidget", "SVC："))
        self.label_svc_conf_path.setText(_translate("SVCCtrlWidget", "SVC Conf Path :"))
        self.btn_svc_conf_path.setText(_translate("SVCCtrlWidget", "Brower"))
        self.label_config_context.setText(_translate("SVCCtrlWidget", "Config Context:"))
        self.btn_ok.setText(_translate("SVCCtrlWidget", "OK"))
