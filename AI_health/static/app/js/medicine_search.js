import { TabManager } from "./utilities.js"



class MedicineSearchManager {
    constructor({tabManager, submitBtn, gobackBtn}) {
        this.tabManager = tabManager
        this.submitBtn = submitBtn
        this.gobackBtn = gobackBtn
    }

    load() {
        this.submitBtn.addEventListener("click", this.submitEvent())
        this.gobackBtn.addEventListener("click", this.gobackBtnEvent())
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
            thisParent.tabManager.showTab(1)
        }
    }
}


window.addEventListener("load", () => {
    const tabManager = new TabManager({
        tabs: [
            document.getElementById("tab-select"),
            document.getElementById("tab-result"),
        ],
        classHiden: "tab-hiden"
    })

    const medicineSearchManager = new MedicineSearchManager({
        tabManager: tabManager,
        submitBtn: document.getElementById("action-search"),
        gobackBtn: document.getElementById("previous-action")
    })

    medicineSearchManager.load()
})