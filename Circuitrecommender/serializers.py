from rest_framework import serializers
from .models import Hotel, Tourism

class TourismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tourism
        fields = '__all__'
class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'