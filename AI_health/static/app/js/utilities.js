
export class TabManager {
    constructor({tabs, classHiden}) {
        this.tabs = tabs
        this.classHiden = classHiden
    }

    showTab(index) {
        console.log(this.tabs)
        this.tabs.forEach(tab => {
            tab.classList.add(this.classHiden)
        });
        this.tabs[index].classList.remove(this.classHiden)
    }
}