const overDisplay = document.getElementById("overDisplay")
const predictOption = document.getElementById("predict_option")


predictOption.addEventListener("click", (event) => {
    event.stopPropagation()
    if (overDisplay.classList.contains("hiden")) {
        overDisplay.classList.remove("hiden")
    }
})

overDisplay.addEventListener("click", (event) => {
    event.stopPropagation()
    if (event.target == overDisplay) {
        if (!overDisplay.classList.contains("hiden")) {
            overDisplay.classList.add("hiden")
        }
    }
})