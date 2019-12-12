const io = require("socket.io")(5000)
let currentUsers = {}
let saveUsers = {} 
let roomNumber = 1

io.on("connection", function (socket) {

    socket.on("information", function(data) {
        currentUsers[data.id] = socket.id
        let result = {}

        if (!(data.id in saveUsers)) {
            saveUsers[data.id] = data.name
        }

        for (let id of Object.keys(data.friend)) {
            if (Object.keys(currentUsers).includes(id)) {
                result[id] = true
            } else {
                result[id] = false
            }
        }

        socket.emit("currentuser", result)

        io.emit("checkinout", {
            type : "in",
            id : data.id
        })

        console.log("\n" + "-----------------------------------")
        console.log(`접속감지, 이름 : ${data.name}, 아이디 : ${data.id}`)
        console.log("현재 접속자 : ")
        console.log(currentUsers)
        console.log("서버 내 유저 : ")
        console.log(saveUsers)
        console.log("-----------------------------------" + "\n")

    })

    socket.on("out", function(data) {
        delete currentUsers[data.id]

        io.emit("checkinout", {
            type : "out",
            id : data.id
        })

        console.log("\n" + "-----------------------------------")
        console.log("현재 접속자 : ")
        console.log(currentUsers)
        console.log("서버 내 유저 : ")
        console.log(saveUsers)
        console.log("-----------------------------------" + "\n")
    })

    socket.on("checkoneperson", function(data) {
        let status = ""

        if (data.id in currentUsers) {
            status = "in"
        } else {
            status = "out"
        }

        socket.emit("checkinout", {
            type : status,
            id : data.id
        })
    })

    socket.on("friendmanager", function(data) {

        if (Object.keys(saveUsers).includes(data.friendId)) {
            socket.emit("exist", {
                id : data.friendId,
                boolean : "True",
                name : saveUsers[data.friendId]
            })
        } else {
            socket.emit("exist", {
                id : data.friendId,
                boolean : "False",
                name : "?"
            })
        }
    })

    socket.on("roommanager", function(data) {

        if (data.type == "join") {
            socket.join(data.room)
        
            socket.emit("system", {
                room : data.room,
                message : "채팅방에 오신 것을 환영합니다."
            })

            socket.broadcast.to(data.room).emit("system", {
                room : data.room,
                message : `${data.name}님이 접속하셨습니다.`
            })

            console.log(`${data.name} -> ${data.room}`);
            
        }

        if (data.type == "quit") {
            socket.leave(data.room)

            socket.emit("system", {
                room : data.room,
                message : "채팅방을 나갔습니다."
            })

            socket.broadcast.to(data.room).emit("system", {
                room : data.room,
                message : `${data.name}님이 나가셨습니다.`
            })

            console.log(`${data.name} -X ${data.room}`);
        }

        if (data.type == "init") {
            console.log("test")
            io.to(currentUsers[data.friendid]).emit("invite", {
                friendid : data.id
            })
        }
    })

    socket.on("room", function (data) {

        if (data.type == "chat") {
            socket.broadcast.to(data.room).emit("msg", {
                name : data.name,
                room : data.room,
                message : data.message
            })
        }
    })
})
