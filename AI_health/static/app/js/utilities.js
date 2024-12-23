
export class TabManager {
    constructor({tabs, classHiden}) {
        this.tabs = tabs
        this.classHiden = classHiden
    }

    showTab(index) {
        this.tabs.forEach(tab => {
            tab.classList.add(this.classHiden)
        });
        this.tabs[index].classList.remove(this.classHiden)
    }
}