import { JsonTool } from './jsonTool.js'

export class SelectionManager {
    constructor(
        {
            formId, optionClass, btnAddId, overlay, listUI, dataLink,
            baseParentClass, baseTextClass, markClass, optionAttibutes, textKey
        }) {
        this.form = document.getElementById(formId)
        this.optionClass = optionClass
        this.btnAdd = document.getElementById(btnAddId)
        this.overlay = overlay
        this.listUI = listUI
        this.dataLink = dataLink
        this.baseParentClass = baseParentClass
        this.baseTextClass = baseTextClass
        this.markClass = markClass
        this.optionAttibutes = optionAttibutes
        this.textKey = textKey

    }

    load() {
        this.addEvent()
        this.loadSelectOption()
    }

    addEvent() {
        this.btnAdd.addEventListener("click", this.confirmEvent())
    }

    async loadSelectOption() {
        const datas = await JsonTool.loadJson(this.dataLink)

        datas.forEach((data) => {
            let baseParent = document.createElement("div")
            let newOption = document.createElement("div")
            let text = document.createElement("span")
            baseParent.className = this.baseParentClass
            text.className = this.baseTextClass
            newOption.className = this.optionClass

            this.optionAttibutes.forEach((attribute) => {
                newOption.setAttribute(`data-${attribute}`, data[`${attribute}`])
            })
            text.innerHTML = data[this.textKey]

            newOption.appendChild(text)
            baseParent.appendChild(newOption)
            this.form.appendChild(baseParent)
        })
        const optionHasLoaded = this.getOptions()
        optionHasLoaded.forEach((option) => {
            option.addEventListener("click", this.markSelectedEvent())
        })
    }

    updateOption(filterValue) {
        const options = this.getOptions()

        // Display All
        if (filterValue == "all") {
            options.forEach((option) => {
                option.classList.remove("hiden")
            })
            return
        }
        options.forEach((option) => {
            if (option.getAttribute("data-type") == filterValue) {
                option.classList.remove("hiden")
            } else {
                option.classList.add("hiden")
            }
        })
    }

    getOptions() {
        return document.querySelectorAll(`.${this.optionClass}`)
    }

    getSelected() {
        var selecteds = []
        this.getOptions().forEach((option) => {
            if (option.classList.contains(this.markClass)) {
                selecteds.push(option)
            }
        })
        return selecteds
    }

    resetMark() {

    }

    // JS DOM Event
    markSelectedEvent() {
        var thisParent = this
        return function(event) {
            event.stopPropagation()
            this.classList.toggle(thisParent.markClass)
        }
    }

    // JS DOM Event
    confirmEvent() {
        var thisParent = this
        return function (event) {
            event.stopPropagation()
            let selecteds = thisParent.getSelected()
            // add symptom
            selecteds.forEach((selected) => {
                var attributeKeyData = []
                thisParent.optionAttibutes.forEach((attribute) => {
                    let newItem =  {
                        key: `${attribute}`,
                        value: selected.getAttribute(`data-${attribute}`)
                    }
                    attributeKeyData.push(newItem)
                })
                let options = {
                    text: selected.innerText,
                    attributeKeyData: attributeKeyData
                }
                thisParent.listUI.addItem(options)
            })

            // reste selected
            selecteds.forEach((selected) => {
                selected.classList.remove("selected")
            })

            thisParent.overlay.hiden()
        }
    }
}