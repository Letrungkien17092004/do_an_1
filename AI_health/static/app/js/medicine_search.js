import { TabManager } from "./utilities.js"

class ImageSelection {
    constructor({ selectActivation, captureActivation, targetInput, previewElm }) {
        this.selectActivation = selectActivation
        this.captureActivation = captureActivation
        this.targetInput = targetInput
        this.previewElm = previewElm
        this.currentBase64 = null
    }

    load() {
        this.selectActivation.addEventListener("click", this.selectEvent())
        this.captureActivation.addEventListener("click", this.captureEvent())
        this.targetInput.addEventListener("change", this.changeFileEvent())
    }

    selectEvent() {
        var thisParent = this
        return function (event) {
            event.stopPropagation()
            thisParent.targetInput.removeAttribute('capture')
            thisParent.targetInput.click()
        }
    }

    async readAsBase64(file) {
        const readerTask = new Promise((resolve, reject) => {
            const reader = new FileReader()
            reader.onload = function (e) {
                resolve(e.target.result)
            }
            reader.readAsDataURL(file)
        })

        return await readerTask // Nhận base64 ở đây

    }

    captureEvent() {
        var thisParent = this
        return function (event) {
            event.stopPropagation()
            thisParent.targetInput.setAttribute('capture', 'environment')
            thisParent.targetInput.click()
        }
    }

    changeFileEvent() {
        var thisParent = this
        return async function (event) {
            event.stopPropagation()
            const file = this.files[0]
            if (file) {
                try {
                    thisParent.currentBase64 = await thisParent.readAsBase64(file)
                    thisParent.loadPreview()
                } catch (error) {
                    thisParent.currentBase64 = null
                    thisParent.loadPreview()
                }
            }
        }
    }

    getData() {
        return this.currentBase64
    }

    async loadPreview() {
        if (this.previewElm) {
            this.previewElm.src = this.currentBase64
        } else {
            console.warn("preview element is not set in ImageSelection");
        }
    }
}

class MedicineSearchManager {
    constructor({ tabManager, submitBtn, gobackBtn, imageSelection, mainMedicineCard, recommendList }) {
        this.state = "ready"
        this.tabManager = tabManager
        this.submitBtn = submitBtn
        this.gobackBtn = gobackBtn
        this.imageSelection = imageSelection
        this.mainMedicineCard = mainMedicineCard
        this.recommendList = recommendList
    }

    load() {
        this.submitBtn.addEventListener("click", this.submitEvent())
        this.gobackBtn.addEventListener("click", this.gobackBtnEvent())
    }

    async postData(base64Data) {
        let res = await fetch("/api/medicineService/v1/search-medicine", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "image": base64Data
            })
        })

        if (res.status != 200) {
            return null
        }
        return await res.json()
    }

    async search(base64Data) {
        try {
            if (this.state != "ready") return false
            this.state = "pending"
            const resData = await this.postData(base64Data)
            if (resData) {
                this.renderMedicines(resData.data)
                this.state = "ready"
                return true
            }
            alert("Đã cã lỗi xảy ra!, vui lòng thử lại sau.")
            this.state = "ready"
            return false
        } catch (error) {
            console.log("error here")
            alert("Đã cã lỗi xảy ra!, vui lòng thử lại sau.")
            this.state = "ready"
            return false
        }

    }

    async renderMedicines(data) {
        this.mainMedicineCard.innerHTML = ""
        this.recommendList.innerHTML = ""
        if (data.length > 0) {
            this.renderOne(data[0])
            this.renderList(data)
            if (data.length > 1) {
                this.renderList(data.slice(1))
            }
        }
    }

    async renderOne(medicine) {
        let newMedicineCard = this.createNewMedicineCard(medicine, true)
        this.mainMedicineCard.innerHTML = newMedicineCard.innerHTML
    }
    async renderList(medicines) {
        medicines.forEach(medicine => {
            let newMedicineCard = this.createNewMedicineCard(medicine, false)
            let newCol = document.createElement("div")
            newCol.className = "col l-3 m-6 s-12 xs-12"
            newCol.appendChild(newMedicineCard)
            this.recommendList.appendChild(newCol)
        })
    }

    createNewMedicineCard(medicine, isFull) {
        let medicineCard = document.createElement("div")
        medicineCard.className = "medicine-card"
        let context1 =
        `
        <div style="background-image: url('${medicine.url}');" class="medicine-image"></div>
        <div class="medicine-info">
            <div class="medicine-info-title">${medicine.name}</div>
            <div class="medicine-info-price">
                    Giá tham khảo:
                <span class="medicine-info-price-highlight">${medicine.price} VND</span>
            </div>
        </div>
        <div class="medicine-link">
            <a href="${medicine.links}">
                <div class="btn btn-color-theme">
                        Xem tại hiệu thuốc
                </div>
            </a>
        </div>
        `
        let context2 = 
        `
        <div style="background-image: url('${medicine.url}');" class="medicine-image"></div>
        <div class="medicine-info">
            <div class="medicine-info-title">${medicine.name}</div>
            <div class="medicine-info-price">
                    Giá tham khảo:
                <span class="medicine-info-price-highlight">${medicine.price} VND</span>
            </div>
            <div class="medicine-info-discrible">
                <p class="text">
                ${medicine.info}
                </p>
            </div>
        </div>
        <div class="medicine-link">
            <a href="${medicine.links}">
                <div class="btn btn-color-theme">
                        Xem tại hiệu thuốc
                </div>
            </a>
        </div>
        `

        if (isFull == true) {
            medicineCard.innerHTML = context2
            return medicineCard
        } 
        medicineCard.innerHTML = context1
        return medicineCard
    }

    gobackBtnEvent() {
        var thisParent = this
        return function (event) {
            event.stopPropagation()
            thisParent.tabManager.showTab(0)
        }
    }

    submitEvent() {
        var thisParent = this
        return async function (event) {
            event.stopPropagation()

            let base64Data = thisParent.imageSelection.getData()
            if (base64Data) {
                thisParent.tabManager.showTab(2)
                if (await thisParent.search(base64Data)) {
                    thisParent.tabManager.showTab(1)
                } else {
                    thisParent.tabManager.showTab(0)
                }
            } else {
                alert("Vui lòng chọn ảnh")
            }
        }
    }
}


window.addEventListener("load", () => {
    const tabManager = new TabManager({
        tabs: [
            document.getElementById("tab-select"),
            document.getElementById("tab-result"),
            document.getElementById('tab-loading'),
        ],
        classHiden: "tab-hiden"
    })

    const imageSelection = new ImageSelection({
        selectActivation: document.getElementById("chooseFile"),
        captureActivation: document.getElementById("capture"),
        targetInput: document.getElementById("imageInput"),
        previewElm: document.getElementById("preview-image")
    })

    const medicineSearchManager = new MedicineSearchManager({
        tabManager: tabManager,
        submitBtn: document.getElementById("action-search"),
        gobackBtn: document.getElementById("previous-action"),
        mainMedicineCard: document.getElementById("mainMedicine"),
        recommendList: document.getElementById("recommends-list"),
        imageSelection: imageSelection,
    })
    imageSelection.load()
    medicineSearchManager.load()
})