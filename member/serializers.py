import datetime
from rest_framework import serializers
from .models import UserProfile

class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        if value:
            return value.strftime('%Y/%m/%d')
        return ''

    def to_internal_value(self, data):
        try:
            return datetime.datetime.strptime(data, '%Y/%m/%d').date()
        except ValueError:
            raise serializers.ValidationError('Date format should be YYYY/MM/DD')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserProfile
        fields = [
            'email', 'password', 'full_name', 'profile_picture', 
            'phone_number', 'date_of_birth', 'gender', 
            'height', 'weight', 'medical_history'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        member_profile = UserProfile.objects.create(**validated_data)
        member_profile.set_password(password)
        member_profile.save()
        return member_profile
