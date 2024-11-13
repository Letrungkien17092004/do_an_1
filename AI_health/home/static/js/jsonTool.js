

export class JsonTool {
    static async loadJson(url) {
        var res = await fetch(url, {
            method: "GET"
        })
        return await res.json()
    }
}