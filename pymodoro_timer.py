import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui 
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title='Hello, world!'
        self.left=10
        self.top=10
        self.width=640
        self.height=480
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.statusBar().showMessage('In progress') #Added
        self.show()
if __name__=='__main__':
    app= QApplication(sys.argv)
    ex=App()