
class ChatManager {
    constructor({ textarea, areaSetting, messContainer }) {
        this.textarea = textarea
        this.areaSetting = areaSetting
        this.messContainer = messContainer

        this.textarea.addEventListener("input", autoResize)
    }

    addMessage(messContent, messType) {
        const newMessage =
            `
        <div class="message ${messType}">
            <div class="message-text">
                ${messContent}
            </div>
        </div>
        `
    }

    autoResize() {
        let thisParrent = this
        return function(event) {
            event.stopPropagation()
            this.style.height = "30px";
            this.style.height = (this.scrollHeight) + "px";
            this.scrollIntoView()
        }
    }
}


    window.addEventListener("load", () => {
    })