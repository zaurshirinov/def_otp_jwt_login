from rest_framework import serializers

from .models import Project


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=5)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 
            'title', 
            'description', 
            'created_by',
            'status', 
            'created_at'
        ]
        read_only_fields = [
            'id', 
            'created_by', 
            'status', 
            'created_at'
        ]
        