import sys, pickle
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Ktalk(QWidget):
    
    def __init__(self):
        super().__init__()
        f = open("DataBase/userInfo.dat","rb")
        self.IF = pickle.load(f)
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
        self.friendList = Friend(self.IF)
        # security
        self.security = Security()
        self.security.namelabel.setText(self.IF['name'])
        # stackwidget
        self.stackWidget = QStackedWidget()
        self.stackWidget.addWidget(self.security)
        self.stackWidget.addWidget(self.friendList)
        self.stackWidget.addWidget(self.roomList)
        #self.stackWidget.addWidget(self.chatting)
        
        # set main layout
        main.addWidget(self.stackWidget, 1, 0, 1, 2)
        self.setLayout(main)

        self.setWindowTitle("Kook Talk")
        self.setGeometry(300, 300, 800, 1000)
        self.show()

        self.friendList.friendButton.clicked.connect(self.buttonClicked)
        self.roomList.friendButton.clicked.connect(self.buttonClicked)
        self.friendList.chattingButton.clicked.connect(self.buttonClicked)
        self.roomList.chattingButton.clicked.connect(self.buttonClicked)
        self.roomList.makeRoomButton.clicked.connect(self.makePopUp)
        self.popup.okButton.clicked.connect(self.showChat)
        self.security.verifyButton.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        sender = self.sender()
        if sender.text() == "친구":
            self.stackWidget.setCurrentIndex(1)
        if sender.text() == "채팅":
            self.stackWidget.setCurrentIndex(2)
        if sender.text() == "확인":
            print('ok')
            if self.security.passwordLine.text() == self.IF['password']:
                self.stackWidget.setCurrentIndex(2)

    def makePopUp(self):

        self.popup.popupValue.clear()
        self.popup.show()
        self.popup.popupLabel.setText("방 이름 : ")
        self.popup.okButton.clicked.connect(self.popup.hide)
        self.popup.cancelButton.clicked.connect(self.popup.hide)

    def showChat(self):

        self.chatting.show()

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
        self.layout.addWidget(self.currentFriendBox, 1, 7, 5, 6)
        self.layout.addWidget(self.messageText, 6, 1, 1, 1)
        self.layout.addWidget(self.sld, 6, 7, 1, 6)

        self.setWindowTitle("Kook Talk")
        self.setGeometry(300, 300, 500, 800)

class Room(Window):

    def __init__(self):
        super().__init__()
        self.makeRoomButton = QPushButton("+")
        self.roomBox = QListWidget()
        self.friendButton = QPushButton("친구")
        self.chattingButton = QPushButton("채팅")
        self.layout.addWidget(self.makeRoomButton, 1, 6)
        self.layout.addWidget(self.roomBox, 2, 1, 1, 6)
        self.layout.addWidget(self.friendButton, 3, 1, 1, 3)
        self.layout.addWidget(self.chattingButton, 3, 4, 1, 3)

class Friend(Window):

    def __init__(self, IF):
        self.IF = IF
        super().__init__()
        self.friendBox = QListWidget()
        self.popup = Popup()
        self.friendButton = QPushButton("친구")
        self.friendAddButton = QPushButton("+")
        self.friendDelButton = QPushButton("-")
        self.chattingButton = QPushButton("채팅")
        self.friendDelOkButton = QPushButton("확인")
        self.friendDelCancelButton = QPushButton("취소")
        self.layout.addWidget(self.friendDelButton, 1, 1)
        self.layout.addWidget(self.friendDelOkButton, 1, 1)
        self.layout.addWidget(self.friendAddButton, 1, 6)
        self.layout.addWidget(self.friendDelCancelButton, 1, 6)
        self.layout.addWidget(self.friendBox, 2, 1, 1, 6)
        self.layout.addWidget(self.friendButton, 3, 1, 1, 3)
        self.layout.addWidget(self.chattingButton, 3, 4, 1, 3)
        self.friendBox.addItems(self.IF['friend'])
        
        self.friendDelCancelButton.hide()
        self.friendDelOkButton.hide()
        
        self.friendAddButton.clicked.connect(self.buttonClicked)
        self.friendDelButton.clicked.connect(self.buttonClicked)
        self.friendDelCancelButton.clicked.connect(self.buttonClicked)
        self.friendDelOkButton.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        sender = self.sender()
        if sender.text() == "+":
            self.makePopUp()
        elif sender.text() == "-":
            self.friendDelCancelButton.show()
            self.friendDelOkButton.show()
        elif sender.text() == "확인":
            self.friendBox.takeItem(self.friendBox.currentRow())
            self.friendDelCancelButton.hide()
            self.friendDelOkButton.hide()
        elif sender.text() == "취소":
            self.friendDelCancelButton.hide()
            self.friendDelOkButton.hide()

    def makePopUp(self):

        self.popup.show()
        self.popup.popupLabel.setText("친구 이름 : ")
        self.popup.okButton.clicked.connect(self.okButtonFuntion)
        self.popup.cancelButton.clicked.connect(self.popup.hide)

    def okButtonFuntion(self):
        self.friendBox.addItem(self.popup.popupValue.text())
        self.popup.hide()

class Popup(Window):

    def __init__(self):
        super().__init__()
        self.popupLabel = QLabel()
        self.popupValue = QLineEdit()
        self.okButton = QPushButton("확인")
        self.cancelButton = QPushButton("취소")

        self.layout.addWidget(self.popupLabel, 1, 1)
        self.layout.addWidget(self.popupValue, 2, 1, 1, 3)
        self.layout.addWidget(self.okButton, 3, 1)
        self.layout.addWidget(self.cancelButton, 3, 3)

        self.move(300, 300)

class Security(Window):

    def __init__(self):
        super().__init__()
        self.namelabel = QLabel()
        self.passwordLine = QLineEdit()
        self.verifyButton = QPushButton('확인')

        self.layout.addWidget(self.namelabel,1,1)
        self.layout.addWidget(self.passwordLine,2,1)
        self.layout.addWidget(self.verifyButton,2,2)
        self.setGeometry(300, 300, 800, 1000)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.verifyButton.click()
