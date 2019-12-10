import socketio, pickle
from Client_UI2 import *

class user(Ktalk):

    IF = None
    
    def __init__(self):
        super().__init__()
        self.dataReading()
        self.name = user.IF["name"]
        self.id = user.IF["id"]
        self.friend = user.IF["friend"]
        self.room = ""
        # 다른 방법이 있을까
        self.currentFriend = ""
        self.currentFriendCheck = ""
        self.currentFriendName = ""

        self.security.nameLabel.setText(self.name + "\n")
        self.friendList.friendBox.addItems(self.friend)

        self.start_connection()
    
    def start_connection(self):
        self.sio = socketio.Client()
        self.sio.connect("http://10.30.118.179:5000")

        @self.sio.on("system")
        def on_connect(data):
            self.sendMessage(data["message"] + "\n", "system")


        @self.sio.on("msg")
        def on_connect(data):
            self.sendMessage(data["name"] + "\n" * 2 + data["message"] + "\n")

        @self.sio.on("exist")
        def on_connect(data):
            if data["boolean"] == "True":
                self.currentFriendCheck = data["boolean"]
                self.currentFriendName = data["name"]
                self.currentFriend = data["id"]
            else:
                self.currentFriendCheck = data["boolean"]
                self.currentFriendName = ""
                self.currentFriend = data["id"]

        self.friendList.friendButton.clicked.connect(self.menuButtonClicked)
        self.friendList.chattingButton.clicked.connect(self.menuButtonClicked)
        self.friendList.friendMakeButton.clicked.connect(self.friendButtonClicked)
        self.friendList.friendDelButton.clicked.connect(self.friendButtonClicked)
        self.friendList.friendDelOkButton.clicked.connect(self.friendButtonClicked)
        self.friendList.friendDelCancelButton.clicked.connect(self.friendButtonClicked)
        self.roomList.friendButton.clicked.connect(self.menuButtonClicked)
        self.roomList.chattingButton.clicked.connect(self.menuButtonClicked)
        self.roomList.makeRoomButton.clicked.connect(self.makeRoomButtonClicked)
        self.makeFriend.friendSearch.clicked.connect(self.makeFriendButtonClicked)
        self.makeFriend.okButton.clicked.connect(self.makeFriendButtonClicked)
        self.makeFriend.cancelButton.clicked.connect(self.makeFriendButtonClicked)
        self.makeFriend.backButton.clicked.connect(self.makeFriendButtonClicked)
        self.security.verifyButton.clicked.connect(self.securityCheck)
        self.userInit.okButton.clicked.connect(self.dataReadingException)

    # 서버에 정보 보내기
    def sendInfo(self):
        self.sio.emit("information", {
            "name" : self.name,
            "id" : self.id
        })

    # 아이디/패스워드 체크
    def securityCheck(self):
        if self.security.passwordLine.text() == user.IF["password"] and self.security.idLine.text() == user.IF["id"]:
            self.stackWidget.setCurrentIndex(2)
            self.sendInfo()

    # 메뉴바 처리
    def menuButtonClicked(self):
        sender = self.sender()
        if sender.text() == "친구":
            self.stackWidget.setCurrentIndex(2)
        elif sender.text() == "채팅":
            self.stackWidget.setCurrentIndex(3)
    
    # 친구창 처리
    def friendButtonClicked(self):
        sender = self.sender()
        if sender.text() == "+":
            self.stackWidget.setCurrentIndex(4)
        elif sender.text() == "-":
            self.friendList.friendBox.setSelectionMode(QAbstractItemView.MultiSelection)
            self.friendList.setChoiceButtonVisible()
        elif sender.text() == "확인":
            self.friendListDelete()
            self.friendList.friendBox.setSelectionMode(QAbstractItemView.NoSelection)
        elif sender.text() == "취소":
            self.friendList.setChoiceButtonUnvisible()
            self.friendList.friendBox.setSelectionMode(QAbstractItemView.NoSelection)

    def makeFriendButtonClicked(self):
        sender = self.sender()
        if sender.text() == "검색":
            friendId = self.makeFriend.friendId.text()
            if friendId:
                if friendId in self.friend:
                    self.makeFriend.resultfriendId.setText("이미 있는 친구 입니다.")
                    self.makeFriend.resultfriendName.setText(self.currentFriendName)
                    self.makeFriend.setLayOutVisibleWithoutButton()
                elif friendId == self.id:
                    self.makeFriend.resultfriendId.setText("나 자신은 영원한 인생의 친구 입니다.")
                    self.makeFriend.resultfriendName.setText(self.currentFriendName)
                    self.makeFriend.setLayOutVisibleWithoutButton()
                else:
                    self.sio.emit("friendmanager", {
                        "friendId" : self.makeFriend.friendId.text()
                    })
                    while True:
                        if self.currentFriend != friendId:
                            continue
                        else:
                            if self.currentFriendCheck == "True":
                                self.makeFriend.resultfriendName.setText(self.currentFriendName)
                                self.makeFriend.resultfriendId.setText(self.currentFriend)
                                self.makeFriend.setLayOutVisible()
                                print("check")
                                return
                            else:
                                self.makeFriend.resultfriendId.setText("사용자를 찾을 수 없습니다.")
                                self.makeFriend.resultfriendName.setText("검색 결과 없음")
                                self.makeFriend.setLayOutVisibleWithoutButton()
            else:
                self.makeFriend.resultfriendId.setText("최소 한자리 이상의 아이디를 검색해야 합니다.")
                self.makeFriend.resultfriendName.setText("검색 결과 없음")
                self.makeFriend.setLayOutVisibleWithoutButton()
        elif sender.text() == "추가":
            self.friendList.friendBox.addItem(self.currentFriendName)
            self.makeFriend.friendId.setText("")
            self.makeFriend.setLayOutUnvisible()
            self.stackWidget.setCurrentIndex(2)
        elif sender.text() == "취소":
            self.makeFriend.friendId.setText("")
            self.makeFriend.setLayOutUnvisible()
            self.stackWidget.setCurrentIndex(2)
        elif sender.text() == "<-":
            self.makeFriend.friendId.setText("")
            self.makeFriend.setLayOutUnvisible()
            self.stackWidget.setCurrentIndex(2)

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
        elif myPassWord != myPassWordCheck:
            self.userInit.exceptionAlert.showMessage("패스워드가 일치하지 않습니다.", 2000)
            return
        else :
            user.IF = {
                'name' : myName,
                'id' : myId,
                'password' : myPassWord,
                'friend' : []
                }
            self.name = user.IF["name"] + "\n"
            self.dataWriting()
            self.stackWidget.setCurrentIndex(2)
            self.sendInfo()

    # 사용자 정보 저장하기   
    def dataWriting(self):
        f = open("DataBase/userInfo.dat", "wb")
        pickle.dump(user.IF, f)

    # 이거 아직 안됨
    def friendListDelete(self):
        items = self.friendList.friendBox.selectedItems()
        indexs = self.friendList.friendBox.selectedIndexes()
        if not indexs:
            self.friendList.setChoiceButtonUnvisible()
        for item, index in zip(items, indexs):
            self.friend.remove(item.text())
            self.friendList.friendBox.takeItem(index.column())
            self.friendList.setChoiceButtonUnvisible()
        self.dataWriting()