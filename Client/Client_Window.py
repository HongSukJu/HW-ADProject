import socketio, pickle
from Client_UI2 import *

class user(Ktalk):

    IF = None
    
    def __init__(self):
        super().__init__()
        self.dataReading()
        self.name = user.IF["name"]
        self.security.nameLabel.setText(self.name)
        self.friend = user.IF["friend"]
        self.Friend.friendBox.addItems(self.friend)
        self.room = ""

        self.start_connection()
    
    def start_connection(self):
        self.sio = socketio.Client()
        self.sio.connect("http://localhost:5000")

        @self.sio.on("system")
        def on_connect(data):
            self.sendMessage(data["message"] + "\n", "system")


        @self.sio.on("msg")
        def on_connect(data):
            self.sendMessage(data["name"] + "\n" * 2 + data["message"] + "\n")

        self.friendList.friendButton.clicked.connect(self.menuButtonClicked)
        self.friendList.chattingButton.clicked.connect(self.menuButtonClicked)
        # self.friendList.
        self.roomList.friendButton.clicked.connect(self.menuButtonClicked)
        self.roomList.chattingButton.clicked.connect(self.menuButtonClicked)
        self.roomList.makeRoomButton.clicked.connect(self.makeRoomButtonClicked)
        self.security.verifyButton.clicked.connect(self.securityCheck)
        self.userInit.okButton.clicked.connect(self.dataReadingException)

    # 아이디/패스워드 체크
    def securityCheck(self):
        if self.security.passwordLine.text() == user.IF["password"] and self.security.idLine.text() == user.IF["id"]:
            self.stackWidget.setCurrentIndex(2)

    # 메뉴바 처리
    def menuButtonClicked(self):
        sender = self.sender()
        if sender.text() == "친구":
            self.stackWidget.setCurrentIndex(2)
        elif sender.text() == "채팅":
            self.stackWidget.setCurrentIndex(3)

    # 방 만들기
    def makeRoomButtonClicked(self):
        sender = self.sender()
        if sender.text() == "+":
            self.userInOut("room") # 채팅방 만들기 구현 후 할게요
            
    # 메세지 보내기
    def sendMessage(self, data, userType=None):
        item = QListWidgetItem()
        item.setText(data)
        if userType == "self":
            item.setTextAlignment(Qt.AlignRight)
        elif userType == "system":
            item.setTextAlignment(Qt.AlignCenter)
        self.chatting.chattingBox.addItem(item)

    # 방 들어가기
    def userInOut(self, room):
        self.sio.emit("roommanager", {
            "type" : "join",
            "name" : self.name,
            "room" : room
        })

    # 메세지 보내기
    def msgToRoom(self, data):
        self.sio.emit("room", data)
        self.sendMessage(data["name"] + "\n" * 2 + data["message"] + "\n", "self")
    
    # 채팅 저장하기 (미구현)
    def writeChat(self):
        pass
            
    # 채팅 불러오기 (미구현)
    def readChat(self):
        pass

    # 사용자 정보 불러오기
    def dataReading(self):
        f = open("DataBase/userInfo.dat", "rb")
        user.IF = pickle.load(f)
        if not user.IF["name"]:
            self.stackWidget.setCurrentIndex(1)
            
    # 사용자 정보 불러오기 예외처리
    def dataReadingException(self):
        myName = self.userInit.nameValue.text()
        myId = self.userInit.idValue.text()
        myPassWord = self.userInit.passwordValue.text()
        myPassWordCheck = self.userInit.passwordCheckValue.text()
        if not myName:
            self.userInit.exceptionAlert.showMessage("이름이 없습니다.", 2000)
            return
        elif not myId:
            self.userInit.exceptionAlert.showMessage("아이디가 없습니다.", 2000)
            return
        elif not myPassWord:
            self.userInit.exceptionAlert.showMessage("패스워드가 없습니다.", 2000)
            return
        elif myPassWord == myPassWordCheck:
            user.IF = {
                'name' : myName,
                'id' : myId,
                'password' : myPassWord,
                'friend' : []
                }
            self.dataWriting()
            self.stackWidget.setCurrentIndex(2)
            self.name = user.IF["name"]
        else:
            self.userInit.exceptionAlert.showMessage("패스워드가 일치하지 않습니다.", 2000)
            return

    # 사용자 정보 저장하기   
    def dataWriting(self):
        f = open("DataBase/userInfo.dat", "wb")
        pickle.dump(user.IF, f)

    def makeFriend(self):
        pass

    # 이거 아직 안됨
    def friendListDelete(self):
        # self.friend.remove(self.friendBox.currentItem())
        # self.friendBox.takeItem(self.friendBox.currentRow())
        # self.friendDelCancelButton.hide()
        # self.friendDelOkButton.hide()
        pass