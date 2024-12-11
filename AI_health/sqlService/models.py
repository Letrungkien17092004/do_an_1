from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()  # Trường rich text
    discription = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='static/images/posts', null=True, blank=True)
    def __str__(self):
        return self.title

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=100, unique=True)
    parentId = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True
        )
    def __str__(self):
        return self.categoryName

class Post_Categories(models.Model):
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryId = models.ForeignKey(Categories, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('postId', 'categoryId')
        
    def __str__(self):
        return f'post: {self.postId} <-> category: {self.categoryId}'

class Diseases(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    searchName = models.CharField(max_length=100)
    discription = models.TextField(max_length=1000)
    postLinks = models.JSONField(null=True, blank=True)
    index = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Prescriptions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    diseaseId = models.ForeignKey(Diseases, on_delete=models.CASCADE, related_name = "prescriptions")
    foodDiscription = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

class Medicines(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    info = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    prescription = models.ForeignKey(Prescriptions, on_delete=models.CASCADE, related_name = "medicines")
    image_theme = models.ImageField(upload_to="static/images/medicines/", null=True, blank=True)
    hasTrained = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class MedicineImages(models.Model):
    id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicines, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="static/images/medicines_train/", null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ảnh của {self.medicine.name}"
