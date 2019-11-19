import socketio

class user: # 유저 생성, 정보 저장 기능
    def __init__(self, name):
        self.name = name
        self.room = []
        self.readInfo()
        self.start_connection()

    def start_connection(self):
        self.sio = socketio.Client()
        self.sio.connect("http://http://localhost:5000")
        
        @self.sio.on("connection")
        def on_connect(data):
            pass

        @self.sio.on("system")
        def on_connect(data):
            pass

        @self.sio.on("msg")
        def on_connect(data):
            pass

    def writeChat(self):
        pass

    def writeRoom(self):
        pass

    def writeInfo(self):
        pass

    def readInfo(self):
        pass

class roommanager: # 방과 유저 연결 기능
    def userInOut(self, user, data):
        user.sio.emit("roomanager", data)

    def initRoom(self):
        # 서버에 빈 방 요청
        # 서버에서 1~100까지 랜덤으로 생성?
        # 서버 내에도 room array 필요
        # 어레이 내에 존재할 경우 다시 랜덤배정
        pass

class room: # 방 내에서의 기능
    def msgToRoom(self, user, data):
        user.sio.emit("room", data)
        
        