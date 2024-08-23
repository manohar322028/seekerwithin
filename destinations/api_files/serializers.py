from rest_framework import serializers
from ..models import Destination




class DestinationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['name', 'short_intro', 'detailed_info', 'thumbnail_image', 'images', 'latitude', 'longitude', 'opening_time', 'closing_time']