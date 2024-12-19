

window.addEventListener("load", async () => {
    const previousButton = document.getElementById("previous-page")
    previousButton.addEventListener("click", () => {
        history.back()
    })
})