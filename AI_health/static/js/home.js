import { OverlayDisplay } from "./overlay_display.js"

const overDisplay = new OverlayDisplay({
    activationId: "predict_option",
    overlayId: "choosePredictType"
})

window.addEventListener("load", (event) => {
    overDisplay.load()
})