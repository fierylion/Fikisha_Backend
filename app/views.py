from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import CustomUserSerializer, TransactionSerializer, TransactionRecordsSerializer, UserDataSerializer

from .models import CustomUser, Transaction, TransactionRecords, UserData
import os
from azampay import Azampay
import jwt
from django.forms import model_to_dict
from .card_creation import send_email_with_attachment
import uuid
# Create your views here.
class UserView(ViewSet):
    def create_single_user(self, request):
        request.data["paid"]=False
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            del user_data["password"]
            encoded_token=jwt.encode({"user_id":user_data["id"] }, os.getenv("JWT_SECRET"), algorithm="HS256")

            return Response({"data":user_data, "token":encoded_token, "status":'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def login_single_user(self, request):
        email = request.data.get("email")
        password=request.data.get("password")
        if(email):
            user=CustomUser.objects.filter(email=email).first()
            if(user):
                obtained_password = user.password
                if(password==obtained_password):
                    encoded_token = jwt.encode({"user_id":str(user.id) }, os.getenv("JWT_SECRET"), algorithm="HS256")
                    return Response({"data":{
                        "id":str(user.id),
                        "email":user.email,
                        "paid":user.paid

                    }, "token":encoded_token, "status":"success" }, status=status.HTTP_200_OK)
                return Response({"err":"password is not correct!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"err":"Email doesn\'t exist!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"err":"Please provide email!"}, status=status.HTTP_400_BAD_REQUEST)
    def save_details(self, request):
        request.data["user"]=request.user_details.id
        request.data["membership_no"] = str(uuid.uuid4())
        if(UserData.objects.filter(user=request.user_details.id).first()):
            return Response({"err":"User details already saved!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def send_email(self, request):
        email = request.data.get("email") or request.user_details.email
        if(email):
            user_data = UserData.objects.filter(user=request.user_details.id).first()
            if(user_data):
                send_email_with_attachment(data={"membership_no":user_data.membership_no, "first_name":user_data.first_name, "surname":user_data.surname, "email":user_data.email, "phone_number":user_data.phone_number}, email=email)
                return Response({"status":"success", "msg":"sent successfull"})
            return Response({"err":"User details not found!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"err":"Please provide email!"}, status=status.HTTP_400_BAD_REQUEST)
    def get_info(self, request):
        user_data = UserData.objects.filter(user=request.user_details.id).first()
        if(user_data):
            return Response({"status":"success", "data":model_to_dict(user_data)})
        return Response({"err":"User details not found!", "msg":"not filled form!","paid":True,"status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
                
                
                

        



class PaymentOperationView(ViewSet):
    def create_payment_link(self, request):
        provider = request.data.get("provider")
        if(provider):
            azampay = Azampay( app_name=os.environ.get('APP_NAME'), client_id=os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET_KEY'), sandbox=True)
            track = str(uuid.uuid4())
            user= CustomUser.objects.get(id=request.user_details.id)
            user.reference=track
            user.save()

            data = azampay.generate_payment_link(
                amount=10000,
                external_id=track,
                provider=provider,
                redirect_success_url = 'https://dufa.netlify.app/homepage'
            )
            print(data)
            return Response(data, status=status.HTTP_200_OK)
        return Response({"err":"Please provide provider"}, status=status.HTTP_400_BAD_REQUEST)
    def receive_callback(self, request):
        #message, user, password, clientId, submerchantAcc, additionalProperties
        print(request.data)
        request.data.pop("message")
        request.data.pop("additionalProperties")
        request.data.pop("clientId")
        request.data.pop("password")
        request.data.pop("submerchantAcc")
        request.data.pop("user")
        print(request.data)
        print(request.data['utilityref'])
        user_required = CustomUser.objects.filter(reference=request.data['utilityref']).first()
       
        request.data['user']=user_required.id
        serializer=TransactionSerializer(data=request.data)
        if serializer.is_valid():
            print("valid")
            serializer.save()
            
            usd =CustomUser.objects.get(reference=request.data['utilityref'])
            usd.paid=True
            usd.save()

            print("paid", user_required.email)
            return Response({"status":"success"}, status=status.HTTP_200_OK)
        print("error", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
            

  
