# Create your helper here
from .models import Diseases, Post, Categories

class DiseaseHelper:
    def getDiseaseInfo(diseaseName):
        medicine = Diseases.objects.get(searchName = diseaseName)
        return medicine
    
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

