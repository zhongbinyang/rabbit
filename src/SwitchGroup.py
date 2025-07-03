from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *



class SwitchGroup(QWidget):
    toggled = pyqtSignal(int, bool, str)

    def __init__(self, centralWidget, title, rowCount, colCount, parent=None):
        super(SwitchGroup, self).__init__(parent)
        self.gridLayout = QGridLayout(centralWidget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(0)
        centralWidget.setLayout(self.gridLayout)
        self.groupBox = QGroupBox(centralWidget)
        self.gridLayout.addWidget(self.groupBox)
        self.groupBox.setTitle(title)
        self.groupBox.setStyleSheet(
            "QGroupBox{background-color: rgb(245, 245, 245);\
            border-radius: 10px;\
            border-style:solid;\
            border-width:1px;\
            border-color:rgb(117, 117, 117);}"
        )
        self.groupLayout = QGridLayout(self.groupBox)
        self.groupLayout.setContentsMargins(15, 15, 15, 15)
        self.groupLayout.setSpacing(10)
        self.groupBox.setLayout(self.groupLayout)
        self.switchList = []
        for i in range(colCount):
            for j in range(rowCount):
                centralWidget = QWidget()
                centralWidget.setMinimumSize(50, 30)
                switch = SwitchControl(centralWidget, centralWidget)
                # switch = QPushButton(self.groupBox)
                self.groupLayout.addWidget(switch, i, j)
                self.switchList.append(switch)
                switch.toggled.connect(lambda: self.onToggled())

    def onToggled(self):
        index = self.switchList.index(self.sender())
        if self.switchList[index].bChecked == True:
            self.toggled.emit(index, True, self.switchList[index].textChecked)
        else:
            self.toggled.emit(index, False, self.switchList[index].textNoChecked)

    def setSwitchCheckedText(self, textList):
        l1 = len(textList)
        l2 = len(self.switchList)
        l = min(l1, l2)
        if l1 == 1:
            for switch in self.switchList:
                switch.textChecked = textList[0]
        else:
            for i in range(l):
                self.switchList[i].textChecked = textList[i]

    def setSwitchNoCheckedText(self, textList):
        l1 = len(textList)
        l2 = len(self.switchList)
        l = min(l1, l2)
        if l1 == 1:
            for switch in self.switchList:
                switch.textNoChecked = textList[0]
        else:
            for i in range(l):
                self.switchList[i].textNoChecked = textList[i]

    def setSwitchCheckedColor(self, color):
        for switch in self.switchList:
            switch.checkColor = color

    def setSwitchBackgroundColor(self, color):
        for switch in self.switchList:
            switch.backgroundColor = color


class SwitchControl(QWidget):
    toggled = pyqtSignal(bool, str)

    def __init__(self, centralWidget, parent=None):
        super(SwitchControl, self).__init__(parent)
        self.centralWidget = centralWidget
        self.centralWidget.setObjectName("centralWidget")
        self.centralWidget.setStyleSheet(
            "QWidget{"
            "border-radius: 10px;"
            "border-style:solid;"
            "border-width:0px;"
            "border-color:rgb(220, 235, 235);"
            "font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;"
            "font-weight:bold;"
            "}"
            "QWidget:hover{background-color: rgb(100, 255, 255);}"
        )
        self.centralWidget.setAttribute(Qt.WA_TranslucentBackground)
        self.gridLayout = QGridLayout(centralWidget)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setSpacing(0)
        centralWidget.setLayout(self.gridLayout)
        self.gridLayout.addWidget(self)
        self.nHeight = 16
        self.bChecked = False
        self.radius = 10
        self.margin = 3
        self.checkColor = QColor(0, 205, 205)
        self.disableColor = QColor(245, 245, 245)
        self.backgroundColor = QColor(200, 235, 235)
        self.textColor = QColor(46, 46, 46)
        self.textSize = 16
        self.setCursor(Qt.PointingHandCursor)
        self.textChecked = "开启"
        self.textNoChecked = "关闭"
        self.nY = 0
        self.nX = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimeout)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        painter.save()
        painter.setPen(Qt.NoPen)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
        background = QColor()
        sliderColor = QColor()
        dOpacity = 1
        if self.isEnabled() == True:
            if self.bChecked == True:
                background = self.checkColor
                # sliderColor = self.checkColor
                sliderColor.setRed(int(self.checkColor.red() * 1.2))
                sliderColor.setGreen(int(self.checkColor.green() * 1.2))
                sliderColor.setBlue(int(self.checkColor.blue() * 1.2))
                dOpacity = 1
            else:
                background = self.backgroundColor
                # sliderColor = self.backgroundColor
                sliderColor.setRed(int(self.backgroundColor.red() * 0.9))
                sliderColor.setGreen(int(self.backgroundColor.green() * 0.9))
                sliderColor.setBlue(int(self.backgroundColor.blue() * 0.9))
                dOpacity = 0.8
        else:
            background = self.backgroundColor
            sliderColor = self.backgroundColor
            dOpacity = 0.26
        painter.setBrush(background)
        painter.setOpacity(dOpacity)
        rect = QRect(0, 0, self.width(), self.height())
        side = min(self.width(), self.height())
        path1 = QPainterPath()
        path1.addEllipse(rect.x(), rect.y(), side, side)
        path2 = QPainterPath()
        path2.addEllipse(rect.width() - side, rect.y(), side, side)
        path3 = QPainterPath()
        path3.addRect(rect.x() + side / 2, rect.y(), rect.width() - side, self.height())
        path = path1 + path2 + path3
        painter.drawPath(path)
        sliderWidth = min(self.height(), self.width()) - self.margin * 2
        rect = QRect(int(self.nX + self.margin - self.nHeight / 2), int(self.margin), int(sliderWidth), int(sliderWidth))
        painter.setBrush(sliderColor)
        painter.drawEllipse(rect)
        font = painter.font()
        font.setPixelSize(self.textSize)
        painter.setFont(font)
        painter.setPen(QPen(self.textColor))
        if self.bChecked == True:
            textRect = QRect(0, 0, self.width() - sliderWidth, self.height())
            painter.drawText(textRect, Qt.AlignCenter, self.textChecked)
        else:
            textRect = QRect(sliderWidth, 0, self.width() - sliderWidth, self.height())
            painter.drawText(textRect, Qt.AlignCenter, self.textNoChecked)
        painter.restore()

    def mousePressEvent(self, event):
        if self.isEnabled() == True:
            if event.button() == Qt.LeftButton:
                event.accept()
            else:
                event.ignore()

    def mouseReleaseEvent(self, event):
        if self.isEnabled() == True:
            if event.button() == Qt.LeftButton:
                event.accept()
                self.bChecked = not self.bChecked
                if self.bChecked == True:
                    self.toggled.emit(self.bChecked, self.textChecked)
                else:
                    self.toggled.emit(self.bChecked, self.textNoChecked)
                self.timer.start(5)
            else:
                event.ignore()

    def resizeEvent(self, event):
        self.nHeight = self.height()
        if self.bChecked == True:
            self.nX = self.width() - self.nHeight / 2
        else:
            self.nX = self.nHeight / 2
        self.nY = self.nHeight / 2
        self.update()

    def onTimeout(self):
        if self.bChecked == True:
            if self.nX >= self.width() - self.nHeight / 2:
                self.timer.stop()
            else:
                self.nX = self.nX + 2
        else:
            if self.nX <= self.nHeight / 2:
                self.timer.stop()
            else:
                self.nX = self.nX - 2
        self.update()

    def isToggled(self):
        return self.bChecked

    def setToggled(self, checked):
        self.bChecked = checked
        self.timer.start(5)
