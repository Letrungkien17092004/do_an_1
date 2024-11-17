

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
        window.alert(data.message)
        console.log(data)
        return data
    }
}

export class PredictTypeSelect extends PredictionDiseaseSystem {
    constructor({url, selectedList, submitBtn}) {
        super({url: url})
        this.selectedList = selectedList
        this.submitBtn = submitBtn
    }

    load() {
        this.submitBtn.addEventListener("click", this.submitEvent())
    }

    // JS DOM Event
    submitEvent() {
        let thisParent = this
        return function(event) {
            let values = thisParent.selectedList.getValues()
            thisParent.predictServer(values)
        }
    }
}
