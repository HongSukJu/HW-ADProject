import socketio
from Client_UI import *

class user(Ktalk):
    
    def __init__(self):
        super().__init__()
        self.name = "홍석주"
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

        self.popup.okButton.clicked.connect(self.userInOut)

    def sendMessage(self, data, userType=None):
        item = QListWidgetItem()
        item.setText(data)
        if userType == "self":
            item.setTextAlignment(Qt.AlignRight)
        elif userType == "system":
            item.setTextAlignment(Qt.AlignCenter)
        self.chatting.chattingBox.addItem(item)

    def userInOut(self):
        self.room = self.popup.popupValue.text()
        self.sio.emit("roommanager", {
            "type" : "join",
            "name" : self.name,
            "room" : self.room,
        })
        self.stackWidget.setCurrentIndex(2)

    def msgToRoom(self, data):
        self.sio.emit("room", data)
        self.sendMessage(data["name"] + "\n" * 2 + data["message"] + "\n", "self")
    
    def writeChat(self):
        pass

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return and self.chatting.messageText.text():
            chat = self.chatting.messageText.text()
            data = {
                "type" : "chat",
                "name" : self.name,
                "room" : self.room,
                "message" : chat
            }
            self.msgToRoom(data)
            self.chatting.messageText.setText("")

    def closeEvent(self, event):
        if self.room:
            self.sio.emit("roommanager", {
                "type" : "quit",
                "name" : self.name,
                "room" : self.room
            })