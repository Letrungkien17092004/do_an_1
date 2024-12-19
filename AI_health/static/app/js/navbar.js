

window.addEventListener("load", async () => {
    const previousButton = document.getElementById("previous-page")
    previousButton.addEventListener("click", () => {
        history.back()
    })

    // const navbar = document.getElementById("main-navbar")
    // const triggerScrollHeight = 100

    // window.addEventListener("scroll", () => {
    //     if (window.screenY > triggerScrollHeight) {
    //         navbar.classList.add("fixed")
    //     } else {
    //         navbar.classList.remove("fixed")
    //     }
    // })
})