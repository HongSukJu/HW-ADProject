import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Ktalk(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # main layout
        main = QGridLayout()
        # chatting
        self.chatting = Chat()
        # room
        self.roomList = Room()
        self.popup = Popup()
        # friend
        self.friendList = Friend()
        # stackwidget
        self.stackWidget = QStackedWidget()
        self.stackWidget.addWidget(self.friendList)
        self.stackWidget.addWidget(self.roomList)
        self.stackWidget.addWidget(self.chatting)
        # menu bar
        self.friendButton = QPushButton("친구")
        self.chattingButton = QPushButton("채팅")
        # set main layout
        main.addWidget(self.stackWidget, 1, 0, 1, 2)
        main.addWidget(self.friendButton, 2, 0)
        main.addWidget(self.chattingButton, 2, 1)
        self.setLayout(main)

        self.setWindowTitle("Kook Talk")
        self.setGeometry(300, 300, 800, 1000)
        self.show()

        self.friendButton.clicked.connect(self.buttonClicked)
        self.chattingButton.clicked.connect(self.buttonClicked)
        self.roomList.makeRoomButton.clicked.connect(self.makePopUp)

    def buttonClicked(self):
        sender = self.sender()
        if sender.text() == "친구":
            self.stackWidget.setCurrentIndex(0)
        if sender.text() == "채팅":
            self.stackWidget.setCurrentIndex(1)

    def makePopUp(self):

        self.popup.show()
        self.popup.okButton.clicked.connect(self.popup.hide)
        self.popup.cancelButton.clicked.connect(self.popup.hide)

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)

class Chat(Window):

    def __init__(self):
        super().__init__()
        self.temp = QLabel()
        self.chattingBox = QListWidget()
        self.chattingBox.setSelectionMode(QAbstractItemView.NoSelection)
        self.currentFriendBox = QListWidget()
        self.messageText = QLineEdit()
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setRange(0,100)
        self.sld.setMaximum(100)
        self.layout.addWidget(self.chattingBox, 1, 1, 5, 1)
        self.layout.addWidget(self.currentFriendBox, 1, 3, 5, 2)
        self.layout.addWidget(self.messageText, 6, 1, 1, 1)
        self.layout.addWidget(self.sld, 6, 3, 1, 2)

class Room(Window):

    def __init__(self):
        super().__init__()
        self.makeRoomButton = QPushButton("+")
        self.roomBox = QListWidget()
        self.layout.addWidget(self.makeRoomButton, 1, 5)
        self.layout.addWidget(self.roomBox, 2, 1, 1, 5)

class Friend(Window):

    def __init__(self):
        super().__init__()
        self.friendBox = QListWidget()
        self.layout.addWidget(self.friendBox, 1, 1)

class Popup(Window):

    def __init__(self):
        super().__init__()
        self.roomLabel = QLabel("방 이름 : ")
        self.roomValue = QLineEdit()
        self.okButton = QPushButton("확인")
        self.cancelButton = QPushButton("취소")

        self.layout.addWidget(self.roomLabel, 1, 1)
        self.layout.addWidget(self.roomValue, 1, 2, 1, 3)
        self.layout.addWidget(self.okButton, 2, 3)
        self.layout.addWidget(self.cancelButton, 2, 4)

        self.move(300, 300)