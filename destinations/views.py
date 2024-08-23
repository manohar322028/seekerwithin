from django.shortcuts import render
from .models import Destination
from .api_files.serializers import DestinationsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET'])
def destinations_list(request):
    destinations = Destination.objects.all()
    serializer = DestinationsSerializer(destinations, many=True)
    return Response(serializer.data)