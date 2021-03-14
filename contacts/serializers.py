from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
