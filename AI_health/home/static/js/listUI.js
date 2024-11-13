
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
    
    addItem(text, value) {
        var newItem = document.createElement("div")
        var textElm = document.createElement("div")
        var actionElm = document.createElement("div")

        textElm.className = "text fz-18 text-white"
        textElm.innerHTML = text

        actionElm.className = "list_items_actions"
        actionElm.innerHTML = "<span>x</span>"
        newItem.setAttribute("data-value", value)
        newItem.className = `${this.#classItem} ${this.#baseChild}`
        newItem.appendChild(textElm)
        newItem.appendChild(actionElm)
        this.list.appendChild(newItem)
    }
}
