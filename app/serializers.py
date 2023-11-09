from .models import CustomUser, FeedbackModal, OrderPartiesModal, OrderModal, OrderLocationModal, OrderDeliveryModal, AgentPaymentModal, LocationModal
from rest_framework import serializers
class LocationModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationModal
        fields = '__all__'
    

class AgentPaymentModalSerializer(serializers.ModelSerializer):
    class Meta:
        model= AgentPaymentModal
        fields='__all__'
class OrderDeliveryModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDeliveryModal
        fields = '__all__'

class OrderPartiesModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPartiesModal
        fields = '__all__'
class OrderLocationModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLocationModal
        fields = '__all__'
class OrderModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModal
        fields = '__all__'
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class FeedbackModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackModal
        fields = '__all__'
        

