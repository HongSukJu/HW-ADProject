const fs = require("fs")

class Barrel {
    constructor () {
        try {
            let lawData = fs.readFileSync("dataBase/userList.json")
            this.data = JSON.parse(lawData, "utf8")
        } catch (e) {
            this.data = {}
            fs.writeFileSync("dataBase/userList.json", JSON.stringify(this.data))
        }
    }

    async save(data) {
        this.data = data
        fs.writeFileSync("dataBase/userList.json", JSON.stringify(this.data))
    }
}

module.exports = Barrel