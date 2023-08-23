from .models import CustomUser, ProductRegistrationModal, TransportRequestModal, TrackDeliveryModal, FeedbackModal
from rest_framework import serializers
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
class ProductRegistrationModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRegistrationModal
        fields = '__all__'
class TransportRequestModalSerializer(serializers.ModelSerializer):
    product = ProductRegistrationModalSerializer()
    class Meta:
        model = TransportRequestModal
        fields = '__all__'
    def create(self, validated_data):
        print(validated_data)
        return TransportRequestModal.objects.create(**validated_data)
class TrackDeliveryModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackDeliveryModal
        fields = '__all__'
class FeedbackModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackModal
        fields = '__all__'
        

