import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Ktalk(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.chattingBox = QListWidget()
        self.roomBox = QListWidget()
        self.messageText = QLineEdit()
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setRange(0,100)
        self.sld.setMaximum(100)
        # change
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.chattingBox,1,1,5,1)
        grid.addWidget(self.roomBox,1,3,5,2)
        grid.addWidget(self.messageText,6,1,1,1)
        grid.addWidget(self.sld,6,3,1,2)
        self.setLayout(grid)

        self.setWindowTitle("Kook Talk")
        self.setGeometry(300,300,800,1000)
        self.show()