const inputArea = document.getElementById("input_area")
const inputAction = document.getElementById("input_action")
const loadingElm = document.getElementById("loading")
const chatingList = document.getElementById("chating_list")
var isHandling = false

function autoResizeTextArea(event) {
    this.style.height = "20px"
    if (this.scrollHeight > 20) {
        this.style.height = this.scrollHeight + "px"
    }
}

async function postAction(event){
    if (isHandling) return
    let messContent = getContentFromInput("input_area")
    if (messContent.length <= 20) {
        alert("quá ngắn")
        return
    }

    addMessage(messContent, "user")
    togleLoading()
    let data = await postMessage(messContent, "/api/message")
    addMessage(data.message, "bot")
    togleLoading()
}

async function postMessage(messContent, url) {
    if (isHandling) {
        return 
    }
    isHandling = true
    const res = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: messContent
        })
    })
    isHandling = false
    return await res.json()
}

function addMessage(mess, type) {
    let newMess = document.createElement("div")
    let newSpan = document.createElement("p")
    newSpan.innerHTML = mess
    if (type == "user") {
        newMess.className = "message user-message"
    } else if (type == "bot") {
        newMess.className = "message"
    }
    newMess.appendChild(newSpan)
    chatingList.appendChild(newMess)
}

function getContentFromInput(idInp) {
    let inpElm = document.getElementById(idInp)
    return inpElm.value.trim();
}

function clearInp(idInp) {
    let inpElm = document.getElementById(idInp)
    inpElm.value = ""
}

function togleLoading() {
    loadingElm.classList.toggle("hiden")
}

inputArea.addEventListener("input", autoResizeTextArea)
inputAction.addEventListener("click", postAction)