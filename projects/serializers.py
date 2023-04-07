from rest_framework import serializers

from .models import DesiredExpertise

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesiredExpertise
        fields = '__all__'