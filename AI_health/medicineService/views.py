from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from utilities.preprocessImage import ImagePreprocess
from sqlService.helper import MedicineHelper
from rest_framework.views import APIView
from rest_framework.views import Response
from .recogniteMedicineSys.recogniteMedicineSys import RecogniteMedicineSys

recogniteMachine = RecogniteMedicineSys()
recogniteMachine.load()
# recogniteMachine.autoTrained()
recogniteMachine.loadDataFromDatabase()
# Create your views here.


class MedicineRecogniteView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
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
                return Response({
                    "success": True,
                    "message": "OK",
                    "data": medicine
                }, status=200)
            else:
                raise Exception("data is not valid, application/json is require")
            
        except Exception as e:
            return Response({
                "success": False,
                "message": "OK",
                "data": str(e)
            }, status=400)
        