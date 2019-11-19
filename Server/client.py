import socketio

sio = socketio.Client()

sio.connect("http://localhost:5000")

@sio.on("connection")
def on_connect(data):
    if data["type"] == "connected":
        print("연결 성공")
@sio.on("system")
def on_connect(data):
    print(data["message"])
@sio.on("msg")
def on_connect(data):
    print(data["name"] + " : " + data["message"])

sio.sleep(1)

name = ""
room = ""

while not name and not room:
    name = input("이름 > ")
    room = input("채팅방 > ")
    if name and room:
        sio.emit("roommanager", {
            "type" : "join",
            "room" : room,
            "name" : name
        })

msg = ""

while msg != "-1":
    msg = input()
    sio.emit("room", {
        "type" : "chat",
        "room" : room,
        "name" : name,
        "message" : msg
    })
else:
    sio.emit("roommanager", {
        "type" : "quit",
        "room" : room,
        "name" : name
    })

    sio.sleep(1)
    
    sio.disconnect()