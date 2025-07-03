# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PLCfOeBhR.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_PLC(object):
    def setupUi(self, PLC):
        if not PLC.objectName():
            PLC.setObjectName(u"PLC")
        PLC.resize(1066, 876)
        self.verticalLayout_11 = QVBoxLayout(PLC)
        self.verticalLayout_11.setSpacing(5)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_21 = QLabel(PLC)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_27.addWidget(self.label_21)

        self.ip = QLineEdit(PLC)
        self.ip.setObjectName(u"ip")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ip.sizePolicy().hasHeightForWidth())
        self.ip.setSizePolicy(sizePolicy)
        self.ip.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_27.addWidget(self.ip)

        self.label_24 = QLabel(PLC)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_27.addWidget(self.label_24)

        self.port = QSpinBox(PLC)
        self.port.setObjectName(u"port")
        self.port.setMinimumSize(QSize(100, 30))
        self.port.setMaximum(999999)
        self.port.setValue(502)

        self.horizontalLayout_27.addWidget(self.port)

        self.connectPLC = QWidget(PLC)
        self.connectPLC.setObjectName(u"connectPLC")
        self.connectPLC.setMinimumSize(QSize(120, 30))
        self.connectPLC.setMaximumSize(QSize(120, 30))

        self.horizontalLayout_27.addWidget(self.connectPLC)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer)


        self.verticalLayout_11.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.dutBox = QGroupBox(PLC)
        self.dutBox.setObjectName(u"dutBox")
        self.verticalLayout_12 = QVBoxLayout(self.dutBox)
        self.verticalLayout_12.setSpacing(3)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(-1, 20, -1, -1)
        self.widgetJacking = QWidget(self.dutBox)
        self.widgetJacking.setObjectName(u"widgetJacking")
        self.widgetJacking.setMinimumSize(QSize(200, 30))
        self.widgetJacking.setMaximumSize(QSize(200, 30))

        self.verticalLayout_12.addWidget(self.widgetJacking)

        self.widgetClamp1 = QWidget(self.dutBox)
        self.widgetClamp1.setObjectName(u"widgetClamp1")
        self.widgetClamp1.setMinimumSize(QSize(200, 30))
        self.widgetClamp1.setMaximumSize(QSize(200, 30))

        self.verticalLayout_12.addWidget(self.widgetClamp1)

        self.widgetClamp2 = QWidget(self.dutBox)
        self.widgetClamp2.setObjectName(u"widgetClamp2")
        self.widgetClamp2.setMinimumSize(QSize(200, 30))
        self.widgetClamp2.setMaximumSize(QSize(200, 30))

        self.verticalLayout_12.addWidget(self.widgetClamp2)

        self.widgetSideInsertion1 = QWidget(self.dutBox)
        self.widgetSideInsertion1.setObjectName(u"widgetSideInsertion1")
        self.widgetSideInsertion1.setMinimumSize(QSize(200, 30))
        self.widgetSideInsertion1.setMaximumSize(QSize(200, 30))

        self.verticalLayout_12.addWidget(self.widgetSideInsertion1)

        self.widgetSideInsertion2 = QWidget(self.dutBox)
        self.widgetSideInsertion2.setObjectName(u"widgetSideInsertion2")
        self.widgetSideInsertion2.setMinimumSize(QSize(200, 30))
        self.widgetSideInsertion2.setMaximumSize(QSize(200, 30))

        self.verticalLayout_12.addWidget(self.widgetSideInsertion2)

        self.widgetKey1 = QWidget(self.dutBox)
        self.widgetKey1.setObjectName(u"widgetKey1")
        self.widgetKey1.setMinimumSize(QSize(200, 30))
        self.widgetKey1.setMaximumSize(QSize(200, 30))

        self.verticalLayout_12.addWidget(self.widgetKey1)

        self.widgetKey2 = QWidget(self.dutBox)
        self.widgetKey2.setObjectName(u"widgetKey2")
        self.widgetKey2.setMinimumSize(QSize(200, 30))
        self.widgetKey2.setMaximumSize(QSize(200, 30))

        self.verticalLayout_12.addWidget(self.widgetKey2)

        self.widgetStartStop = QWidget(self.dutBox)
        self.widgetStartStop.setObjectName(u"widgetStartStop")
        self.widgetStartStop.setMinimumSize(QSize(0, 30))

        self.verticalLayout_12.addWidget(self.widgetStartStop)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer)


        self.horizontalLayout_12.addWidget(self.dutBox)

        self.sensorBox = QGroupBox(PLC)
        self.sensorBox.setObjectName(u"sensorBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sensorBox.sizePolicy().hasHeightForWidth())
        self.sensorBox.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.sensorBox)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 20, 5, 5)
        self.scrollArea = QScrollArea(self.sensorBox)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.sensor = QWidget()
        self.sensor.setObjectName(u"sensor")
        self.sensor.setGeometry(QRect(0, 0, 806, 778))
        sizePolicy1.setHeightForWidth(self.sensor.sizePolicy().hasHeightForWidth())
        self.sensor.setSizePolicy(sizePolicy1)
        self.scrollArea.setWidget(self.sensor)

        self.gridLayout.addWidget(self.scrollArea, 0, 1, 1, 1)


        self.horizontalLayout_12.addWidget(self.sensorBox)


        self.verticalLayout_11.addLayout(self.horizontalLayout_12)


        self.retranslateUi(PLC)

        QMetaObject.connectSlotsByName(PLC)
    # setupUi

    def retranslateUi(self, PLC):
        PLC.setWindowTitle(QCoreApplication.translate("PLC", u"PLC", None))
        self.label_21.setText(QCoreApplication.translate("PLC", u"IP:", None))
        self.ip.setText(QCoreApplication.translate("PLC", u"192.168.6.6", None))
        self.label_24.setText(QCoreApplication.translate("PLC", u"Port:", None))
        self.dutBox.setTitle(QCoreApplication.translate("PLC", u"Cylinder", None))
        self.sensorBox.setTitle(QCoreApplication.translate("PLC", u"Sensor", None))
    # retranslateUi

