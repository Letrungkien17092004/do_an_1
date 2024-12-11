

class PredictionDiseaseSystem {
    constructor({url}) {
        this.url = url
    }

    async predictServer(raw_inp) {
        const res = await fetch(this.url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(raw_inp)
        })
        let data = await res.json()
        return data
    }
}

export class PredictTypeSelect extends PredictionDiseaseSystem {
    constructor({url, selectedList, submitBtn, resultContainer, resultName, resultDiscription, resultFood,resultMedicines}) {
        super({url: url})
        this.selectedList = selectedList
        this.submitBtn = submitBtn
        this.resultContainer = resultContainer
        this.resultName = resultName
        this.resultDiscription = resultDiscription
        this.resultFood = resultFood
        this.resultMedicines = resultMedicines
    }

    load() {
        this.submitBtn.addEventListener("click", this.submitEvent())
        this.hidenContainer()
    }

    hidenContainer() {
        this.resultContainer.classList.add("hiden")
    }
    showContainer() {
        this.resultContainer.classList.remove("hiden")
        this.submitBtn.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
          });
    }
    renderResult(data) {
        this.resultName.innerHTML = data.disease.name
        this.resultDiscription.innerHTML = data.disease.discription
        this.resultFood.innerHTML = data.prescription.foodDiscription
        this.renderMedicines(data.medicines)
        // show container
        this.showContainer()
        
    }

    renderMedicines(medicines) {
        this.resultMedicines.innerHTML = ''
        medicines.forEach(medicine => {
            let newCol = document.createElement("div")
            let newMedicineCard = document.createElement("div")
            newCol.className = "col l-3"
            newMedicineCard.className = "medicine-cards"
            newMedicineCard.innerHTML = 
            `
            <div class="medicine-cards-image">
                <!-- Image here -->
                <img src="${medicine.image}" alt="">
            </div>
            <div class="medicine-cards-name">
                <!-- Name here -->
                ${medicine.name}
            </div>
            `
            newCol.appendChild(newMedicineCard)
            this.resultMedicines.appendChild(newCol)
        });
    }

    // JS DOM Event
    submitEvent() {
        let thisParent = this
        return async function(event) {
            let values = thisParent.selectedList.getValues()
            var resData = await thisParent.predictServer(values)
            if (resData.status == 200) {
                thisParent.renderResult(resData)
            } else {
                window.alert("Hệ Thống đang bận. Vui lòng thử lại sau !")
            }
        }
    }
}
