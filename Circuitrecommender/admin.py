from django.contrib import admin
from .models import *

@admin.register(Tourism)
class TourismAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'category_name', 'subcategory_name', 'subsubcategory',
        'rating', 'url', 'name', 'address', 'latitude', 'longitude',
        'cuisine', 'Dietaryrestrictions', 'price',
        'GoodFor', 'Duration','Country','destinations_features'
    )
    search_fields = (
        'name', 'address', 'category_name', 'subcategory_name',
        'subsubcategory','destinations_features','price'
    )