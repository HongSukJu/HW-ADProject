const io = require("socket.io")(5000);

io.on("connection", function (socket) {

    socket.emit("connection", {
        type : "connected"
    })

    socket.on("chat", function(data) {
        console.log(`${data.room} // ${data.name} : ${data.message}`)
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
