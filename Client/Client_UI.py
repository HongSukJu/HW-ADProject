import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import socketio
import pickle

class Ktalk(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data = []
        self.dbfilename = '/home/co/다운로드/소프2/AD/Client/chat.dat'    
        self.startConnection()
        self.readChat()
        self.sendMessage()


    def startConnection(self):
        self.sio = socketio.Client()
        self.sio.connect("http://localhost:5000")

        self.sio.sleep(1)

        @self.sio.on("connection")
        def on_connect(data):
            if data["type"] == "connected":
                self.data.append("연결 성공")
                self.writeChat()
                self.sendMessage("연결 성공")

        @self.sio.on("system")
        def on_connect(data):
            self.data.append(data["message"])
            self.writeChat()
            self.sendMessage(data["message"])


        @self.sio.on("msg")
        def on_connect(data):
            self.data.append(data["name"] + " : " + data["message"])
            self.writeChat()
            self.sendMessage(data["name"] + " : " + data["message"])

        
        self.sio.sleep(1)

        name = ""
        room = ""

        while not name and not room:
            name = input("이름 > ")
            room = input("채팅방 > ")
            if name and room:
                self.sio.emit("roommanager", {
                    "type" : "join",
                    "room" : room,
                    "name" : name
                })

        msg = ""

        while msg != "-1":
            msg = input()
            self.sio.emit("room", {
                "type" : "chat",
                "room" : room,
                "name" : name,
                "message" : msg
            })
        else:
            self.sio.emit("roommanager", {
                "type" : "quit",
                "room" : room,
                "name" : name
            })

            self.sio.sleep(1)
            
            self.sio.disconnect()

    def initUI(self):
        self.chattingBox = QListWidget()
        self.roomBox = QListWidget()
        self.messageText = QLineEdit()
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setRange(0,100)
        self.sld.setMaximum(100)
        #change
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.chattingBox,1,1,5,1)
        grid.addWidget(self.roomBox,1,3,5,2)
        grid.addWidget(self.messageText,6,1,1,1)
        grid.addWidget(self.sld,6,3,1,2)
        self.setLayout(grid)

        self.setWindowTitle("Kook Talk")
        self.setGeometry(300,300,800,1000)
        self.show()
        
    def sendMessage(self,data):
        item = QListWidgetItem()
        item.setText(data)
        self.chattingBox.addItem(item)
        pass
    def closeEvent(self, event):
        self.writeChat()

    def readChat(self):
        try:
            fH = open(self.dbfilename, 'rb')
        except FileNotFoundError as e:
            self.data = []
            return

        try:
            self.data =  pickle.load(fH)
        except:
            pass
        else:
            pass
        fH.close()

    def writeChat(self):
        fH = open(self.dbfilename, 'wb')
        pickle.dump(self.data, fH)
        fH.close()
