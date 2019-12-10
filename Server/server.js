const io = require("socket.io")(5000)
let currentUsers = {}
let saveUsers = {}

io.on("connection", function (socket) {

    socket.on("information", function(data) {
        currentUsers[data.id] = socket.id
        if (!(data.name in saveUsers)) {
            saveUsers[data.id] = data.name
        }
        console.log("\n" + "-----------------------------------")
        console.log(`접속감지, 이름 : ${data.name}, 아이디 : ${data.id}`)
        console.log("현재 접속자 : ")
        console.log(currentUsers)
        console.log("서버 내 유저 : ")
        console.log(saveUsers)
        console.log("-----------------------------------" + "\n")
    })

    socket.on("friendmanager", function(data) {
        if (data.friendId in saveUsers) {
            socket.emit("exist", {
                id : data.friendId,
                boolean : "True",
                name : saveUsers[data.friendId]
            })
        } else {
            socket.emit("exist", {
                id : data.friendId,
                boolean : "False"
            })
        }
    })

    socket.on("roommanager", function(data) {
        if(data.type == "join") {
            socket.join(data.room)
        
            socket.emit("system", {
                message : "채팅방에 오신 것을 환영합니다."
            })

            socket.broadcast.to(data.room).emit("system", {
                message : `${data.name}님이 접속하셨습니다.`
            })

            console.log(`${data.name} -> ${data.room}`);
            
        }
        if(data.type == "quit") {
            socket.leave(data.room)

            socket.emit("system", {
                message : "채팅방을 나갔습니다."
            })

            socket.broadcast.to(data.room).emit("system", {
                message : `${data.name}님이 나가셨습니다.`
            })

            console.log(`${data.name} -X ${data.room}`);
        }
    })

    socket.on("room", function (data) {
        if (data.type == "chat") {
            socket.broadcast.to(data.room).emit("msg", {
                name : data.name,
                message : data.message
            })
        }
    })
})
