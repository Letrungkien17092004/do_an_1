import { OverlayDisplay } from './overlay_display.js'
import { ListUI } from './listUI.js'
import { PredictTypeSelect } from './predictionDiseaseSystem.js'

class InputManager {
    constructor({ formId, optionClass, btnAddId, listId, overlay, listUI }) {
        this.formId = formId
        this.optionClass = optionClass
        this.btnAddId = btnAddId
        this.listId = listId
        this.overlay = overlay
        this.listUI = listUI
    }

    load() {
        this.form = document.getElementById(this.formId)
        this.options = document.querySelectorAll(`.${this.optionClass}`)
        this.btnAdd = document.getElementById(this.btnAddId)
        this.list = document.getElementById(this.listId)
        this.addEvent()
    }

    getSelected() {
        var selecteds = []
        this.options.forEach((option) => {
            if (option.classList.contains("selected")) {
                selecteds.push(option)
            }
        })
        return selecteds
    }

    addEvent() {
        // event click to select options
        this.options.forEach((option) => {
            option.addEventListener("click", this.markSelectedEvent)
        })

        this.btnAdd.addEventListener("click", this.addSymptomEvent(this))
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
})