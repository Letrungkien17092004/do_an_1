# Create your helper here
from .models import Diseases, Post, Categories, Medicines, MedicineImages
from django.shortcuts import get_object_or_404
class DiseaseHelper:
    def getDiseaseInfo(self, diseaseName):
        if not DiseaseHelper.isExitsWithSearchName(diseaseName):
            return "Disease is not found"
        disease = Diseases.objects.get(searchName = diseaseName)
        prescriptions = disease.prescriptions.all()
        prescriptWithMedicine = []

        for prescript in prescriptions:
            medicines = Medicines.objects.filter(prescription_medicines__prescriptionId__id = prescript.id)
            prescriptDict = {
                "name": prescript.name,
                "foodDiscription": prescript.foodDiscription,
            }
            medicineDicts = [
                {
                    "name": medicine.name, 
                    "info": medicine.info, 
                    "price": medicine.price,
                    "url": medicine.image_theme.url,
                    "links": medicine.links
                } 
                for medicine in  medicines
                ]
            prescriptWithMedicine.append({
                "prescription": prescriptDict,
                "medicines": medicineDicts
            })
        diseaseDict = {
            "name": disease.name,
            "discription": disease.discription,
            "postLinks": disease.postLinks,
        }
        return {
            "disease": diseaseDict,
            "prescript-Medicine": prescriptWithMedicine
        }
    def isExitsWithSearchName(self, searchName):
        return Diseases.objects.filter(searchName = searchName).exists()
    
class PostHelper:
    def getAll(self, pageNumber = 1, category = 'all', sortBy = 'newest'):
        posts = Post.objects.all()
        if category != "all":
            posts = posts.filter(post_categories__categoryId__categoryName=category)
        if sortBy == "newest":
            posts = posts.order_by("-created_at")
        elif sortBy == "oldest":
            posts = posts.order_by("created_at")
        return posts
    def getById(self, postId):
        post = Post.objects.get(id = postId)
        return post

class CategoriesHelper:
    def getAll():
        categories = Categories.objects.all()
        return categories

class MedicineHelper:
    def getAllMedicine():
        medicines = Medicines.objects.all()
        return medicines
    def getById(medicineId):
        medicine = get_object_or_404(Medicines, id = medicineId)
        return medicine
    
    def getImageOfMedicine(medicineId, hasTrained = False):
        medicine = get_object_or_404(Medicines, id = medicineId)
        images = medicine.images.filter(hasTrained=hasTrained)
        return images
    def getImageById(imageId):
        image = MedicineImages.objects.get(id = imageId)
        return image
    def setImageHasTrained(imageId, hasTrained):
        image = MedicineImages.objects.get(id = imageId)
        image.hasTrained = hasTrained
        image.save()

