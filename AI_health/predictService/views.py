from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from sqlService.models import Diseases, Prescriptions, Medicines
from .DiseaseSystem.diseasePredictSys import DiseasePredictSys
from chatBotService.views import chat


diseasePredictSys = DiseasePredictSys()
diseasePredictSys.load()

# Create your views here.

@require_POST
@csrf_exempt
def predictMassage(request):
    try:
        body = json.loads(request.body)
        message_vi = body["message"]
        chatResponse = chat(message_vi)
        res = {
            "message" : None,
            "status" : "OK"
        }
        if chatResponse == None:
            result = diseasePredictSys.diseasePredict(message_vi, predType="chat")
            print("work in None 2")
            if result == "ZERO-SYMPTOM":
                res["message"] = "Xin lỗi tôi không hiểu yêu cầu này của bạn"
            elif result == "ZERO-IMPORTANT":
                res["message"] = \
                "tôi không thể chuẩn đoán bệnh của bạn bởi vì những triệu chứng mà bạn cung cấp thật sự \
                không quan trọng. Nó xuất hiện ở rất nhiều căn bệnh. Tôi rất xin lỗi vì sự bất tiện này"
            else:
                res["message"] = result
        else:
            res["message"] = chatResponse
        print("work here", res)
        return JsonResponse(res)
    except Exception as e:
        res = {
            "message" : "Server error",
            'status' : "BAD"
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
