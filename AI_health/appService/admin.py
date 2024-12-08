from django.contrib import admin
from .models import Post, Categories, Post_Categories, Diseases, Prescriptions, Medicines
from django.utils.html import format_html
# TabularInLine
class MedicinesInLine(admin.TabularInline):
    model = Medicines

class PrescriptionsInLine(admin.TabularInline):
    model = Prescriptions

# Model Admin
class MedicinesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "PrescriptionsId", "image_tag", "image")
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100"/>', obj.image.url)
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