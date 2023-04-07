
from rest_framework import serializers
from .models import Message
from datetime import datetime

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    sender_img = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = '__all__'

    def get_sender_img(self,obj):
        return obj.sender.avatar.url
    
    def get_created_at(self,obj):
        return datetime.strftime(obj.created_at, "%H:%M %p")