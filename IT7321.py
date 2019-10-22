import visa
import easygui
visa_dll = "./DLL/visa32.dll"
from PyQt5.QtCore import QObject, pyqtSignal

class IT7321Communication(QObject):
    signalDeviceNum = pyqtSignal(str)
    signalMessage = pyqtSignal(str)
    signalReDraw = pyqtSignal()
    signalChangeGray = pyqtSignal()

    def __init__(self):
        super(IT7321Communication,self).__init__()
        self.deviceNum = ('','')

        #self.inst = pyvisa.resources.usb.USBInstrument

    def searchDevice(self):
        self.rm = visa.ResourceManager()
        self.deviceNum = self.rm.list_resources()

        if self.deviceNum:
            self.signalDeviceNum.emit(self.deviceNum[0])
        #return self.deviceNum[0]  ,image='./background/bk0.png'
        else:
            self.rm.close()
            easygui.msgbox(title='提示', msg='未搜索到设备，请检查IT7321仪器是否打开',ok_button='确定',image="./Gif/09macos00.gif")

    def openDevice(self, device):
        try:
            self.inst = self.rm.open_resource(device)
            self.signalReDraw.emit()

        #print(self.inst)
        except BaseException:
            pass
    def closeDevice(self):
        self.rm.close()
        self.signalChangeGray.emit()

    def DealError(self):
        error = self.inst.query('SYSTem:ERRor?')
        easygui.msgbox(title="命令类型错误", msg=error, ok_button="确定")
        self.inst.write('SYSTem:CLEar')


    def setVoltage(self, vol):
        command = 'VOLTage:IMMediate ' + vol
        self.inst.write(command)
    def queryVoltage(self):
        return self.inst.query('VOLTage?')

    def writeOnly(self, command):
        try:
            self.inst.write(command)
        except BaseException:
            self.DealError()

    def readOnly(self):
        try:
            data = self.inst.read()
            self.signalMessage.emit(data)
        except BaseException:
            pass
    def readWrite(self, command):
        if command.endswith('?'):
            try:
                data = self.inst.query(command)
                self.signalMessage.emit(data)
            except BaseException:
                self.DealError()
        else:
            easygui.msgbox(title="命令类型错误",msg="请输入以“？”结尾的查询命令",ok_button="确定")

    '''
>>> it = IT7321()
Resource Manager of Visa Library at C:\Windows\system32\visa32.dll
>>> device = it.searchDevice()
USB0::0xFFFF::0x7300::800476152746720022::INSTR
>>> it.openDevice(device)
>>> it.setVoltage('220')
>>> it.queryVoltage()
'220.0'
    '''