import sys, pickle
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
        # userinit
        self.userInit = userInit()
        # chatting
        self.chatting = Chat()
        # room
        self.roomList = Room()
        # friend
        self.friendList = Friend()
        self.makeFriend = MakeFriend()
        # security
        self.security = Security()
        # stackwidget
        self.stackWidget = QStackedWidget()
        self.stackWidget.addWidget(self.security)
        self.stackWidget.addWidget(self.userInit)
        self.stackWidget.addWidget(self.friendList)
        self.stackWidget.addWidget(self.roomList)
        self.stackWidget.addWidget(self.chatting)
        self.stackWidget.addWidget(self.makeFriend)
        # set main layout
        main.addWidget(self.stackWidget, 1, 0, 1, 2)
        self.setLayout(main)

        self.setWindowTitle("Kook Talk")
        self.setGeometry(300, 300, 700, 900)
        self.show()

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)

class userInit(Window):

    def __init__(self):
        super().__init__()
        self.welcomeLabel = QLabel("처음이시네요!")
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setFont(QFont("Arial", 30, QFont.Bold))
        self.nameLabel = QLabel("이름 : ")
        self.nameValue = QLineEdit()
        self.idLabel = QLabel("아이디 : ")
        self.idValue = QLineEdit()
        self.passwordLabel = QLabel("패스워드 : ")
        self.passwordValue = QLineEdit()
        self.passwordCheckLabel = QLabel("패스워드 확인 : ")
        self.passwordCheckValue =  QLineEdit()
        self.okButton = QPushButton("등록")
        self.exceptionAlert = QStatusBar()

        self.layout.addWidget(self.welcomeLabel, 1, 1, 1, 3)
        self.layout.addWidget(self.nameLabel, 2, 1)
        self.layout.addWidget(self.nameValue, 2, 2, 1, 2)
        self.layout.addWidget(self.idLabel, 3, 1)
        self.layout.addWidget(self.idValue, 3, 2, 1, 2)
        self.layout.addWidget(self.passwordLabel, 4, 1)
        self.layout.addWidget(self.passwordValue, 4, 2, 1, 2)
        self.layout.addWidget(self.passwordCheckLabel, 5, 1)
        self.layout.addWidget(self.passwordCheckValue, 5, 2, 1, 2)
        self.layout.addWidget(self.okButton, 6, 2)

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

    def __init__(self):
        super().__init__()
        self.friendBox = QListWidget()
        self.friendMakeButton = QPushButton("+")
        self.friendButton = QPushButton("친구")
        self.chattingButton = QPushButton("채팅")

        self.layout.addWidget(self.friendMakeButton, 1, 6)
        self.layout.addWidget(self.friendBox, 2, 1, 1, 6)
        self.layout.addWidget(self.friendButton, 3, 1, 1, 3)
        self.layout.addWidget(self.chattingButton, 3, 4, 1, 3)

class MakeFriend(Window):

    def __init__(self):
        super().__init__()
        self.friendLabel = QLabel("닉네임 : ")
        self.friendName = QLineEdit()
        self.friendSearch = QPushButton("검색")
        
        self.resultLayout = QGridLayout()
        self.resultfriendName = QLabel()
        self.okButton = QPushButton()
        self.delButton = QPushButton()

        self.resultLayout.addWidget(self.resultfriendName, 1, 1, 1, 2)
        self.resultLayout.addWidget(self.okButton, 2, 1)
        self.resultLayout.addWidget(self.delButton, 2, 2)

        self.layout.addWidget(self.friendLabel, 1, 1)
        self.layout.addWidget(self.friendName, 2, 1, 1, 2)
        self.layout.addWidget(self.friendSearch, 2, 3)
        self.layout.addLayout(self.resultLayout, 3, 1)

        self.setLayOutUnvisible()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.friendSearch.click()
    
    def setLayOutUnvisible(self):
        self.resultfriendName.setVisible(False)
        self.okButton.setVisible(False)
        self.delButton.setVisible(False)

    def setLayOutVisible(self):
        self.resultfriendName.setVisible(True)
        self.okButton.setVisible(True)
        self.delButton.setVisible(True)

class Chat(Window):

    def __init__(self):
        super().__init__()
        self.temp = QLabel()
        self.chattingBox = QListWidget()
        self.chattingBox.setSelectionMode(QAbstractItemView.NoSelection)
        self.currentFriendBox = QListWidget()
        self.messageText = QLineEdit()
        self.sendButton = QPushButton("보내기")
        self.layout.addWidget(self.chattingBox, 1, 1, 1, 5)
        self.layout.addWidget(self.currentFriendBox, 1, 6, 1, 2)
        self.layout.addWidget(self.messageText, 2, 1, 1, 5)
        self.layout.addWidget(self.sendButton, 2, 6, 1, 2)

        self.setWindowTitle("Kook Talk")
        self.setGeometry(300, 300, 700, 900)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.sendButton.click()
 
class Security(Window):

    def __init__(self):
        super().__init__()
        self.nameLabel = QLabel()
        self.idLine = QLineEdit()
        self.passwordLine = QLineEdit()
        self.verifyButton = QPushButton('확인')

        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.nameLabel, 1, 1)
        self.layout.addWidget(self.idLine, 2, 1)
        self.layout.addWidget(self.passwordLine, 3, 1)
        self.layout.addWidget(self.verifyButton, 2, 2, 2, 1)
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.verifyButton.click()
