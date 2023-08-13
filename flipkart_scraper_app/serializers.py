from rest_framework import serializers
from .models import ScrappedData

class ScrappedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrappedData
        fields = '__all__'
