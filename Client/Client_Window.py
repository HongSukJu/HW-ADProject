import socketio
from Client_UI import *

class user(Ktalk):
    
    def __init__(self):
        super().__init__()
        self.name = "채원찬"
        self.room = []
        self.start_connection()

    def start_connection(self):
        self.sio = socketio.Client()
        self.sio.connect("http://localhost:5000")
        
        self.sio.sleep(1)

        @self.sio.on("connection")
        def on_connect(data):
            if data["type"] == "connected":
                self.sendMessage("연결 성공")

        @self.sio.on("system")
        def on_connect(data):
            self.sendMessage(data["message"] + "\n", "system")


        @self.sio.on("msg")
        def on_connect(data):
            self.sendMessage(data["name"] + "\n" * 2 + data["message"] + "\n")

        self.userInOut({
            "type" : "join",
            "name" : self.name,
            "room" : "막강소융"
        })

    def sendMessage(self, data, userType=None):
        item = QListWidgetItem()
        item.setText(data)
        if userType == "self":
            item.setTextAlignment(Qt.AlignRight)
        elif userType == "system":
            item.setTextAlignment(Qt.AlignCenter)
        self.chattingBox.addItem(item)

    def userInOut(self, data):
        self.sio.emit("roommanager", data)

    def msgToRoom(self, data):
        self.sio.emit("room", data)
        self.sendMessage(data["name"] + "\n" * 2 + data["message"] + "\n", "self")
    
    def writeChat(self):
        pass

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            chat = self.messageText.text()
            data = {
                "type" : "chat",
                "name" : self.name,
                "room" : "막강소융",
                "message" : chat
            }
            self.msgToRoom(data)
            self.messageText.setText("")