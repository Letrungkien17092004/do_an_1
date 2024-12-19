
class ChatManager {
    constructor({ textarea, areaSetting, messContainer, activator }) {
        this.textarea = textarea
        this.areaSetting = areaSetting
        this.messContainer = messContainer
        this.activator = activator
        this.state = 'ready'
    }

    async load() {
        if (!this.textarea || !this.areaSetting || !this.messContainer || !this.activator) {
            window.console.error("ChatManager chưa định nghĩa các ràng buộc quan trọng. Hệ thống chưa thể sử dụng");
            return
        }
        this.textarea.addEventListener("input", this.autoResize())
        this.activator.addEventListener("click", await this.submitMessageEvent())
        console.log("khởi tạo thành công")
    }

    addMessage(messContent, messType) {
        const newMessage = document.createElement("div")
        newMessage.className = `message ${messType}`

        const newMessageText = document.createElement("div")
        newMessageText.className = "message-text"
        newMessageText.innerHTML = messContent

        newMessage.appendChild(newMessageText)
        this.messContainer.append(newMessage)
    }

    async postMessage(message) {
        const res = await fetch("/api/predict/v1/message", {
            headers: {
                "Content-Type" : "application/json",
            },
            method: "POST",
            body: JSON.stringify({
                "message": message
            })
        })

        return await res.json()

    }

    makeMessageWithData(data) {
        console.log(data)
        let disease = data["disease"]
        let prescriptMedicines = data["prescript-Medicine"]
        let text1 = 
        `
        Từ các triệu chứng bạn đã chung cấp rất có khả năng bạn đã mắc bệnh:
        <span style = "text-decoration: underline; color: red">
            ${disease.name}
        </span>
        </br>
        ${disease.discription}
        </br></br>
        `
        if (prescriptMedicines.length > 0) {
            let prescriptMedicine  =  prescriptMedicines[0]
            console.log(prescriptMedicine)
            var text2 = 
            `
            Tôi đã tìm thấy một vài liệu pháp mà bạn có thể tham khảo:</br>
            với chế độ ăn uống bạn nên sử dụng: 
            <span style = "color: blue">
                ${prescriptMedicine.prescription.foodDiscription}
            </span>
            </br></br>
            `
            if (prescriptMedicine["medicines"].length > 0)  {
                let medicines = prescriptMedicine["medicines"]
                let medicineText = 
                `
                Tôi cung đã tìm thấy một vài loại thuốc liên quan đến bệnh này mà bạn có thể tham khảo:
                `
                medicines.forEach(medicine => {
                    let temp = `<a href = "${medicine.url}">${medicine.name}</a> </br>`
                    medicineText+=temp
                });
                text2 += medicineText
            }
        }
        return text1 + text2
    }

    renderNormal({message, status, type, data}) {
        switch (type) {
            case "ONLY-CHAT":
                this.addMessage(message, "bot")
                break;
            case "FULL-DATA":
                this.addMessage(this.makeMessageWithData(data), "bot")
                break;
            default:
                break;
        }
    }
    renderError(type) {
        switch (type) {
            case "ZERO-IMPORTANT":
                this.addMessage("Vui lòng cung cấp nhiều triệu chứng hơn!", "bot")
                break;
            case "ZERO-SYMPTOM":
                this.addMessage("Vui lòng cung cấp các triệu chứng!", "bot")
                break;
            default:
                this.addMessage("Đã có lỗi sảy ra! vui lòng thử lại sau", "bot")
                break;
        }
    }
    // DOM Event
    async submitMessageEvent() {
        const thisParrent = this
        return async function (event) {
            event.stopPropagation()
            if (thisParrent.state == "pending") {
                console.log("Vui Lòng đợi!")
                return
            }
            thisParrent.state = 'pending'
            let userMessage = thisParrent.textarea.value
            // Add user message
            thisParrent.addMessage(userMessage, "user")
            let responseJson = await thisParrent.postMessage(userMessage.trim())
            // Add bot response
            switch (responseJson["status"]) {
                case "OK":
                    thisParrent.renderNormal(responseJson)
                    break;
                case "BAD":
                    thisParrent.renderError(responseJson["message"])
                    break;
                default:
                    break;
            }
            thisParrent.textarea.value = ""
            thisParrent.state = "ready"
        }
    }

    // DOM Event
    autoResize() {
        let thisParrent = this
        return function (event) {
            event.stopPropagation()
            this.style.height = `${thisParrent.areaSetting.heightTrigger}px`;
            this.style.height = (this.scrollHeight) + "px";
            this.scrollIntoView()
        }
    }
}


window.addEventListener("load", () => {
    const chatManager = new ChatManager({
        textarea: document.getElementById("chat-input"),
        areaSetting: {
            heightTrigger: 30
        },
        messContainer: document.getElementById("message-container"),
        activator: document.getElementById("post-message")
    })
    chatManager.load()
})