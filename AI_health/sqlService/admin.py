from django.contrib import admin
from .models import Post, Categories, Post_Categories, Diseases, Prescriptions, Medicines, MedicineImages
from django.utils.html import format_html
# TabularInLine
class MedicinesInLine(admin.TabularInline):
    model = Medicines

class PrescriptionsInLine(admin.TabularInline):
    model = Prescriptions

class MedicineImagesInLine(admin.TabularInline):
    model = MedicineImages

# Model Admin
class MedicinesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "prescription", "theme","image_theme", "info", "price", "hasTrained")
    inlines = [MedicineImagesInLine]
    def theme(self, obj):
        if obj.image_theme:
            return format_html('<img src="{}" width="200"/>', obj.image_theme.url)

class MedicineImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "medicine", "image_tag", "image")
    def image_tag(self, obj):
        return format_html('<img src="{}" width="200"/>', obj.image.url)

class PrescriptionsAdmin(admin.ModelAdmin):
    inlines = [MedicinesInLine]

class DiseasesAdmin(admin.ModelAdmin):
    inlines = [PrescriptionsInLine]


admin.site.register(Post)
admin.site.register(Categories)
admin.site.register(Post_Categories)
admin.site.register(Diseases, DiseasesAdmin)
admin.site.register(Prescriptions, PrescriptionsAdmin)
admin.site.register(Medicines, MedicinesAdmin)
admin.site.register(MedicineImages, MedicineImagesAdmin)