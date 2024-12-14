# Create your helper here
from .models import Diseases, Post, Categories, Medicines
from django.forms.models import model_to_dict
class DiseaseHelper:
    def getDiseaseInfo(diseaseName):
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
    def isExitsWithSearchName(searchName):
        return Diseases.objects.filter(searchName = searchName).exists()
    
class PostHelper:
    def getAll(pageNumber = 1, category = 'all', sortBy = 'newest'):
        posts = Post.objects.all()
        if category != "all":
            posts = posts.filter(post_categories__categoryId__categoryName=category)
        if sortBy == "newest":
            posts = posts.order_by("-created_at")
        elif sortBy == "oldest":
            posts = posts.order_by("created_at")
        return posts
    def getById(postId):
        post = Post.objects.get(id = postId)
        return post

class CategoriesHelper:
    def getAll():
        categories = Categories.objects.all()
        return categories

