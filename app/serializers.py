from .models import CustomUser, Transaction, TransactionRecords, UserData
from rest_framework import serializers
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
class TransactionRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionRecords
        fields = '__all__'
class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'


