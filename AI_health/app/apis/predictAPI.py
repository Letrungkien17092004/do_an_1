from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from DiseaseSystem.diseasePredictSys import DiseasePredictSys
from app.models import Diseases, Prescriptions, Medicines
import json

diseasePredictSys = DiseasePredictSys()
diseasePredictSys.load()

@require_POST
@csrf_exempt
def predictMassage(request):
    message_vi = json.loads(request.body)
    result = diseasePredictSys.diseasePredict(message_vi, predType="chat")
    res = {
        "message": result
    }
    return JsonResponse(res)

@require_POST
@csrf_exempt
def predictSelect(request):
    try:
        raw_inp = json.loads(request.body)
        result = diseasePredictSys.diseasePredict(raw_inp, predType="select")
        if result=="COUNT":
            res = {
                "message": "COUNT",
                "status": 200
            }
            return JsonResponse(res)
        key = result.strip().lower().replace(" ", "")
        disease = Diseases.objects.filter(searchName__contains=f'{key}')[0]
        prescriptions = Prescriptions.objects.filter(diseaseId = disease.id)[0]
        medicines = Medicines.objects.filter(PrescriptionsId = prescriptions.id)
        listMedicine = []
        for medicine in medicines:
            if medicine.image:
                image = medicine.image.url
            else:
                image = "null"
            listMedicine.append({
                "name": medicine.name,
                "image": image
            })

        res = {
            "message": "Succsessfuly",
            "disease": {
                "name": disease.name,
                "discription": disease.discription,
                "postLink": disease.postLinks,
            },
            "prescription": {
                "name": prescriptions.name,
                "foodDiscription": prescriptions.foodDiscription,
            },
            "medicines": listMedicine,
            "status": 200

        }
        return JsonResponse(res)
    except:
        res = {
            "message": "máy chủ đang bận. vui lòng thử lại sau",
            "status": 500
        }
    return JsonResponse(res)