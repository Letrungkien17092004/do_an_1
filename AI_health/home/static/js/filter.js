import { JsonTool } from "./jsonTool.js"

export class Filter {
    constructor({ filterId, optionClass, dataLink, selectionObj }) {
        this.filterElm = document.getElementById(filterId) // select tag
        this.optionClass = optionClass
        this.dataLink = dataLink
        this.selectionObj = selectionObj
    }

    load() {
        // Add event
        this.filterElm.addEventListener("change", this.changeValueEvent())
        // load HTML
        this.loadOptions()
    }

    async loadOptions() {
        const types = await JsonTool.loadJson(this.dataLink)

        for (let i = 0; i < types.length; i++) {
            let newOption = document.createElement("option")
            newOption.value = types[i]
            newOption.innerHTML = types[i]
            this.filterElm.appendChild(newOption)
        }
    }

    getValue() {
        return this.filterElm.value
    }

    // JS DOM Event
    changeValueEvent() {
        var thisParent = this
        return function (event) {
            event.stopPropagation()
            thisParent.selectionObj.updateOption(thisParent.getValue())
        }
    }
}