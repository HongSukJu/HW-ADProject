import socketio, pickle
from Client_UI import *

class user(Ktalk):

    IF = None
    fileName = "dataBase/userInfo.dat"
    
    def __init__(self):
        super().__init__()
        self.dataReading()
        self.name = user.IF["name"]
        self.id = user.IF["id"]
        self.friend = user.IF["friend"]
        self.currentFriend = ""
        self.currentFriendCheck = ""
        self.currentFriendName = ""

        self.security.nameLabel.setText(self.name + "\n")
        self.friendList.friendBox.addItems(self.friend.values())

        self.start_connection()
    
    def start_connection(self):
        self.sio = socketio.Client()
        self.sio.connect("http://192.168.34.158:5000")

        @self.sio.on("system")
        def on_connect(data):
            self.takeMessage(data["message"] + "\n",  data["room"], "system")

        @self.sio.on("msg")
        def on_connect(data):
            self.takeMessage(data["name"] + "\n" * 2 + data["message"] + "\n", data["room"])

        @self.sio.on("currentuser")
        def on_connect(data):
            for ID in data:
                if data[ID]:
                    self.friendList.friendBox.findItems(self.friend[ID], Qt.MatchExactly)[0].setBackground(QColor(0, 255, 0))
                else:
                    self.friendList.friendBox.findItems(self.friend[ID], Qt.MatchExactly)[0].setBackground(QColor(255, 255, 255))

        @self.sio.on("exist")
        def on_connect(data):
            self.currentFriendCheck = data["boolean"]
            self.currentFriendName = data["name"]
            self.currentFriend = data["id"]
        
        @self.sio.on("checkinout")
        def on_connect(data):
            if data["id"] == self.id:
                return
            if data["type"] == "in":
                self.friendList.friendBox.findItems(self.friend[data["id"]], Qt.MatchExactly)[0].setBackground(QColor(0, 255, 0))
            else:
                self.friendList.friendBox.findItems(self.friend[data["id"]], Qt.MatchExactly)[0].setBackground(QColor(255, 255, 255))

        @self.sio.on("invite")
        def on_connect(data):
            roomName = "&&".join(sorted([self.id, data["friendid"]]))
            newChat = Chat()
            newChat.sendButton.clicked.connect(lambda : self.sendMessage(roomName=roomName))
            self.chatting[roomName] = newChat
            self.userInOut(room=roomName)
            self.roomList.roomBox.addItem(friend)

        @self.sio.on("roomclient")
        def on_connect(data):
            self.chatting[data["room"]].currentFriendBox.clear()
            self.chatting[data["room"]].currentFriendBox.addItems(data["clients"])

        self.friendList.friendButton.clicked.connect(self.menuButtonClicked)
        self.friendList.chattingButton.clicked.connect(self.menuButtonClicked)
        self.friendList.friendMakeButton.clicked.connect(self.friendButtonClicked)
        self.friendList.friendDelButton.clicked.connect(self.friendButtonClicked)
        self.friendList.friendDelOkButton.clicked.connect(self.friendButtonClicked)
        self.friendList.friendDelCancelButton.clicked.connect(self.friendButtonClicked)
        self.roomList.friendButton.clicked.connect(self.menuButtonClicked)
        self.roomList.chattingButton.clicked.connect(self.menuButtonClicked)
        self.roomList.makeRoomButton.clicked.connect(self.makeRoomButtonClicked)
        self.roomList.deleteRoomButton.clicked.connect(self.deleteRoomButtonClicked)
        self.roomList.checkRoomButton.clicked.connect(self.checkRoomButtonClicked)
        self.roomList.cancelRoomButton.clicked.connect(self.cancelRoomButtonClicked)
        self.roomList.roomBox.itemDoubleClicked.connect(self.openChatting)
        self.makeFriend.friendSearchButton.clicked.connect(self.makeFriendButtonClicked)
        self.makeFriend.okButton.clicked.connect(self.makeFriendButtonClicked)
        self.makeFriend.cancelButton.clicked.connect(self.makeFriendButtonClicked)
        self.makeFriend.backButton.clicked.connect(self.makeFriendButtonClicked)
        self.security.verifyButton.clicked.connect(self.securityCheck)
        self.userInit.okButton.clicked.connect(self.dataReadingException)
        self.friendList.friendBox.itemDoubleClicked.connect(self.friendListClicked)

    # 서버에 정보 보내기
    def sendInfo(self):
        self.sio.emit("information", {
            "name" : self.name,
            "id" : self.id,
            "friend" : self.friend
        })

    # 아이디/패스워드 체크
    def securityCheck(self):
        if self.security.passwordLine.text() == user.IF["password"] and self.security.idLine.text() == user.IF["id"]:
            self.stackWidget.setCurrentIndex(3)
            self.sendInfo()

    # 메뉴바 처리
    def menuButtonClicked(self):
        sender = self.sender()
        if sender.pos().x() == 0:
            self.stackWidget.setCurrentIndex(3)
        elif sender.pos().x() == 350:
            self.stackWidget.setCurrentIndex(4)
    
    # 친구창 처리
    def friendButtonClicked(self):
        sender = self.sender()
        if sender == self.friendList.friendMakeButton:
            self.stackWidget.setCurrentIndex(5)
        elif sender == self.friendList.friendDelButton:
            self.friendList.friendBox.setSelectionMode(QAbstractItemView.MultiSelection)
            self.friendList.setChoiceButtonVisible()
        elif sender == self.friendList.friendDelOkButton:
            self.friendListDelete()
            self.friendList.friendBox.setSelectionMode(QAbstractItemView.NoSelection)
        elif sender == self.friendList.friendDelCancelButton:
            self.friendList.setChoiceButtonUnvisible()
            self.friendList.friendBox.setSelectionMode(QAbstractItemView.NoSelection)

    # 친구 만들기 처리
    def makeFriendButtonClicked(self):
        sender = self.sender()
        if sender == self.makeFriend.friendSearchButton:
            friendId = self.makeFriend.friendId.text()
            self.makeFriend.setLayOutUnvisible()
            if friendId:
                if friendId in self.friend:
                    self.makeFriend.resultfriendId.setText("이미 있는 친구 입니다.")
                    self.makeFriend.resultfriendName.setText(friendId)
                    self.makeFriend.setLayOutVisibleWithoutButton()
                elif friendId == self.id:
                    self.makeFriend.resultfriendId.setText("나 자신은 영원한 인생의 친구 입니다.")
                    self.makeFriend.resultfriendName.setText(self.name)
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
                                return
                            else:
                                self.makeFriend.resultfriendId.setText("사용자를 찾을 수 없습니다.")
                                self.makeFriend.resultfriendName.setText("검색 결과 없음")
                                self.makeFriend.setLayOutVisibleWithoutButton()
                                return
            else:
                self.makeFriend.resultfriendId.setText("최소 한자리 이상의 아이디를 검색해야 합니다.")
                self.makeFriend.resultfriendName.setText("검색 결과 없음")
                self.makeFriend.setLayOutVisibleWithoutButton()
        elif sender == self.makeFriend.okButton:
            self.friendList.friendBox.addItem(self.currentFriendName)
            self.friend[self.currentFriend] = self.currentFriendName
            self.sio.emit("checkoneperson", {
                "id" : self.currentFriend
            })
            self.dataWriting()
            self.makeFriend.friendId.setText("")
            self.makeFriend.setLayOutUnvisible()
            self.stackWidget.setCurrentIndex(3)
        elif sender == self.makeFriend.cancelButton:
            self.makeFriend.friendId.setText("")
            self.makeFriend.setLayOutUnvisible()
            self.stackWidget.setCurrentIndex(3)
        elif sender == self.makeFriend.backButton:
            self.makeFriend.friendId.setText("")
            self.makeFriend.setLayOutUnvisible()
            self.stackWidget.setCurrentIndex(3)

    # 방 만들기
    def makeRoomButtonClicked(self):
        roomNameValue = self.roomList.roomNameValue.text()
        if roomNameValue in self.chatting:
            self.roomList.roomNameValue.setText("")
            return
        if roomNameValue:
            newChat = Chat()
            newChat.sendButton.clicked.connect(lambda : self.sendMessage(roomNameValue))
            self.chatting[roomNameValue] = newChat
            self.userInOut(roomNameValue)
            self.roomList.roomBox.addItem(roomNameValue)
            self.roomList.roomNameValue.setText("")
                
    # 방 지우기 처리
    def deleteRoomButtonClicked(self):
        self.roomList.setChoiceButtonVisible()
        self.roomList.roomBox.setSelectionMode(QAbstractItemView.MultiSelection)

    # 방 지우기 처리2
    def checkRoomButtonClicked(self):
        items = self.roomList.roomBox.selectedItems()
        indexs = self.roomList.roomBox.selectedIndexes()
        if not indexs:
            self.roomList.setChoiceButtonUnvisible()
            return
        for item, index in zip(items, indexs):
            roomName = item.text()
            self.sio.emit('roommanager',{
                "type" : "quit",
                "name" : self.name,
                "room" : roomName
            })
            self.roomList.roomBox.takeItem(index.column())
            QTest.qWait(100)
            del self.chatting[roomName]
        self.roomList.roomBox.setSelectionMode(QAbstractItemView.NoSelection)
        self.roomList.setChoiceButtonUnvisible()
            
    # 방 지우기 처리3
    def cancelRoomButtonClicked(self):
        for item in self.roomList.roomBox.selectedItems():
            item.setSelected(False)
        self.roomList.roomBox.setSelectionMode(QAbstractItemView.NoSelection)
        self.roomList.setChoiceButtonUnvisible()

    # 1:1 채팅방 만들기
    def friendListClicked(self):
        if self.friendList.friendBox.currentItem().background() == QColor(0, 255, 0):
            friendId = list(self.friend)[self.friendList.friendBox.currentRow()]
            roomName = "&&".join(sorted([self.id, friendId]))
            self.sio.emit("roommanager", {
                "type" : "init",
                "id" : self.id,
                "friendid" : friendId
            })
            newChat = Chat()
            newChat.sendButton.clicked.connect(lambda : self.sendMessage(roomName=roomName))
            self.chatting[roomName] = newChat
            self.userInOut(room=roomName)
            self.roomList.roomBox.addItem(roomName)
    
    # 톡방 친구 추가 
    def addFriendsToRoom(self):
        sender = self.sender()
        if sender.text() == "확인":
            pass

    # 메세지 받기
    def takeMessage(self, data, room, userType=None):
        item = QListWidgetItem()
        item.setText(data)
        if userType == "self":
            item.setTextAlignment(Qt.AlignRight)
        elif userType == "system":
            item.setTextAlignment(Qt.AlignCenter)
        self.chatting[room].chattingBox.addItem(item)
        self.chatting[room].chattingBox.scrollToBottom()

    # 방 들어가기
    def userInOut(self, room):
        self.sio.emit("roommanager", {
            "type" : "join",
            "name" : self.name,
            "room" : room
        })

    # 방 열기
    def openChatting(self):
        self.chatting[self.roomList.roomBox.currentItem().text()].show()

    # 메세지 보내기
    def sendMessage(self, roomName):
        obj = self.chatting[roomName]
        msg = obj.messageText.text()
        if msg:
            self.sio.emit("room", {
                "type" : "chat",
                "name" : self.name,
                "room" : roomName,
                "message" : msg
                })
            data = self.name + "\n" * 2 + msg + "\n"
            obj.messageText.setText("")
            self.takeMessage(data, roomName, userType="self")

    # 사용자 정보 불러오기
    def dataReading(self):
        try:
            f = open(user.fileName, "rb")
            user.IF = pickle.load(f)
        except:
            f = open(user.fileName, "wb")
            pickle.dump({
                "name" : "",
                "id" : "",
                "password" : "",
                "friend" : {}
            }, f)
            f = open(user.fileName, "rb")
            user.IF = pickle.load(f)
        if not user.IF["name"]:
            QTest.qWait(1000)
            self.fader_widget = FaderWidget(self.stackWidget.widget(0), self.stackWidget.widget(2))
            self.stackWidget.setCurrentIndex(2)
        else:
            QTest.qWait(1000)
            self.fader_widget = FaderWidget(self.stackWidget.widget(0), self.stackWidget.widget(1))
            self.stackWidget.setCurrentIndex(1)
            
    # 사용자 정보 불러오기 예외처리
    def dataReadingException(self):
        myName = self.userInit.nameValue.text()
        myId = self.userInit.idValue.text()
        myPassWord = self.userInit.passwordValue.text()
        myPassWordCheck = self.userInit.passwordCheckValue.text()
        if not myName:
            self.userInit.exceptionAlert.showMessage("이름을 입력해주세요.", 2000)
            return
        elif not myId:
            self.userInit.exceptionAlert.showMessage("아이디를 입력해주세요.", 2000)
            return
        elif not myPassWord:
            self.userInit.exceptionAlert.showMessage("패스워드를 입력해주세요.", 2000)
            return
        elif myPassWord != myPassWordCheck:
            self.userInit.exceptionAlert.showMessage("패스워드 확인을 제대로 입력해주세요", 2000)
            return
        else :
            user.IF = {
                'name' : myName,
                'id' : myId,
                'password' : myPassWord,
                'friend' : {}
                }
            self.name = user.IF["name"]
            self.dataWriting()
            self.stackWidget.setCurrentIndex(3)
            self.sendInfo()

    # 사용자 정보 저장하기   
    def dataWriting(self):
        f = open(user.fileName, "wb")
        pickle.dump(user.IF, f)

    # 친구 목록 지우기
    def friendListDelete(self):
        items = self.friendList.friendBox.selectedItems()
        indexs = self.friendList.friendBox.selectedIndexes()
        if not indexs:
            self.friendList.setChoiceButtonUnvisible()
            return
        for item, index in zip(items, indexs):
            for ID in self.friend:
                if self.friend[ID] == item.text():
                    del self.friend[ID]
                    break
            self.friendList.friendBox.takeItem(index.column())
            self.friendList.setChoiceButtonUnvisible()
        user.IF["friend"] = self.friend
        self.dataWriting()

    # 꺼짐 처리
    def closeEvent(self, event):
        self.sio.emit("out", {
            "id" : self.id
            })
        QApplication.closeAllWindows()
        QTest.qWait(100)
        self.sio.disconnect()