

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

    // JS DOM Event
    submitEvent() {
        let thisParent = this
        return function(event) {
            console.log(thisParent.selectedList.getItem())
        }
    }
}