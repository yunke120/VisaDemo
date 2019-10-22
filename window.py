from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import IT7321
import re


m_it7321 = IT7321.IT7321Communication()

class IT7321Demo(QWidget):

    signalButtonWt = pyqtSignal(str)
    signalButtonRd = pyqtSignal()
    signalButtonWtRd = pyqtSignal(str)
    signalButtonOpen = pyqtSignal(str)
    signalButtonOpen_1 = pyqtSignal()

    def __init__(self):
        super(IT7321Demo,self).__init__()
        self.initUI()
        self.name = ''
        self.brush = QtGui.QBrush()
        self.brush.setStyle(Qt.SolidPattern)
        self.brush.setColor(Qt.gray)
        self.parttern = r'\d{1,3}, \d{1,3}'



    def initUI(self):
        #_translate = QtCore.QCoreApplication.translate
        self.setWindowTitle("IT7321测试")
        self.resize(500,300)
        #self.setWindowIcon(QIcon("./leaves_icon/f8.ico"))
        #self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.gridLayout = QtWidgets.QGridLayout()

        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)
        self.textEdit.setStyleSheet("QTextEdit{background-color: rgb(0, 0, 0);\
                                                          color: rgb(0, 255, 0);\
                                                    font - size: 9pt;\
                                                    font - weight: 400;\
                                                    font - style: normal;}")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.hboxlayout_1 = QtWidgets.QHBoxLayout()

        self.labelCommand = QtWidgets.QLabel()
        self.labelCommand.setObjectName("labelCommand")
        self.labelCommand.setText("输入命令:")
        self.labelCommand.setMaximumWidth(100)
        self.hboxlayout_1.addWidget(self.labelCommand)
        self.comBoxInput = QtWidgets.QComboBox()
        self.comBoxInput.setObjectName('comBoxInput')
        self.itemDelegate = QtWidgets.QStyledItemDelegate()
        self.comBoxInput.setItemDelegate(self.itemDelegate)
        self.comBoxInput.setStyleSheet("QComboBox QAbstractItemView{color: rgb(45, 255, 8);"
                                       "background-color: rgb(0, 0, 0);"
                                       "border: 2px solid rgb(0,255,0);}")
        #self.comBoxInput.setStyleSheet("QComboBox QAbstractItemView::item:selected{	background-color: rgba(255, 0, 0);}",)
        self.comBoxInput.setEditable(True)
        self.model = QtGui.QStandardItemModel()
        command = ['SYST:VERS?','SYSTem:ERRor?','SYSTem:CLEar','SYSTem:REMote','SYSTem:LOCal','SYSTem:BEEPer',
                   'CONFig:VOLTage:MINimum **','CONFig:VOLTage:MAXimum **',
                   'CONFig:FREQuency:MINimum **','CONFig:FREQuency:MAXimum **',
                   'CONFig:PROTect:CURRent:RMS **','CONFig:PROTect:CURRent:PEAK **',
                   'FREQuency **','FREQuency?','VOLTage **','VOLTage?','OUTPut 0','OUTPut 1']
        toolTip = {
             0:'该命令用来查询当前使用的 SCPI 命令的版本号',
             1:'该命令用来查询电源的错误信息情况',
             2:'这条命令用于清除出错信息。',
             3:'该命令用来设置电源为远端控制模式',
             4:'该命令设置电源为本地控制模式',
             5:'这条命令用来打开/关闭蜂鸣器，参数为 1|ON 时蜂鸣器打开，按键时蜂鸣器鸣叫',
             6: '该命令配置电压下限值，同仪器面板菜单中的 Volt-Min 设置',
             7: '该命令配置电压上限值，同仪器面板菜单中的 Volt-Max 设置',
             8: '该命令配置频率下限值，同仪器面板菜单的 Freq-Min',
             9: '该命令配置频率上限值，同仪器面板菜单的 Freq-Max',
            10: '配置电流有效值保护点，同仪器面板菜单的 Irms-Protect',
            11: '配置电流峰值保护点，同仪器面板菜单的 Ipeak-Protect',
            12: '该命令设置电源当前输出频率',
            13: '该命令查询电源当前输出频率',
            14: '该命令设定电源输出电压',
            15: '该命令查询电源输出电压',
            16: '该命令用来关闭电源的输出',
            17: '该命令用来打开电源的输出'
        }
        for index, each in enumerate(command):
            self.item = QtGui.QStandardItem(each)
            self.item.setToolTip(toolTip[index])
            self.model.appendRow(self.item)

        self.comBoxInput.setModel(self.model)
        self.hboxlayout_1.addWidget(self.comBoxInput)

        self.gridLayout.addLayout(self.hboxlayout_1, 1, 0, 1, 1)

        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.labelDisplay = QtWidgets.QLabel()
        self.labelDisplay.setObjectName("labelDisplay")
        self.labelDisplay.setFixedWidth(100)
        self.labelDisplay.setFixedHeight(100)

        #self.labelDisplay.setText('搜索设备')

        self.buttonSearch = QtWidgets.QPushButton()
        self.buttonSearch.setObjectName("buttonSearch")
        self.buttonSearch.setText('搜索设备')
        #self.buttonSearch.setStyleSheet("QPushButton{background-color:black; color: white;  border-radius: 10px; border: 2px groove gray;border-style: outset;}")
        self.buttonOpen = QtWidgets.QPushButton()
        self.buttonOpen.setObjectName("buttonOpen")
        self.buttonOpen.setText('打开设备')

        self.buttonWriteOnly = QtWidgets.QPushButton()
        self.buttonWriteOnly.setObjectName("buttonWriteOnly")
        self.buttonWriteOnly.setText('只写')

        self.buttonReadOnly = QtWidgets.QPushButton()
        self.buttonReadOnly.setObjectName("buttonReadOnly")
        self.buttonReadOnly.setText('只读')
        self.buttonReadOnly.setEnabled(False)

        self.buttonWriteRead = QtWidgets.QPushButton()
        self.buttonWriteRead.setObjectName("buttonWriteRead")
        self.buttonWriteRead.setText('读写')

        self.verticalLayout.addWidget(self.labelDisplay)
        self.verticalLayout.addWidget(self.buttonSearch)
        self.verticalLayout.addWidget(self.buttonOpen)
        self.verticalLayout.addWidget(self.buttonWriteOnly)
        self.verticalLayout.addWidget(self.buttonReadOnly)
        self.verticalLayout.addWidget(self.buttonWriteRead)

        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 2, 1)

        self.setLayout(self.gridLayout)

        self.buttonSearch.clicked.connect(m_it7321.searchDevice)
        m_it7321.signalDeviceNum.connect(self.getDeviceNum)
        m_it7321.signalMessage.connect(self.getIT7321Message)
        m_it7321.signalReDraw.connect(self.rePaint)
        m_it7321.signalChangeGray.connect(self.changeGray)
        #self.buttonOpen.clicked.connect(lambda :m_it7321.openDevice(self.name))
        self.signalButtonOpen.connect(m_it7321.openDevice)
        self.signalButtonOpen_1.connect(m_it7321.closeDevice)
        self.buttonOpen.clicked.connect(self.buttonOpenClicked)

        self.buttonWriteOnly.clicked.connect(self.buttonWriteOnlyClicked)
        self.buttonReadOnly.clicked.connect(self.buttonReadOnlyClicked)
        self.buttonWriteRead.clicked.connect(self.buttonReadWriteClicked)
        self.signalButtonWt.connect(m_it7321.writeOnly)
        self.signalButtonRd.connect(m_it7321.readOnly)
        self.signalButtonWtRd.connect(m_it7321.readWrite)

    def buttonOpenClicked(self):
        if self.buttonOpen.text() == "打开设备":
            self.buttonOpen.setText("关闭设备")
            self.signalButtonOpen.emit(self.name)
        elif self.buttonOpen.text() == "关闭设备":
            self.buttonOpen.setText("打开设备")
            self.signalButtonOpen_1.emit()
    def changeGray(self):
        self.brush.setColor(Qt.gray)
        self.update()

    def rePaint(self):
        self.brush.setColor(Qt.green)
        self.update()

    def getDeviceNum(self, num):
        self.textEdit.append(num)
        self.name = num



    def getIT7321Message(self,mes):
        mes = mes.strip()
        self.textEdit.append(mes)

    def buttonWriteOnlyClicked(self):

        try:
            self.buttonReadOnly.setEnabled(True)
            self.signalButtonWt.emit(self.comBoxInput.currentText())
        except BaseException:
            pass
    def buttonReadOnlyClicked(self):
        self.buttonReadOnly.setEnabled(False)
        self.signalButtonRd.emit()

    def buttonReadWriteClicked(self):
        try:
            self.buttonReadOnly.setEnabled(False)
            self.signalButtonWtRd.emit(self.comBoxInput.currentText())
        except BaseException:
            pass


    def paintEvent(self, ev):
        p = QPainter(self)
        p.begin(self)
        #self.brush.setColor(Qt.red)
        p.setBrush(self.brush)
        temp_1 = self.labelDisplay.geometry().topLeft()
        temp_2 = str(temp_1)
        temp_3 = re.search(self.parttern, temp_2).group().split(',')
        x = int(temp_3[0])
        y = int(temp_3[1].strip())
        #print(x,y)

        width = self.labelDisplay.width()
        height = self.labelDisplay.height()
        '''
        if width <= height:
            rect = QRect(x, y, width-2, width-2)
        else:
            rect = QRect(x, y, height - 2, height - 2)
        '''
        rect = QRect(x, y, width, height)
        p.drawEllipse(rect)
        p.end()







