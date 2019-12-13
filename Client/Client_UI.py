import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtTest import QTest

class Ktalk(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # main layout
        main = QGridLayout()
        main.setSpacing(0)
        main.setContentsMargins(0, 0, 0, 0)
        # startlogo
        self.logo = StartLogo()
        # userinit
        self.userInit = UserInit()
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
        self.stackWidget.addWidget(self.logo)
        self.stackWidget.addWidget(self.security)
        self.stackWidget.addWidget(self.userInit)
        self.stackWidget.addWidget(self.friendList)
        self.stackWidget.addWidget(self.roomList)
        self.stackWidget.addWidget(self.makeFriend)

        # set main layout
        main.addWidget(self.stackWidget, 1, 0, 1, 2)
        self.setLayout(main)

        self.setWindowTitle("Kook Talk")
        self.setGeometry(900, 100, 700, 900)
        self.show()

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

class FaderWidget(QWidget):

    def __init__(self, old_widget, new_widget):
    
        QWidget.__init__(self, new_widget)
        
        self.old_pixmap = QPixmap(700, 900)
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0
        
        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(1000)
        self.timeline.start()
        
        self.resize(700, 900)

    def paintEvent(self, event):
    
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()
    
    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()        

class StartLogo(Window):

    def __init__(self):
        super().__init__()
        self.image = QPixmap("./res/logo.png")
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(self.image)
        self.imageLabel.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.imageLabel, 1, 1)

        self.setStyleSheet("background-color: white;")

class UserInit(Window):

    def __init__(self):
        super().__init__()
        self.welcomeLabel = QLabel("처음이시네요!")
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setFont(QFont("Arial", 30))
        self.nameLabel = QLabel("이름 : ")
        self.nameValue = QLineEdit()
        self.idLabel = QLabel("아이디 : ")
        self.idValue = QLineEdit()
        self.passwordLabel = QLabel("패스워드 : ")
        self.passwordValue = QLineEdit()
        self.passwordValue.setEchoMode(QLineEdit.Password)
        self.passwordCheckLabel = QLabel("패스워드 확인 : ")
        self.passwordCheckValue =  QLineEdit()
        self.passwordCheckValue.setEchoMode(QLineEdit.Password)
        self.okButton = QPushButton("등록")
        self.exceptionAlert = QStatusBar()
        self.exceptionAlert.setStyleSheet("QStatusBar{padding-left:15px;color:blue;font-weight:bold;}")

        self.layout.addWidget(self.welcomeLabel, 1, 1, 1, 3)
        self.layout.addWidget(self.exceptionAlert, 2, 1, 1, 3)
        self.layout.addWidget(self.nameLabel, 3, 1)
        self.layout.addWidget(self.nameValue, 3, 2, 1, 2)
        self.layout.addWidget(self.idLabel, 4, 1)
        self.layout.addWidget(self.idValue, 4, 2, 1, 2)
        self.layout.addWidget(self.passwordLabel, 5, 1)
        self.layout.addWidget(self.passwordValue, 5, 2, 1, 2)
        self.layout.addWidget(self.passwordCheckLabel, 6, 1)
        self.layout.addWidget(self.passwordCheckValue, 6, 2, 1, 2)
        self.layout.addWidget(self.okButton, 7, 2)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(100, 100, 100, 100)

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
        self.roomBox.setSelectionMode(QAbstractItemView.NoSelection)
        self.friendButtonOffPixmap = QPixmap("./res/user1.png")
        self.friendButtonIcon = QIcon(self.friendButtonOffPixmap)
        self.friendButton = QPushButton()
        self.friendButton.setIcon(self.friendButtonIcon)
        self.friendButton.setIconSize(QSize(50, 50))
        self.chattingButtonOnPixmap = QPixmap("./res/chat2.png")
        self.chattingButtonIcon = QIcon(self.chattingButtonOnPixmap)
        self.chattingButton = QPushButton()
        self.chattingButton.setIcon(self.chattingButtonIcon)
        self.chattingButton.setIconSize(QSize(50, 50))

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
        self.friendButtonOnPixmap = QPixmap("./res/user2.png")
        self.friendButtonIcon = QIcon(self.friendButtonOnPixmap)
        self.friendButton = QPushButton()
        self.friendButton.setIcon(self.friendButtonIcon)
        self.friendButton.setIconSize(QSize(50, 50))
        self.chattingButtonOffPixmap = QPixmap("./res/chat1.png")
        self.chattingButtonIcon = QIcon(self.chattingButtonOffPixmap)
        self.chattingButton = QPushButton()
        self.chattingButton.setIcon(self.chattingButtonIcon)
        self.chattingButton.setIconSize(QSize(50, 50))
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
        self.sendButtonPixmap = QPixmap("./res/send.png")
        self.sendButtonIcon = QIcon(self.sendButtonPixmap)
        self.sendButton = QPushButton()
        self.sendButton.setIcon(self.sendButtonIcon)

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
        self.passwordLine.setEchoMode(QLineEdit.Password)
        self.verifyButton = QPushButton('확인')

        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.welcomeLabel, 1, 1)
        self.layout.addWidget(self.nameLabel, 2, 1)
        self.layout.addWidget(self.idLine, 3, 1)
        self.layout.addWidget(self.passwordLine, 4, 1)
        self.layout.addWidget(self.verifyButton, 5, 1)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(100, 100, 100, 100)
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.verifyButton.click()