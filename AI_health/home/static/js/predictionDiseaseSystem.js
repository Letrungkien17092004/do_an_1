

class PredictionDiseaseSystem {
    constructor({url}) {
        this.url = url
    }

    async predictServer(input) {
        let response = await fetch(`${this.url}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                input: input
            })
        })
        return await response.json()
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
            let values =thisParent.selectedList.getValues()
            thisParent.predict(values)
        }
    }

    async predict(raw_inp) {
        const res = await fetch(this.url, {
            method: "POST",
            body: JSON.stringify(raw_inp)
        })

        let data = await res.json()
        console.log(data.message)
        return data.message
    }
}
