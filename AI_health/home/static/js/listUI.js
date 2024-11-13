
export class ListUI {
    #baseParent
    #baseChild
    #listId
    #classItem
    constructor({listId, classItem, baseParent, baseChild}) {
        this.#baseParent = baseParent
        this.#baseChild = baseChild
        this.#listId = listId
        this.#classItem = classItem
    }

    load() {
        this.list = document.getElementById(this.#listId)
    }

    getItem() {
        return this.items = document.querySelectorAll(`.${this.#classItem}`)
    }

    getValues() {
        var values = []
        var items = this.getItem()
        items.forEach((item) => {
            values.push(item.getAttribute("data-value"))
        })

        return values
    }
    
    addItem({text, attributeKeyData}) {
        var newItem = document.createElement("div")
        var textElm = document.createElement("div")
        var actionElm = document.createElement("div")

        textElm.className = "text fz-18 text-white"
        textElm.innerHTML = text

        actionElm.className = "list_items_actions text fz-16"
        actionElm.innerHTML = "<span>x</span>"
        actionElm.addEventListener("click", this.removeEvent())
        attributeKeyData.forEach((item) => {
            newItem.setAttribute(`data-${item.key}`, item.value)
        })
        newItem.className = `${this.#classItem} ${this.#baseChild}`
        newItem.appendChild(textElm)
        newItem.appendChild(actionElm)
        this.list.appendChild(newItem)
    }

    // JS DOM Event
    removeEvent() {
        var thisParent = this
        return function(event) {
            event.stopPropagation()
            this.closest(".selected_list_items").remove()
        }
    }
}
