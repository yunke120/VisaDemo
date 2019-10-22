import sys
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow
import window

if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    ui = window.IT7321Demo()
    ui.show()
    sys.exit(myapp.exec())

