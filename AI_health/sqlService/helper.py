# Create your helper here
from .models import Diseases

class DiseaseHelper:
    def getDiseaseInfo(diseaseName):
        medicine = Diseases.objects.get(searchName = diseaseName)
        return medicine

