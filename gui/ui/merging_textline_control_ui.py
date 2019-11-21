# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'merging_textline_control.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MergeCtrlWidget(object):
    def setupUi(self, MergeCtrlWidget):
        MergeCtrlWidget.setObjectName("MergeCtrlWidget")
        MergeCtrlWidget.setWindowModality(QtCore.Qt.NonModal)
        MergeCtrlWidget.resize(570, 341)
        self.verticalLayout = QtWidgets.QVBoxLayout(MergeCtrlWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.paramsLayout = QtWidgets.QFormLayout()
        self.paramsLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.paramsLayout.setObjectName("paramsLayout")
        self.label_combined_area_size_lim = QtWidgets.QLabel(MergeCtrlWidget)
        self.label_combined_area_size_lim.setMinimumSize(QtCore.QSize(220, 0))
        self.label_combined_area_size_lim.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_combined_area_size_lim.setObjectName("label_combined_area_size_lim")
        self.paramsLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_combined_area_size_lim)
        self.linedit_combined_area_size_lim = QtWidgets.QLineEdit(MergeCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linedit_combined_area_size_lim.sizePolicy().hasHeightForWidth())
        self.linedit_combined_area_size_lim.setSizePolicy(sizePolicy)
        self.linedit_combined_area_size_lim.setMinimumSize(QtCore.QSize(150, 0))
        self.linedit_combined_area_size_lim.setObjectName("linedit_combined_area_size_lim")
        self.paramsLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.linedit_combined_area_size_lim)
        self.label_overlap_ratio = QtWidgets.QLabel(MergeCtrlWidget)
        self.label_overlap_ratio.setMinimumSize(QtCore.QSize(220, 0))
        self.label_overlap_ratio.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_overlap_ratio.setObjectName("label_overlap_ratio")
        self.paramsLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_overlap_ratio)
        self.dspinbox_overlap_ratio = QtWidgets.QDoubleSpinBox(MergeCtrlWidget)
        self.dspinbox_overlap_ratio.setMaximum(1.0)
        self.dspinbox_overlap_ratio.setSingleStep(0.01)
        self.dspinbox_overlap_ratio.setProperty("value", 0.25)
        self.dspinbox_overlap_ratio.setObjectName("dspinbox_overlap_ratio")
        self.paramsLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.dspinbox_overlap_ratio)
        self.label_distance = QtWidgets.QLabel(MergeCtrlWidget)
        self.label_distance.setMinimumSize(QtCore.QSize(220, 0))
        self.label_distance.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_distance.setObjectName("label_distance")
        self.paramsLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_distance)
        self.dspinbox_distance = QtWidgets.QDoubleSpinBox(MergeCtrlWidget)
        self.dspinbox_distance.setProperty("value", 2.6)
        self.dspinbox_distance.setObjectName("dspinbox_distance")
        self.paramsLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.dspinbox_distance)
        self.label_combined_aspect_ratio_lim = QtWidgets.QLabel(MergeCtrlWidget)
        self.label_combined_aspect_ratio_lim.setMinimumSize(QtCore.QSize(220, 0))
        self.label_combined_aspect_ratio_lim.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_combined_aspect_ratio_lim.setObjectName("label_combined_aspect_ratio_lim")
        self.paramsLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_combined_aspect_ratio_lim)
        self.horizontalLayout_copy = QtWidgets.QHBoxLayout()
        self.horizontalLayout_copy.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_copy.setObjectName("horizontalLayout_copy")
        self.label_combined_aspect_ratio_low = QtWidgets.QLabel(MergeCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_combined_aspect_ratio_low.sizePolicy().hasHeightForWidth())
        self.label_combined_aspect_ratio_low.setSizePolicy(sizePolicy)
        self.label_combined_aspect_ratio_low.setMinimumSize(QtCore.QSize(50, 0))
        self.label_combined_aspect_ratio_low.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_combined_aspect_ratio_low.setObjectName("label_combined_aspect_ratio_low")
        self.horizontalLayout_copy.addWidget(self.label_combined_aspect_ratio_low)
        self.dspinbox_combined_aspect_ratio_low = QtWidgets.QDoubleSpinBox(MergeCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dspinbox_combined_aspect_ratio_low.sizePolicy().hasHeightForWidth())
        self.dspinbox_combined_aspect_ratio_low.setSizePolicy(sizePolicy)
        self.dspinbox_combined_aspect_ratio_low.setMinimumSize(QtCore.QSize(100, 0))
        self.dspinbox_combined_aspect_ratio_low.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dspinbox_combined_aspect_ratio_low.setMaximum(10.0)
        self.dspinbox_combined_aspect_ratio_low.setSingleStep(0.1)
        self.dspinbox_combined_aspect_ratio_low.setObjectName("dspinbox_combined_aspect_ratio_low")
        self.horizontalLayout_copy.addWidget(self.dspinbox_combined_aspect_ratio_low)
        self.label_combined_aspect_ratio_high = QtWidgets.QLabel(MergeCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_combined_aspect_ratio_high.sizePolicy().hasHeightForWidth())
        self.label_combined_aspect_ratio_high.setSizePolicy(sizePolicy)
        self.label_combined_aspect_ratio_high.setMinimumSize(QtCore.QSize(50, 0))
        self.label_combined_aspect_ratio_high.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_combined_aspect_ratio_high.setObjectName("label_combined_aspect_ratio_high")
        self.horizontalLayout_copy.addWidget(self.label_combined_aspect_ratio_high)
        self.dspinbox_combined_aspect_ratio_high = QtWidgets.QDoubleSpinBox(MergeCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dspinbox_combined_aspect_ratio_high.sizePolicy().hasHeightForWidth())
        self.dspinbox_combined_aspect_ratio_high.setSizePolicy(sizePolicy)
        self.dspinbox_combined_aspect_ratio_high.setMinimumSize(QtCore.QSize(100, 0))
        self.dspinbox_combined_aspect_ratio_high.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dspinbox_combined_aspect_ratio_high.setMaximum(1000.0)
        self.dspinbox_combined_aspect_ratio_high.setProperty("value", 100.0)
        self.dspinbox_combined_aspect_ratio_high.setObjectName("dspinbox_combined_aspect_ratio_high")
        self.horizontalLayout_copy.addWidget(self.dspinbox_combined_aspect_ratio_high)
        self.paramsLayout.setLayout(6, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_copy)
        self.label_strategy = QtWidgets.QLabel(MergeCtrlWidget)
        self.label_strategy.setMinimumSize(QtCore.QSize(220, 0))
        self.label_strategy.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_strategy.setObjectName("label_strategy")
        self.paramsLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_strategy)
        self.combobox_strategy = QtWidgets.QComboBox(MergeCtrlWidget)
        self.combobox_strategy.setObjectName("combobox_strategy")
        self.combobox_strategy.addItem("")
        self.combobox_strategy.addItem("")
        self.combobox_strategy.addItem("")
        self.paramsLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.combobox_strategy)
        self.checkbox_show_verbsoe = QtWidgets.QCheckBox(MergeCtrlWidget)
        self.checkbox_show_verbsoe.setObjectName("checkbox_show_verbsoe")
        self.paramsLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.checkbox_show_verbsoe)
        self.label_merge_text_line = QtWidgets.QLabel(MergeCtrlWidget)
        self.label_merge_text_line.setObjectName("label_merge_text_line")
        self.paramsLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_merge_text_line)
        self.label_morph = QtWidgets.QLabel(MergeCtrlWidget)
        self.label_morph.setObjectName("label_morph")
        self.paramsLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_morph)
        self.label_morph_area_size_lim = QtWidgets.QLabel(MergeCtrlWidget)
        self.label_morph_area_size_lim.setMinimumSize(QtCore.QSize(220, 0))
        self.label_morph_area_size_lim.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_morph_area_size_lim.setObjectName("label_morph_area_size_lim")
        self.paramsLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_morph_area_size_lim)
        self.spinbox_morph_area_size_lim = QtWidgets.QSpinBox(MergeCtrlWidget)
        self.spinbox_morph_area_size_lim.setProperty("value", 9)
        self.spinbox_morph_area_size_lim.setObjectName("spinbox_morph_area_size_lim")
        self.paramsLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinbox_morph_area_size_lim)
        self.verticalLayout.addLayout(self.paramsLayout)
        self.btn_ok = QtWidgets.QPushButton(MergeCtrlWidget)
        self.btn_ok.setObjectName("btn_ok")
        self.verticalLayout.addWidget(self.btn_ok)

        self.retranslateUi(MergeCtrlWidget)
        QtCore.QMetaObject.connectSlotsByName(MergeCtrlWidget)

    def retranslateUi(self, MergeCtrlWidget):
        _translate = QtCore.QCoreApplication.translate
        MergeCtrlWidget.setWindowTitle(_translate("MergeCtrlWidget", "Preprocess Control Panel"))
        self.label_combined_area_size_lim.setText(_translate("MergeCtrlWidget", "Combined Area Size Lim :"))
        self.linedit_combined_area_size_lim.setText(_translate("MergeCtrlWidget", "400000"))
        self.label_overlap_ratio.setText(_translate("MergeCtrlWidget", "Overlap Ratio :"))
        self.label_distance.setText(_translate("MergeCtrlWidget", "Distance :"))
        self.label_combined_aspect_ratio_lim.setText(_translate("MergeCtrlWidget", "Combined Aspect Ratio Lim :"))
        self.label_combined_aspect_ratio_low.setText(_translate("MergeCtrlWidget", "Low:"))
        self.label_combined_aspect_ratio_high.setText(_translate("MergeCtrlWidget", "High:"))
        self.label_strategy.setText(_translate("MergeCtrlWidget", "Strategy :"))
        self.combobox_strategy.setItemText(0, _translate("MergeCtrlWidget", "horizon"))
        self.combobox_strategy.setItemText(1, _translate("MergeCtrlWidget", "vertical"))
        self.combobox_strategy.setItemText(2, _translate("MergeCtrlWidget", "default"))
        self.checkbox_show_verbsoe.setText(_translate("MergeCtrlWidget", "Show Verbose"))
        self.label_merge_text_line.setText(_translate("MergeCtrlWidget", "Merge Text Line："))
        self.label_morph.setText(_translate("MergeCtrlWidget", "Morph："))
        self.label_morph_area_size_lim.setText(_translate("MergeCtrlWidget", "Area Size Lima :"))
        self.btn_ok.setText(_translate("MergeCtrlWidget", "OK"))
