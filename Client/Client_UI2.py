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
        # userinit
        self.userInit = userInit()
        # chatting
        self.chatting = {}
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
        self.stackWidget.addWidget(self.makeFriend)
        # set main layout
        main.addWidget(self.stackWidget, 1, 0, 1, 2)
        self.setLayout(main)

        self.setWindowTitle("Kook Talk")
        self.setGeometry(900, 200, 700, 900)
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
        self.roomNameValue = QLineEdit()
        self.roomNameValue.setPlaceholderText("방 이름")
        self.makeRoomButton = QPushButton("+")
        self.deleteRoomButton = QPushButton("-")
        self.checkRoomButton = QPushButton("확인")
        self.cancleRoomButton = QPushButton("취소")
        self.roomLabel = QLabel("채팅")
        self.roomLabel.setAlignment(Qt.AlignCenter)
        self.roomLabel.setFont(QFont("Arial", 30))
        self.roomBox = QListWidget()
        self.friendButton = QPushButton("친구")
        self.chattingButton = QPushButton("채팅")

        self.layout.addWidget(self.roomLabel, 1, 1)
        self.layout.addWidget(self.roomNameValue, 1, 2, 1, 3)
        self.layout.addWidget(self.makeRoomButton, 1, 6)
        self.layout.addWidget(self.deleteRoomButton, 1, 5)
        self.layout.addWidget(self.checkRoomButton, 1, 6)
        self.layout.addWidget(self.cancleRoomButton, 1, 5)
        self.layout.addWidget(self.roomBox, 2, 1, 1, 6)
        self.layout.addWidget(self.friendButton, 3, 1, 1, 3)
        self.layout.addWidget(self.chattingButton, 3, 4, 1, 3)

        self.setChoiceButtonUnvisible()

    def setChoiceButtonUnvisible(self):
        self.checkRoomButton.setVisible(False)
        self.cancleRoomButton.setVisible(False)

    def setChoiceButtonVisible(self):
        self.checkRoomButton.setVisible(True)
        self.cancleRoomButton.setVisible(True)

class Friend(Window):

    def __init__(self):
        super().__init__()
        self.friendBox = QListWidget()
        self.friendBox.setSelectionMode(QAbstractItemView.NoSelection)
        self.friendLabel = QLabel("친구")
        self.friendLabel.setAlignment(Qt.AlignCenter)
        self.friendLabel.setFont(QFont("Arial", 30))
        self.friendButton = QPushButton("친구")
        self.chattingButton = QPushButton("채팅")
        self.friendMakeButton = QPushButton("+")
        self.friendDelButton = QPushButton("-")
        self.friendDelOkButton = QPushButton("확인")
        self.friendDelCancelButton = QPushButton("취소")

        self.layout.addWidget(self.friendLabel, 1, 1)
        self.layout.addWidget(self.friendDelButton, 1, 5)
        self.layout.addWidget(self.friendMakeButton, 1, 6)
        self.layout.addWidget(self.friendDelOkButton, 1, 5)
        self.layout.addWidget(self.friendDelCancelButton, 1, 6)
        self.layout.addWidget(self.friendBox, 2, 1, 1, 6)
        self.layout.addWidget(self.friendButton, 3, 1, 1, 3)
        self.layout.addWidget(self.chattingButton, 3, 4, 1, 3)

        self.setChoiceButtonUnvisible()

    def setChoiceButtonUnvisible(self):
        self.friendDelOkButton.setVisible(False)
        self.friendDelCancelButton.setVisible(False)

    def setChoiceButtonVisible(self):
        self.friendDelOkButton.setVisible(True)
        self.friendDelCancelButton.setVisible(True)

class MakeFriend(Window):

    def __init__(self):
        super().__init__()
        self.makeFriendLabel = QLabel("친구찾기\n")
        self.makeFriendLabel.setFont(QFont("Arial", 30))
        self.makeFriendLabel.setAlignment(Qt.AlignCenter)
        self.friendLabel = QLabel("아이디 : ")
        self.friendId = QLineEdit()
        self.friendSearch = QPushButton("검색")
        self.backButton = QPushButton("<-")
        self.emptyLabel = QLabel("\n" * 8)

        self.resultLayout = QGridLayout()
        self.resultfriendName = QLabel()
        self.resultfriendName.setAlignment(Qt.AlignCenter)
        self.resultfriendName.setFont(QFont("Arial", 25))
        self.resultfriendId = QLabel()
        self.resultfriendId.setAlignment(Qt.AlignCenter)
        self.okButton = QPushButton("추가")
        self.cancelButton = QPushButton("취소")

        self.resultLayout.addWidget(self.resultfriendName, 1, 1, 1, 2)
        self.resultLayout.addWidget(self.resultfriendId, 2, 1, 1, 2)
        self.resultLayout.addWidget(self.okButton, 3, 1)
        self.resultLayout.addWidget(self.cancelButton, 3, 2)

        self.layout.addWidget(self.backButton, 1, 1)
        self.layout.addWidget(self.makeFriendLabel, 1, 3)
        self.layout.addWidget(self.friendLabel, 2, 1)
        self.layout.addWidget(self.friendId, 2, 2, 1, 3)
        self.layout.addWidget(self.friendSearch, 2, 5)
        self.layout.addWidget(self.emptyLabel, 3, 3)
        self.layout.addLayout(self.resultLayout, 4, 3)
        
        self.layout.setAlignment(Qt.AlignTop)

        self.setLayOutUnvisible()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.friendSearch.click()
    
    def setLayOutUnvisible(self):
        self.resultfriendName.setVisible(False)
        self.resultfriendId.setVisible(False)
        self.okButton.setVisible(False)
        self.cancelButton.setVisible(False)

    def setLayOutVisible(self):
        self.resultfriendName.setVisible(True)
        self.resultfriendId.setVisible(True)
        self.okButton.setVisible(True)
        self.cancelButton.setVisible(True)

    def setLayOutVisibleWithoutButton(self):
        self.resultfriendName.setVisible(True)
        self.resultfriendId.setVisible(True)

class Chat(Window):

    def __init__(self):
        super().__init__()
        self.temp = QLabel()
        self.chattingBox = QListWidget()
        self.currentFriendBox = QListWidget()
        self.messageText = QLineEdit()
        self.sendButton = QPushButton("보내기")

        self.layout.addWidget(self.chattingBox, 1, 1, 1, 5)
        self.layout.addWidget(self.currentFriendBox, 1, 6, 1, 2)
        self.layout.addWidget(self.messageText, 2, 1, 1, 5)
        self.layout.addWidget(self.sendButton, 2, 6, 1, 2)

        self.setWindowTitle("Kook Talk")
        self.setGeometry(300, 300, 700, 900)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.sendButton.click()
 
class Security(Window):

    def __init__(self):
        super().__init__()
        self.welcomeLabel = QLabel("KTalk\n")
        self.welcomeLabel.setFont(QFont("Arial", 40))
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel = QLabel()
        self.nameLabel.setFont(QFont("Arial", 20))
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.idLine = QLineEdit()
        self.idLine.setPlaceholderText("아이디를 입력해주세요.")
        self.passwordLine = QLineEdit()
        self.passwordLine.setPlaceholderText("비밀번호를 입력해주세요.")
        self.verifyButton = QPushButton('확인')

        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.welcomeLabel, 1, 1)
        self.layout.addWidget(self.nameLabel, 2, 1)
        self.layout.addWidget(self.idLine, 3, 1)
        self.layout.addWidget(self.passwordLine, 4, 1)
        self.layout.addWidget(self.verifyButton, 5, 1)
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.verifyButton.click()
