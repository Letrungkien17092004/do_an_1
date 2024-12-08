
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

    // DOM Event
    async submitMessageEvent() {
        const thisParrent = this
        return async function (event) {
            event.stopPropagation()
            if (thisParrent.state == "pending") {
                return
            }
            thisParrent.state = 'pending'
            let userMessage = thisParrent.textarea.value
            // Add user message
            thisParrent.addMessage(userMessage, "user")
            let responseJson = await thisParrent.postMessage(userMessage.trim())
            // Add bot response
            thisParrent.addMessage(responseJson["message"], 'bot')
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