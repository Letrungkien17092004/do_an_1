import { OverlayDisplay } from './overlay_display.js'
import { ListUI } from './listUI.js'
import { PredictTypeSelect } from './predictionDiseaseSystem.js'
import { Filter } from './filter.js'
import { SelectionManager } from './selectionManager.js'


const overlay = new OverlayDisplay({
    activationId: "plus-symptom",
    overlayId: "select-overlay"
})

const selectedList = new ListUI({
    listId: "selected_list",
    classItem: "selected_list_items",
    baseParent: "list lis-direction-row",
    baseChild: "list-items text text-align-center"
})

const symptomSelection = new SelectionManager({
    formId: "select-form",
    optionClass: "form-options",
    btnAddId: "select-actions-submit",
    overlay: overlay,
    listUI: selectedList,
    dataLink: "/static/app/json/categories.json",
    baseParentClass: "list-items",
    baseTextClass: "text fz-18 w-500",
    optionAttibutes: ["value", "type"],
    textKey: "word",
    markClass: "selected"
})

const filter = new Filter({
    filterId: "filter-type",
    optionClass: "",
    dataLink: "/static/app/json/types.json",
    selectionObj: symptomSelection
})

const predictSystem = new PredictTypeSelect({
    url: '/api/predict/v1/select',
    selectedList: selectedList,
    submitBtn: document.getElementById("selected-btn"),
    resultContainer: document.getElementById("predict-result-container"),
    resultName: document.getElementById("predict-result-name"),
    resultDiscription: document.getElementById("predict-result-discription"),
    resultFood: document.getElementById("predict-result-food"),
    resultMedicines: document.getElementById("predict-result-medicines")
})

window.addEventListener("load", (event) => {
    overlay.load()
    selectedList.load()
    symptomSelection.load()
    filter.load()
    predictSystem.load()
})