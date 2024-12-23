from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from utilities.preprocessImage import ImagePreprocess
from sqlService.helper import MedicineHelper
from rest_framework.views import APIView
from rest_framework.views import Response
from django.utils.decorators import method_decorator
from .recogniteMedicineSys.recogniteMedicineSys import RecogniteMedicineSys
import json
recogniteMachine = RecogniteMedicineSys()
recogniteMachine.load()
# recogniteMachine.autoTrained()
recogniteMachine.loadDataFromDatabase()
# Create your views here.



@csrf_exempt
def medicineSearch(request):
    try:
        request.data = json.loads(request.body)
        if request.content_type != "application/json": raise Exception("only accept application/json")
        if request.data.get("image") is None: raise KeyError("image field is require in ")
        result = ImagePreprocess.makeImageArray(request.data)
        if result["success"]:
            vector = recogniteMachine.extractVector(result["image_array"])
            searchResult = recogniteMachine.lookUpData(vector)
            medicine = []
            for data in searchResult:
                medicineDB = MedicineHelper.getById(data["id"])
                medicine.append({
                    "name": medicineDB.name,
                    "info": medicineDB.info,
                    "price": medicineDB.price,
                    "url": medicineDB.image_theme.url,
                    "links": medicineDB.links,
                })
            return JsonResponse({
                "success": True,
                "message": "OK",
                "data": medicine
            }, status=200)
        else:
            raise Exception("invalid data, please check image-filed is base64 yet")
    except KeyError as e:
        return JsonResponse({
            "message" : str(e),
            "success": False
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e),
        }, status=400)


# @method_decorator(csrf_exempt, name='dispatch')
# class MedicineRecogniteView(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             print(request.data)
#             if request.content_type != "application/json": raise Exception("only accept application/json")
#             if request.data.get("image") is None: raise KeyError("image field is require in ")
#             result = ImagePreprocess.makeImageArray(request.data)
#             if result["success"]:
#                 vector = recogniteMachine.extractVector(result["image_array"])
#                 searchResult = recogniteMachine.lookUpData(vector)
#                 medicine = []
#                 for data in searchResult:
#                     medicineDB = MedicineHelper.getById(data["id"])
#                     medicine.append({
#                         "name": medicineDB.name,
#                         "info": medicineDB.info,
#                         "price": medicineDB.price,
#                         "url": medicineDB.image_theme.url,
#                         "links": medicineDB.links,
#                     })
#                 return Response({
#                     "success": True,
#                     "message": "OK",
#                     "data": medicine
#                 }, status=200)
#             else:
#                 raise Exception("invalid data, please check image-filed is base64 yet")
#         except KeyError as e:
#             return Response({
#                 "message" : str(e),
#                 "success": False
#             }, status=400)
#         except Exception as e:
#             return Response({
#                 "success": False,
#                 "message": str(e),
#             }, status=400)


        