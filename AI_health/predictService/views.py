from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from sqlService.helper import DiseaseHelper
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
            "type" : None,
            "status": None
        }
        if chatResponse == None:
            result = diseasePredictSys.diseasePredict(message_vi, predType="chat")
            if result == "ZERO-SYMPTOM" or result == "ZERO-IMPORTANT":
                res["message"] = result
                res["status"] = "BAD"
                return JsonResponse(res)
            else:

                data = DiseaseHelper.getDiseaseInfo(result.lower())
                print(result.lower())
                if data == "Disease is not found": raise BaseException("Server logic error")
                res['status'] = "OK"
                res["message"] = "predict successful"
                res["data"] = data
                res["type"] = "FULL-DATA"
                return JsonResponse(res)
        res['status']= "OK"
        res["message"] = chatResponse
        res['type'] = 'ONLY-CHAT'
        return JsonResponse(res)
    except BaseException as error:
        print(error)
        res = {
            "message" : "Server error",
            'status' : "BAD",
        }
        return JsonResponse(res, status = 500)


@require_POST
@csrf_exempt
def predictSelect(request):
    try:
        raw_inp = json.loads(request.body)
        res = {
            "message": None,
            "status": 200,
            "data": None
        }

        result = diseasePredictSys.diseasePredict(raw_inp, predType="select")
        if (result == "ZERO-IMPORTANT") or (result == "ZERO-SYMPTOM"):
            res["message"] = "BAD"
            res['data'] = result
            return JsonResponse(res)
        
        res['message'] = "OK"
        res["data"] = DiseaseHelper.getDiseaseInfo(diseaseName=result.lower())
        return JsonResponse(res)
    except RuntimeError as error:
        res = {
            "message": "máy chủ đang bận. vui lòng thử lại sau",
            "status": 500,
            "error": error
        }
        return JsonResponse(res, status=500)
