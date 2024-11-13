import { OverlayDisplay } from './overlay_display.js'
import { ListUI } from './listUI.js'
import { PredictTypeSelect } from './predictionDiseaseSystem.js'

class InputManager {
    constructor({ formId, optionClass, btnAddId, listId, filterId,overlay, listUI }) {
        this.formId = formId
        this.optionClass = optionClass
        this.btnAddId = btnAddId
        this.listId = listId
        this.filterId = filterId
        this.overlay = overlay
        this.listUI = listUI
    }

    load() {
        this.form = document.getElementById(this.formId)
        this.options = document.querySelectorAll(`.${this.optionClass}`)
        this.btnAdd = document.getElementById(this.btnAddId)
        this.list = document.getElementById(this.listId)
        this.filter = document.getElementById(this.filterId)
        this.addEvent()
    }

    async loadFilter() {
        const types = await this.loadJson("/static/json/types.json")
        const filterSelect = document.getElementById("filter-select")
        for (let i = 0; i < types.length; i++) {
            let newOption = document.createElement("option")
            newOption.value = types[i]
            newOption.innerHTML = types[i]
            filterSelect.appendChild(newOption)
        }
    }

    async loadSelectOption() {
        const symptoms = await this.loadJson("/static/json/categories.json")
        symptoms.forEach((symptom) => {
            let baseChild = document.createElement("div")
            let baseText = document.createElement("span")
            let newOption = document.createElement("div")
            newOption.value_symptom = "a"
            baseChild.className = "form-options"
            baseText.className = "text fz-18 w-500"

            newOption.className = "list-items"
            newOption.setAttribute("data-value", symptom.value)
            newOption.setAttribute("data-type", symptom.type)
            baseText.innerHTML = symptom.word

            baseChild.appendChild(baseText)
            newOption.appendChild(baseChild)
            this.form.appendChild(newOption)
        })
        const optionHasLoaded = this.getOptions()
        optionHasLoaded.forEach((option) => {
            option.addEventListener("click", this.markSelectedEvent)
        })
    }

    async loadJson(url) {
        var res = await fetch(url, {
            method: "GET"
        })
        return await res.json()
    }

    getSelected() {
        var selecteds = []
        this.getOptions().forEach((option) => {
            if (option.classList.contains("selected")) {
                selecteds.push(option)
            }
        })
        return selecteds
    }

    getOptions() {
        return document.querySelectorAll(`.${this.optionClass}`)
    }

    updateOption(event) {
        const listItems = document.querySelectorAll("#select-form .list-items")
        const filterValue = this.filter.value
        if (filterValue == "all") {
            listItems.forEach((listItem) => {
                listItem.className = "list-items"
            })
            return
        }
        listItems.forEach((listItem) => {
            if (listItem.getAttribute("data-type") == filterValue) {
                listItem.className = "list-items"
            } else {
                listItem.className = "list-items hiden"
            }
        })
    }

    addEvent() {
        this.btnAdd.addEventListener("click", this.addSymptomEvent(this))
        this.filter.addEventListener("change", this.updateOption.bind(this))
    }

    // JS DOM Event
    markSelectedEvent(event) {
        event.stopPropagation()
        this.classList.toggle("selected")
    }

    // JS DOM Event
    addSymptomEvent(thisParent) {
        return function (event) {
            let selecteds = thisParent.getSelected()
            // add symptom
            selecteds.forEach((selected) => {
                thisParent.listUI.addItem(selected.innerText)
            })

            // reste selected
            selecteds.forEach((selected) => {
                selected.classList.remove("selected")
            })

            thisParent.overlay.hiden()
        }
    }
}

const overlay = new OverlayDisplay({
    activationId: "plus-symptom",
    overlayId: "select-overlay"
})

const selectedList = new ListUI({
    listId: "selected_list",
    classItem: "selected_list_items",
    baseParent: "list lis-direction-row",
    baseChild: "list-items"
})

const inputManager = new InputManager({
    formId: "select-form",
    optionClass: "form-options",
    btnAddId: "select-actions-submit",
    listId: "select_list",
    filterId: "filter-select",
    overlay: overlay,
    listUI: selectedList
})

const predictSystem = new PredictTypeSelect({
    url: '/api/select',
    selectedList: selectedList
})

window.addEventListener("load", (event) => {
    overlay.load()
    selectedList.load()
    inputManager.load()
    inputManager.loadFilter()
    inputManager.loadSelectOption()
})