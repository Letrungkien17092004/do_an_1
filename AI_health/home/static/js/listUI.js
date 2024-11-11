
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

    getContentItem() {
        var items = this.getItem()
        var listContent = []
        items.forEach((item) => {
            listContent.push(item.innerHTML)
        })

        return listContent
    }
    
    addItem(text) {
        var newItem = document.createElement("div")
        var textElm = document.createElement("div")
        var actionElm = document.createElement("div")

        textElm.className = "text fz-18 text-white"
        textElm.innerHTML = text

        actionElm.className = "list_items_actions"
        actionElm.innerHTML = "<span>x</span>"

        newItem.className = `${this.#classItem} ${this.#baseChild}`
        newItem.appendChild(textElm)
        newItem.appendChild(actionElm)
        this.list.appendChild(newItem)
    }
}
