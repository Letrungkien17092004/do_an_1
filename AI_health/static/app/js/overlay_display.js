
export class OverlayDisplay {
    constructor({activationId, overlayId}) {
        this.activation = document.getElementById(activationId)
        this.overlay = document.getElementById(overlayId)
    }

    load() {
        this.activation.addEventListener("click", this.OpenEvent.bind(this))
        this.overlay.addEventListener("click", this.hiddenEvent.bind(this))
    }

    // JS DOM Event
    OpenEvent(event) {
        event.stopPropagation()
        if (this.overlay.classList.contains("hiden")) {
            this.overlay.classList.remove("hiden")
        }
    }

    // JS DOM Event
    hiddenEvent(event) {
        event.stopPropagation()
        if (event.target == this.overlay) {
            if (!this.overlay.classList.contains("hiden")) {
                this.overlay.classList.add("hiden")
            }
        }
    }

    open() {
        if (this.overlay.classList.contains("hiden")) {
            this.overlay.classList.remove("hiden")
        }
    }

    hiden() {
        if (!this.overlay.classList.contains("hiden")) {
            this.overlay.classList.add("hiden")
        }
    }
}